import click
from cfn_tools import load_yaml, dump_yaml


def cft_merge(source, destination):
    """
    Add source objects from a CFT to destination CFT
    """
    with open(source, "r") as s:
        raw = s.read()
        source_cft = load_yaml(raw)
    with open(destination, "r") as d:
        raw = d.read()
        destination_cft = load_yaml(raw)

    if not destination_cft:
        click.echo(
            click.style(
                f"Unable to parse yaml file. Ensure that it is properly formatted and try again.",
                fg="red",
            )
        )
        raise Exception("ParseException: Unable to parse yaml file.")

    def item_gen(source, dest):
        if isinstance(source, dict):
            for key, val in source.items():
                if not dest or key not in dest:
                    dest[key] = val

                item_gen(val, dest[key])

    item_gen(source_cft, destination_cft)

    with open(destination, "w") as d:
        d.write(dump_yaml(destination_cft))
