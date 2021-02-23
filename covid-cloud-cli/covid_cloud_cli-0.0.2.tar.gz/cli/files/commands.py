from cli.utils import assert_config
from client import *


@click.group()
@click.pass_context
def files(ctx):
    assert_config(ctx, 'drs-url')


@files.command()
@click.pass_context
@click.argument("urls", required=False, nargs=-1)
@click.option('-o', '--output-dir', required=False, default=downloads_directory, show_default=True)
@click.option('-i', '--input-file', required=False, default=None)
@click.option('-q', '--quiet', is_flag=True, required=False)
def download(ctx, urls, output_dir, input_file, quiet):
    download_urls = []

    if len(urls) > 0:
        download_urls = list(urls)
    elif input_file:
        with open(input_file, 'r') as infile:
            download_urls = filter(None, infile.read().split('\n'))  # need to filter out invalid values
    else:
        if not quiet:
            click.echo("Enter one or more URLs. Press q to quit")

        while True:
            try:
                url = click.prompt("", prompt_suffix="", type=str)
                if url[0] == 'q' or len(url) == 0:
                    break
            except click.Abort:
                break

            download_urls.append(url)

    files_client.download_files(ctx.obj['drs-url'], download_urls, output_dir)
