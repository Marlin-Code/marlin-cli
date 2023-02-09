import click
import os
import sys
import json
import requests
import tarfile
import shutil
import subprocess
from git import Repo

ARCHETYPE_MAP = {
  "react-js": {
    "creator": "Marlin",
    "description": "desc",
    "docsumentation_url": "https://marlincode.notion.site/Jumpstart-Your-Frontend-3788900c2f2843a29da725fbbb3d6aa1",
    "repository": {
      "owner": "Marlin-Code",
      "repo_name": "react_frontend_module",
      "version": "1.0.0"
    }
  }
}
@click.command()
@click.argument('archetype')
@click.argument('directory')
def init(archetype, directory):
  '''
  Creates a new Marlin project based on ARCHETYPE at DIRECTORY
  '''
  if (not(archetype in ARCHETYPE_MAP)):
    click.echo(click.style("The requested archetype does not exist.", fg="red"))
    sys.exit(1)
  archetype_details = ARCHETYPE_MAP.get(archetype)
  click.echo(click.style(f"Found archetype: {archetype}", fg="green"))

  project_path = os.path.join(os.getcwd(), directory)
  if (os.path.exists(project_path)):
    click.echo(click.style(f"The directory {directory} already exists.", fg="red"))
    sys.exit(1)
  
  click.echo(click.style(f"Creating project at: {project_path}...", fg="green"))
  os.mkdir(project_path)
  os.chdir(project_path)

  repository = archetype_details.get('repository')
  url = f"https://api.github.com/repos/{repository.get('owner')}/{repository.get('repo_name')}/tarball/1.0.0"
  click.echo(click.style(f"Fetching archetype at {url}", fg="green"))
  response = requests.get(
    url=url,
    headers={
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
    }
  )
  with open(f"{archetype}.tar", 'wb') as fp:
    click.echo(click.style(f"Writing archetype tarball", fg="green"))
    fp.write(response.content)

  click.echo(click.style(f"Unpacking archetype tarball", fg="green"))
  archive = tarfile.open(f"{archetype}.tar")
  archive.extractall()
  extracted_dirname = os.listdir(project_path)[0]
  shutil.copytree(os.path.join(os.getcwd(), extracted_dirname), os.getcwd(), dirs_exist_ok=True)
  shutil.rmtree(os.path.join(os.getcwd(), extracted_dirname))
  os.remove(f"{archetype}.tar")

  click.echo(click.style(f"Creating marlinconf.json...", fg="green"))
  base_marlin_config = {
    "name": directory,
    "archetype": archetype
  }
  with open('marlinconf.json', 'w') as fp:
    json.dump(base_marlin_config, fp, indent=2)
  
  click.echo(click.style(f"Initializing Git repository", fg="green"))
  repo = Repo.init(project_path)
  repo.git.add(all=True)
  repo.git.commit('-m', 'Initial Commit')

  click.echo(click.style(f"Installing npm modules", fg="green"))
  subprocess.call(["npm","install"])
  click.echo(click.style(f"Successfully initialized {archetype} at {project_path}", fg="green"))
  