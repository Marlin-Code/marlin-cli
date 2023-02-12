import click
import json
import sys
import os
import subprocess
from api import archetypes

TEST_MODULE_CONF = {
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0"
    },
    "devDependencies": {
        "jest": "^29.2.1"
    },
    "install_hook": {
        "react-js": {
            "path": "/pages"
        }
    }
}

def resolve_npm_deps(module_conf):
    """_summary_ 

    Args:
        module_conf (_type_): _description_
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
    

def dependency_check(archetype_name, module_conf): 
    (arch_conf, err) = archetypes.get_archetype(archetype_name)
    # pm = arch_conf.get("package_manager") todo: add package_manager to cli-backend
    pm = "package.json"
    if not os.path.exists(pm):
        click.echo(click.style(f'{pm} does not exist in this directory. Unable to install required dependencies', fg='red'))
        sys.exit(1)
    
    match pm: 
        case 'package.json': 
            resolve_npm_deps(module_conf)
        case _: 
            click.echo(click.style(f'Unrecognized or Unsupported package manager {pm}', fg='red'))
            sys.exit(1)
        

@click.command()
@click.argument("module")
def install(module):
    """
    Installs the module MOUDLE in this project
    """
    # Require running from root
    if not os.path.exists('marlinconf.json'):
        click.echo(click.style(f'marlinconf does not exist in this directory', fg='red'))
        sys.exit(1)
    with open('marlinconf.json', 'r') as f: 
        marlinconf = json.load(f)
    
    project_archetype = marlinconf.get('archetype')
    click.echo(click.style(f"Installing {module} for archetype {project_archetype}", fg='green'))
    
    dependency_check(project_archetype, TEST_MODULE_CONF)
    
    click.echo(click.style(f"Completed {module} for archetype {project_archetype}!", fg='green'))
