from marlin_cli.commands.docs import docs
from marlin_cli.commands.init import init
from marlin_cli.commands.install import install
from marlin_cli.commands.list import list
import click


@click.group()
@click.version_option("0.0.0")
def cli():
    pass


cli.add_command(init)
cli.add_command(install)
cli.add_command(list)
cli.add_command(docs)

if __name__ == "__main__":
    cli()
