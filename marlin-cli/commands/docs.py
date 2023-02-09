import click
import sys
from api import archetypes

@click.command()
@click.argument('NAME')
def docs(name):
  """Fetches the documentation url for the Marlin archetype or module NAME"""
  archetype_details = archetypes.get_archetype(archetype_name=name)
  if (not(archetype_details)):
    click.echo(click.style("The requested entity does not exist.", fg="red"))
    sys.exit(1)
  click.echo('\n')
  click.echo(f"Documentation available at: {click.style(archetype_details['documentation_url'], fg='blue')}")
  click.echo('\n')
