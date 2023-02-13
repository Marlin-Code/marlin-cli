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

def update_project(module_details, project_root): 
    project_files = module_details.get("project_updates")
    for source, destination in project_files:
        project_dest = os.path.join(project_root, destination)
        _, file_extension = os.path.splitext(source)
        match file_extension:
            case '.json': 
                json_merge(source, project_dest)
            case '.yaml' | '.yml': 
                yaml_merge(source, project_dest)
            case other: 
                click.echo(click.style(f'Merge unsupported for file extension {other}', fg='red'))
                sys.exit(1)

def copy_source(module_details, project_root):
    source_targets = module_details.get("raw_source_code")
    
    for source, destination in source_targets:
        shutil.copytree(source, os.path.join(project_root, destination), dirs_exist_ok=True)

def resolve_npm_deps(module_conf):
    """
    Compare source and target package.json dependencies. Adds missing dependencies.
    """
    with open('package.json', 'r') as f: 
        package_json = json.load(f)
    
    user_deps = package_json.get("dependencies")
    user_dev_deps = package_json.get("devDependencies")
    module_deps = module_conf.get("dependencies")
    module_dev_deps = module_conf.get("devDependencies")
    
    click.echo("Installing dependencies required by the module...")
    for dep, _ in module_dev_deps.items():
        if dep not in user_dev_deps:
            click.echo(click.style(f'Missing dev dependency {dep}. Installing...', fg='yellow'))
            subprocess.call(["npm", "install", dep, "--save-dev"])
    for dep, _ in module_deps.items():
        if dep not in user_deps:
            click.echo(click.style(f'Missing dependency {dep}. Installing...', fg='yellow'))
            subprocess.call(["npm", "install", dep])
    

def update_dependencies(archetype_name, module_conf): 
    (arch_conf, _) = archetypes.get_archetype(archetype_name)
    pm = arch_conf.get("package_manager")
    match pm:
        case 'npm':
            if not os.path.exists(pm):
                click.echo(click.style(f'{pm} does not exist in this directory. Unable to install required dependencies', fg='red'))
                sys.exit(1)
            resolve_npm_deps(module_conf)
        case other: 
            click.echo(click.style(f'Unrecognized or Unsupported package manager {other}', fg='red'))
            sys.exit(1)

@click.command()
@click.argument("module")
def install(module):
    """
    Installs the module MOUDLE in this project
    """
    # Require running from marlin root
    if not os.path.exists('marlinconf.json'):
        click.echo(click.style(f'marlinconf does not exist in this directory', fg='red'))
        sys.exit(1)
    (module_details, error) = modules.get_module(module_name=module)
    if (error):
        click.echo(click.style(f"The requested module `{module}` does not exist.", fg="red"))
        sys.exit(1)
    click.echo(f"Found module: {module_details}")
    
    with open('marlinconf.json', 'r') as f: 
        marlinconf = json.load(f)
    
    project_archetype = marlinconf.get('archetype')
    click.echo(click.style(f"Installing {module} for archetype {project_archetype}", fg='green'))
    
    # todo: fetch module and version
    repository = module_details.get("repository")
    url = f"https://api.github.com/repos/{repository.get('owner')}/{repository.get('repo_name')}/tarball/1.0.0"
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
    if os.path.exists('marlin-tmp'):
        click.echo(click.style(f"A `marlin-tmp` directory already exists. Please remove it and try again.", fg="red"))
        sys.exit(1)
    os.mkdir('marlin-tmp')
    os.chdir('marlin-tmp')
    
    with open(f"{module}.tar", "wb") as fp:
        fp.write(response.content)
    
    archive = tarfile.open(f"{module}.tar")
    archive.extractall()
    os.remove(f"{module}.tar")
    
    # copy source files to their target dirs
    copy_source(module_details, project_root)
    
    # update the project with other dependencies
    update_dependencies(module_details)
    update_project(module_details)
    
    os.chdir(project_root)
    os.rmdir('marlin-tmp')
    
    click.echo(click.style(f"Successfully installed {module}", fg="green"))
    
