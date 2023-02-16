import click
import json
import sys
import os
import subprocess
import tarfile
import requests
import shutil
from api import modules, archetypes
from util import yaml_merge
from util import json_merge


def update_project(module_install_conf):
    click.echo("Updating project files")
    project_files = module_install_conf.get("project_updates")
    for source, destination in project_files.items():
        module_source = f"marlin-tmp/{source}"
        _, file_extension = os.path.splitext(module_source)
        match file_extension:
            case ".json":
                json_merge(module_source, destination)
            case ".yaml" | ".yml":
                yaml_merge(module_source, destination)
            case other:
                click.echo(
                    click.style(
                        f"Merge unsupported for file extension {other}", fg="red"
                    )
                )
                sys.exit(1)


def copy_source(module_install_conf):
    click.echo("Migrating module source code")
    source_targets = module_install_conf.get("raw_source_code")

    for source, destination in source_targets.items():
        shutil.copytree(f"marlin-tmp/{source}", destination, dirs_exist_ok=True)


def resolve_npm_deps(module_package_location):
    """
    Compare source and target package.json dependencies. Adds missing dependencies.
    """
    click.echo("Installing new npm dependencies")
    with open("package.json", "r") as f:
        package_json = json.load(f)
    with open(f"{module_package_location}/package.json", "r") as m:
        module_package_json = json.load(m)

    user_deps = package_json.get("dependencies")
    user_dev_deps = package_json.get("devDependencies")
    module_deps = module_package_json.get("dependencies")
    module_dev_deps = module_package_json.get("devDependencies")

    click.echo("Installing dependencies required by the module...")
    for dep, _ in module_dev_deps.items():
        if dep not in user_dev_deps:
            click.echo(
                click.style(f"Missing dev dependency {dep}. Installing...", fg="yellow")
            )
            subprocess.call(["npm", "install", dep, "--save-dev"])
    for dep, _ in module_deps.items():
        if dep not in user_deps:
            click.echo(
                click.style(f"Missing dependency {dep}. Installing...", fg="yellow")
            )
            subprocess.call(["npm", "install", dep])


def update_dependencies(archetype_name):
    (arch_conf, _) = archetypes.get_archetype(archetype_name)
    pm = arch_conf.get("package_manager")
    match pm:
        case "npm":
            if not os.path.exists("package.json"):
                click.echo(
                    click.style(
                        f"a package.json does not exist in this directory. Unable to install required dependencies",
                        fg="red",
                    )
                )
                sys.exit(1)
            resolve_npm_deps("marlin-tmp")
        case other:
            click.echo(
                click.style(
                    f"Unrecognized or Unsupported package manager {other}", fg="red"
                )
            )
            sys.exit(1)


@click.command()
@click.argument("module")
def install(module):
    """
    Installs the module MOUDLE in this project
    """
    # Require running from marlin root
    if not os.path.exists("marlinconf.json"):
        click.echo(
            click.style(f"marlinconf does not exist in this directory", fg="red")
        )
        sys.exit(1)

    (module_details, error) = modules.get_module(module_name=module)
    if error:
        click.echo(
            click.style(f"The requested module `{module}` does not exist.", fg="red")
        )
        sys.exit(1)
    click.echo(f"Found module: {module_details}")

    with open("marlinconf.json", "r") as f:
        marlinconf = json.load(f)

    project_archetype = marlinconf.get("archetype")
    click.echo(
        click.style(
            f"Installing {module} for archetype {project_archetype}", fg="green"
        )
    )

    # todo: fetch module and version
    repository = module_details.get("repository")
    url = f"https://api.github.com/repos/{repository.get('owner')}/{repository.get('repo_name')}/tarball/{repository.get('version')}"
    click.echo(f"Fetching module from {url}")
    response = requests.get(
        url=url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    click.echo(click.style(f"Received module source. Writing tarball", fg="green"))

    project_root = os.getcwd()
    # write temp dir
    if os.path.exists("marlin-tmp"):
        click.echo(
            click.style(
                f"A `marlin-tmp` directory already exists. Please remove it and try again.",
                fg="red",
            )
        )
        sys.exit(1)
    os.mkdir("marlin-tmp")

    # step into marlin-tmp for easy extract
    os.chdir("marlin-tmp")
    with open(f"{module}.tar", "wb") as fp:
        fp.write(response.content)

    archive = tarfile.open(f"{module}.tar")
    archive.extractall()
    os.remove(f"{module}.tar")
    # move contents to marlin-tmp
    extracted_dirname = os.listdir(os.getcwd())[0]
    shutil.copytree(
        os.path.join(os.getcwd(), extracted_dirname), os.getcwd(), dirs_exist_ok=True
    )
    shutil.rmtree(os.path.join(os.getcwd(), extracted_dirname))
    os.chdir(project_root)
    # step out of marlin-tmp

    with open("marlin-tmp/marlin-install.json", "r") as mi:
        module_install_conf = json.load(mi)

    click.echo(
        f"Installing with the marlin-install config\n\n{json.dumps(module_install_conf, indent=2)}\n"
    )

    # copy source files to their target dirs
    copy_source(module_install_conf)

    # update the project with other dependencies
    update_dependencies(project_archetype)
    update_project(module_install_conf)

    shutil.rmtree("marlin-tmp")

    click.echo(click.style(f"Successfully installed {module}", fg="green"))
