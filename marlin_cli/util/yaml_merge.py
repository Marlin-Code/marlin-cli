import yaml
import click


def yaml_merge(source, destination):
    """
    Add source json objects to destination yaml
    """
    with open(source, "r") as s:
        source_yaml = yaml.safe_load(s)
    with open(destination, "r") as d:
        destination_yaml = yaml.safe_load(d)

    if not destination_yaml:
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

    item_gen(source_yaml, destination_yaml)

    with open(destination, "w") as d:
        yaml.dump(destination_yaml, d, default_flow_style=False)
