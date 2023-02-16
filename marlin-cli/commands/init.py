import click
import os
import sys
import json
import requests
import tarfile
import shutil
import subprocess
from git import Repo
from api import archetypes


@click.command()
@click.argument("archetype")
@click.argument("directory")
def init(archetype, directory):
    """
    Creates a new Marlin project based on ARCHETYPE at DIRECTORY
    """

    (archetype_details, error) = archetypes.get_archetype(archetype_name=archetype)
    if not (archetype_details):
        click.echo(click.style("The requested archetype does not exist.", fg="red"))
        sys.exit(1)
    click.echo(click.style(f"Found archetype: {archetype}", fg="green"))

    project_path = os.path.join(os.getcwd(), directory)
    if os.path.exists(project_path):
        click.echo(click.style(f"The directory {directory} already exists.", fg="red"))
        sys.exit(1)
    click.echo(click.style(f"Creating project at: {project_path}...", fg="green"))
    os.mkdir(project_path)
    os.chdir(project_path)

    repository = archetype_details.get("repository")
    url = f"https://api.github.com/repos/{repository.get('owner')}/{repository.get('repo_name')}/tarball/{repository.get('version')}"
    click.echo(click.style(f"Fetching archetype at {url}", fg="green"))
    response = requests.get(
        url=url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    click.echo(click.style(f"Writing archetype tarball", fg="green"))

    with open(f"{archetype}.tar", "wb") as fp:
        fp.write(response.content)

    archive = tarfile.open(f"{archetype}.tar")
    archive.extractall()
    os.remove(f"{archetype}.tar")
    extracted_dirname = os.listdir(project_path)[0]
    shutil.copytree(
        os.path.join(os.getcwd(), extracted_dirname), os.getcwd(), dirs_exist_ok=True
    )
    shutil.rmtree(os.path.join(os.getcwd(), extracted_dirname))

    click.echo(click.style(f"Creating marlinconf.json...", fg="green"))
    base_marlin_config = {"name": directory, "archetype": archetype}
    with open("marlinconf.json", "w") as fp:
        json.dump(base_marlin_config, fp, indent=2)

    click.echo(click.style(f"Initializing Git repository", fg="green"))
    repo = Repo.init(project_path)

    click.echo(click.style(f"Installing npm modules", fg="green"))
    subprocess.call(["npm", "install"])
    repo.git.add(all=True)
    repo.git.commit("-m", "Initial Commit")
    click.echo(
        click.style(
            f"Successfully initialized {archetype} at {project_path}", fg="green"
        )
    )
