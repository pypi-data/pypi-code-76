from functools import partial
import logging
import os
import sys

import click
import tornado

from docViewer.preview_server import make_app, close_when_idle
from docViewer.render import guess_method, render as render_doc
from docViewer.logging import set_logging_level
from docViewer.openapi import app as openapi_app


@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', type=click.File('rb'), default=sys.stdin)
@click.argument('destination', type=click.File('wb'), default=sys.stdout)
@click.option('--method', type=click.STRING, default=None)
def render(source, destination, method):
    method = method or guess_method(source.name)
    source_content = source.read().decode('utf8')
    output = render_doc(source_content, method=method)
    writer = destination
    if hasattr(writer, 'buffer'):
        writer = writer.buffer
    writer.write(output)


@cli.command()
@click.argument('filename', required=False, default=None)
@click.option('--port', default='9000')
@click.option('--address', default='localhost')
@click.option('--debug', default=False)
def preview(filename, port, address, debug):
    click.echo(f'Start preview server [debug: {debug}] '
               f'bind to {address}:{port}')
    if debug:
        set_logging_level(logging.DEBUG)
    application = make_app()
    server = application.listen(port, address=address)
    tornado.ioloop.IOLoop.current().add_callback(
        partial(close_when_idle, server=server))
    if filename:
        preview_url = f'http://{address}:{port}/'\
            f'lite-preview?filename={filename}'
        click.echo(f'visit {preview_url} to preview')
    tornado.ioloop.IOLoop.current().start()


@cli.command()
@click.argument('filename', required=True)
@click.option('--port', default='9000')
@click.option('--host', default='localhost')
def preview_openapi(filename, port, host):
    os.environ.setdefault('API_DOC', filename)
    openapi_app.run(host=host, port=port)


if __name__ == '__main__':
    cli()
