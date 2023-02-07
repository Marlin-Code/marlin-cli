import click

@click.command()
@click.argument('NAME')
def docs(name):
  """Fetches the documentation url for the Marlin archetype or module NAME"""
  click.echo(f'Fetching documentation for {name}')