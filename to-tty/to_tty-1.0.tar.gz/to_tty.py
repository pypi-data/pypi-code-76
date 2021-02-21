#!/usr/bin/env python3

import click
from subprocess import Popen, PIPE
from pathlib import Path
from typing import Union
import json
import sys
import os


metafile = Path('/tmp/to_tty')


def save_tty(id, tty):
    '''Save the tty `tty` under id `id` in the tempfile'''
    # touch the file if its not there
    if not metafile.exists():
        with open(metafile, 'w') as f:
            f.write('{}')
    else:  # read existing data
        with open(metafile, 'r') as f:
            metadata = json.load(f)
    # update data and write
    metadata.update({str(id): tty})
    with open(metafile, 'w') as f:
        json.dump(metadata, f)


class ToTTY:
    """ context manager to redirect stdout to tty saved with an id.

    Usage:
        with ToTTY(<tty id>):
            print('abc')  # 'abc' will appear in the tty with id <tty id>.
        print('def') # def will appear in the default print location.

    In this way, any program or subprocess can be run with redirection to the
    other terminal.
    """

    def __init__(self, id):
        self.id = str(id)
        self._stdout = None
        with open(metafile, 'r') as f:
            self.tty = json.load(f)[self.id]

    def __enter__(self):
        if self._stdout is not None:
            raise ValueError('have already redirected stdout!')
        self._stdout = sys.stdout
        sys.stdout = open(self.tty, 'w').__enter__()

    def __exit__(self, type, value, traceback):
        sys.stdout.__exit__(type, value, traceback)
        sys.stdout = self._stdout
        self._stdout = None


def get_child_pid(pid):
    return get_field(Popen(['pgrep', '-P', pid], stdout=PIPE))


@click.command()
@click.argument('cache_id')
@click.option('--set-tty', '-s', is_flag=True, help='set cache-number (0 if '
        'not supplied) tty to the active X window\'s tty')
@click.option('--command', '-c', is_flag=False,
        help='execute [command] and pipe output to TTY')
def main(cache_id, set_tty: bool, command: str = None):
    '''this script executes COMMAND and sends output to a cached TTY with
    CACHE_ID as its saved id.

    If no commands or flags are selected, STDIN is routed straight to the
    selected TTY.'''

    assert cache_id is not None
    if set_tty:
        active_pid = 0
        save_tty(str(cache_id), get_tty(get_active_pid()))
    elif command:
        env = environ_variables(str(cache_id))
        with ToTTY(str(cache_id)):  # redirect output to the tty
            # previously used 'script', '-eqc', command but this was broken in
            # an update.
            Popen(command, env=env, stdout=sys.stdout, stderr=sys.stdout, shell=True)
    else:  # print stdin to stdout (which is redirected to tty)
        with ToTTY(str(cache_id)):
            while True:
                print(input())


def get_field(s: Union[str, Popen], cut: int=-1, skiplines: int=0):
    '''return the cut element (seperated by whitespace) from the skiplines-th line.

    if s is of type Popen, extract from stdout

    By default, returns the last item of the first line.'''
    if type(s) is Popen:
        s = s.communicate()[0].decode('utf-8')
    s.split('\n')[skiplines].strip().split()[cut]
    return s.split('\n')[skiplines].strip().split()[cut]


def get_tty(pid: str):
    rv = get_field(Popen(['ps', '-q', get_child_pid(pid), 'axo', 'tty'], stdout=PIPE), skiplines=1)
    if rv == '?':
        return False
    return '/dev/' + rv


def get_active_pid():
    wid = get_field(Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE))
    return get_field(get_window_info(wid, '_NET_WM_PID'))


def get_window_info(wid, atom=None):
    args = ['xprop', '-id', wid]
    if atom is not None:
        args.append(atom)
    x = Popen(args, stdout=PIPE).stdout.read()
    return x.decode('utf-8')


def environ_variables(id):
    '''update environment variables for call

    copy environment variables from source process (the one that calls this
    script) and update LINES and COLUMNS to be the same as the destination
    terminal (the one with id)
    '''
    # get tty name
    tty = ToTTY(id).tty
    # get relevant information using stty
    rows, columns = Popen(['stty', '-F', tty, 'size'], stdout=PIPE
            ).communicate()[0].decode('utf-8').split()
    # get existing environment
    rv = os.environ.copy()
    # add relevant information
    rv.update({'LINES': rows, 'COLUMNS': columns})
    return rv


if __name__ == '__main__':
    main()
