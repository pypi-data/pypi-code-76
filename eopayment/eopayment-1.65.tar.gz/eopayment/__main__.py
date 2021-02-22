# eopayment - online payment library
# Copyright (C) 2011-2020 Entr'ouvert
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import configparser
import decimal
import logging
import os.path
import pprint
import subprocess
import tempfile

import click

from . import Payment, FORM, URL


def option(value):
    try:
        name, value = value.split('=', 1)
    except Exception:
        raise ValueError('invalid option %s' % value)
    return (name, value)


@click.group()
@click.option('--option', type=option, multiple=True)
@click.option('--name', type=str, default='')
@click.option('--backend', type=str)
@click.option('--debug/--no-debug', default=None)
@click.pass_context
def main(ctx, backend, debug, option, name):
    config_file = os.path.expanduser('~/.config/eopayment.ini')
    option = list(option)
    if os.path.exists(config_file):
        parser = configparser.ConfigParser(interpolation=None)
        with open(config_file) as fd:
            parser.read_file(fd)
        if debug is None:
            debug = parser.getboolean('default', 'debug', fallback=False)
        if debug is True:
            logging.basicConfig(level=logging.DEBUG)
        for section in parser.sections():
            if section == 'default':
                continue
            if ':' in section:
                config_backend, config_name = section.split(':', 1)
            else:
                config_backend, config_name = section, None
            load = False
            if not name and not backend:
                # use first section
                logging.debug('no backend and not name given using first section found')
                backend = config_backend
                load = True
            elif name and backend:
                load = (config_backend == backend and config_name == name)
            elif name:
                load = config_name == name
            elif backend:
                load = config_backend == backend
            if load:
                logging.debug('loading configuration "%s"', section)
                backend = backend or config_backend
                option.extend(parser.items(section=section))
                break
        else:
            if not backend:
                raise ValueError('no backend found')

        if parser.has_section(backend):
            option.extend(parser.items(section=backend))
    if debug is True:
        logging.basicConfig(level=logging.DEBUG)
    ctx.obj = Payment(backend, dict(option))


@main.command()
@click.argument('amount', type=decimal.Decimal)
@click.option('--param', type=option, multiple=True)
@click.pass_obj
def request(backend, amount, param):
    transaction_id, kind, what = backend.request(amount, **dict(param))
    print('Transaction ID:', transaction_id)
    if kind == FORM:
        print(what)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as fd:
            print('<!doctype html> <html> <head> <meta charset="utf-8"> </head> <body>', file=fd)
            print(what, file=fd)
            print('''<script>document.querySelector('input[type="submit"]').click()</script>''', file=fd)
            subprocess.call(['gnome-www-browser', fd.name])
            print('</body> <html>', file=fd)
    elif kind == URL:
        print('Please click on URL:', what)
        subprocess.call(['gnome-www-browser', what])


@main.command()
@click.argument('query_string', type=str)
@click.option('--param', type=option, multiple=True)
@click.pass_obj
def response(backend, query_string, param):
    payment_response = backend.response(query_string, **dict(param))
    for key, value in payment_response.__dict__.items():
        if not isinstance(value, (dict, list)):
            print(' ', key, ':', value)
        else:
            print(' ', key, ':')
            formatted_value = pprint.pformat(value)
            for line in formatted_value.splitlines(False):
                print(' ', line)

main()
