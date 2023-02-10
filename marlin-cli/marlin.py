from commands.docs import docs
from commands.init import init
from commands.install import install
import click


@click.group()
@click.version_option("0.0.1")
def cli():
    pass


cli.add_command(init)
cli.add_command(docs)
cli.add_command(install)

if __name__ == "__main__":
    cli()
