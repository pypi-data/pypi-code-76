#!/usr/bin/python
"""See full version format docs in PEP440.
https://www.python.org/dev/peps/pep-0440/
"""
import sys
import click
import os
import configparser

from .version_manager import (
    _version_ops,
    _main_version_components,
    _segment_version_components,
    update_config_version,
)


def get_config(config_fp=os.path.join(".", "setup.cfg")):
    config = configparser.ConfigParser()
    config.read(config_fp)
    return config, config_fp


@click.group("pypack-metager")
@click.option("-q", "--quiet", is_flag=True, help="Flag for minimal output.")
@click.option(
    "--config_fp",
    default=os.path.join(".", "setup.cfg"),
    show_default=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Custom path for setup.cfg.",
)
@click.pass_context
def cli(ctx, quiet, config_fp):
    ctx.ensure_object(dict)
    ctx.obj["QUIET"] = quiet

    config, config_fp = get_config(config_fp=config_fp)
    ctx.obj["CONFIG"] = config
    ctx.obj["CONFIG_FP"] = config_fp

    if not quiet:
        click.secho("--- PYPACK-METAGER ---", fg="green")
        click.secho("A BuildNN Open Source project.", fg="green")
        click.secho("Reading/Writing from/to {}".format(config_fp))


# fmt: off
@cli.command()
@click.pass_context
@click.argument("element", type=click.Choice(list(_version_ops.keys())))
@click.option("-s", "--segment", type=click.Choice(_segment_version_components),
              default="dev", show_default=True,
              help="If element == 'segment', which segment type to increase.")
@click.option("-u", "--increment_upstream", type=click.Choice(_main_version_components),
              default=None, show_default=True,
              help="If element == 'segment', which upstream to increase "
              "if version is not already in that segment type.")
@click.option("-v", "--custom_version", default=None, show_default=True,
              help="If element == 'custom' reverts version to custom string.")
@click.option("--force", is_flag=True,
              help="If element == 'custom', flag to force version change "
              "(eg if custom is lower).")
# fmt: on
def increment(ctx, element, segment, increment_upstream, custom_version, force):
    update_config_version(
        config=ctx.obj["CONFIG"],
        config_fp=ctx.obj["CONFIG_FP"],
        element=element,
        segment=segment,
        increment_upstream=increment_upstream,
        custom_version=custom_version,
        force=force,
    )


@cli.command()
@click.pass_context
@click.argument("name", type=click.STRING, default="version")
@click.option("-s", "--section", type=click.STRING, default="metadata")
def echo_meta_elm(ctx, name, section):
    config = ctx.obj["CONFIG"]
    try:
        _section = config[section]
    except KeyError:
        raise KeyError(f"Section '{section}' does not exist in `setup.cfg`.")
    try:
        sys.stdout.write(_section[name] + "\n")
    except KeyError:
        raise KeyError(f"Tag '{name}' does not exist in `setup.cfg`/'{section}'.")


if __name__ == "__main__":
    cli()
