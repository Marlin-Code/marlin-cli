import click

@click.command()
@click.argument('module')
def install(module):
  '''
  Installs the module MOUDLE in this project
  '''
  click.echo(f'Installing {module}')