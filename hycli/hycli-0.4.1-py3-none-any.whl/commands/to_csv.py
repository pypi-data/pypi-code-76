from pathlib import Path

import click

from hycli import convert_to_csv
from hycli.commons.auth import Auth
from hycli.commands.types import URL
from hycli.commands.callbacks import parse_arguments
from hycli.commands.context_default import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("url", type=URL)
@click.option("-w", "--workers", default=1, show_default=True, help="amount of workers")
@click.option(
    "-u",
    "--username",
    envvar="HYCLI_USERNAME",
    default=None,
    help="your API username for authenticating",
)
@click.option(
    "-p",
    "--password",
    envvar="HYCLI_PASSWORD",
    default=None,
    help="your API password for authenticating",
)
@click.option(
    "-H",
    "--header",
    default={},
    multiple=True,
    callback=parse_arguments,
    help="extractor endpoint header(s) can be multiple. Similair to curl, e.g. -H 'headerKey: value' -H '2ndHeaderKey: 2ndvalue'",
)
@click.option(
    "-P",
    "--param",
    default={},
    multiple=True,
    callback=parse_arguments,
    help="extractor endpoint param(s) can be multiple. Similair to curl, e.g. -P 'paramKey: value' -P '2ndParamKey: 2ndvalue'",
)
@click.option(
    "-n",
    "--normalize",
    is_flag=True,
    help="Normalize the probabilities to range(min, max) for every column",
)
@click.pass_context
def to_csv(ctx, url, workers, username, password, header, param, normalize: bool):
    """ Convert document(s) to csv """
    auth = Auth(url, username, password)

    convert_to_csv(
        ctx.obj["input_files"],
        url,
        header,
        param,
        auth.token,
        workers,
        ctx.obj["input_path"].parts[-1]
        if not ctx.obj["output_path"].suffix
        else ctx.obj["output_path"].parts[-2],
        Path.cwd() if not ctx.obj["output_path"] else ctx.obj["output_path"],
    )
