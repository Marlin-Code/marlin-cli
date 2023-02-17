import click
import sys
from marlin_cli.api import archetypes, modules
import marlin_cli.constants as constants
import os


@click.command()
@click.option(
    "-t",
    "--type",
    "type",
    default="all",
    help="Type of entity to list, eityher module or archetype",
)
def list(type):
    """List all available modules or archetypes"""
    if type == "all":
        list_archetypes()
        list_modules()
    elif type == "archetype":
        list_archetypes()
    elif type == "module":
        list_modules()
    else:
        click.echo(
            f"Unknown type '{type}' available types are 'archetypes' and 'modules'"
        )
        sys.exit(1)


def list_archetypes():
    click.echo("Archetypes:")
    (archetype_list, error) = archetypes.list_archetypes()
    if error:
        click.echo(f"Error: {error}")
        sys.exit(1)
    for k in archetype_list:
        click.echo(f" - {k}")


def list_modules():
    click.echo("Modules:")
    (module_list, error) = modules.list_modules()
    if error:
        click.echo(f"Error: {error}")
        sys.exit(1)
    for k in module_list:
        click.echo(f" - {k}")
