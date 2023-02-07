import click

@click.command()
@click.argument('archetype')
@click.argument('directory')
def init(archetype, directory):
  '''
  Creates a new Marlin project based on ARCHETYPE at DIRECTORY
  '''
  click.echo(f'Creating {archetype} at {directory}')