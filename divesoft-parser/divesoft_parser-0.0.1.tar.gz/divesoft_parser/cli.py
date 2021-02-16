'''
divesoft_parser - Divesoft DLF parser

MIT License

Copyright (c) 2021 Damian Zaremba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import logging
import sys

import click

from divesoft_parser.decoder import DLFDecoder
from divesoft_parser.utilities import convert_to_json

logger: logging.Logger = logging.getLogger(__name__)


@click.group()
@click.option('--debug', is_flag=True)
def cli(debug: bool) -> None:
    '''divesoft-parser - DLF log parser.'''
    logging.basicConfig(stream=sys.stderr,
                        level=(logging.DEBUG if debug else logging.INFO),
                        format='%(asctime)-15s %(levelname)s:%(name)s:%(message)s')


@cli.command()
@click.argument('source_file', type=click.Path(exists=True))
def decode(source_file: str) -> None:
    dive = DLFDecoder.from_file(source_file)
    click.echo(convert_to_json(dive))


if __name__ == '__main__':
    cli()
