import argparse
import subprocess
import sys
from importlib.util import find_spec
from pathlib import Path
from typing import List

from . import __version__
from spelltinkle.config import Configuration
from spelltinkle.i18n import set_language
from spelltinkle.session import Session
from spelltinkle.screen import Screen
from spelltinkle.utils import find_files


def run(arguments: List[str] = None):
    from .document import Document
    from .text import TextDocument

    parser = argparse.ArgumentParser()
    add = parser.add_argument
    add('files', nargs='*')
    add('-w', '--new-window', action='store_true')
    add('--no-new-window', action='store_true', help=argparse.SUPPRESS)
    add('-m', '--module', action='append', default=[])
    add('-D', '--debug', action='store_true')
    add('-L', '--language')
    add('-g', '--git', action='store_true')
    add('-0', '--dry-run', action='store_true')
    add('-f', '--find', action='append', default=[])
    add('-s', '--select')
    add('-k', '--keys')
    add('-V', '--show-version', action='store_true')
    args = parser.parse_args(arguments)

    set_language(args.language)

    conf = Configuration()
    conf.read()

    if args.show_version:
        print(' SPEL  Version:', __version__)
        print(' LTIN  Code:', Path(__file__).parent)
        print(' KLE')
        return

    if args.new_window and not args.no_new_window:
        subprocess.run(['gnome-terminal',
                        '--geometry',
                        '84x40',
                        '--',
                        '--no-new-window'] + sys.argv,
                       stderr=subprocess.DEVNULL)
        return

    for module in args.module:
        spec = find_spec(module)
        assert spec is not None
        args.files.append(spec.origin)

    if args.git:
        out = subprocess.check_output(['git',
                                       'status',
                                       '--porcelain',
                                       '--short'],
                                      universal_newlines=True)
        for line in out.splitlines():
            status, filename = line.split()
            if status == 'M':
                args.files.append(filename)

    for x in args.find:
        args.files.extend(find_files(x))

    if args.dry_run:
        for file in args.files:
            print(file)
        return

    if args.select:
        args.files = eval(f'args.files[{args.select}]')
        if isinstance(args.files, str):
            args.files = [args.files]

    scr = Screen()

    if args.keys:
        scr.keys = args.keys.split(',')

    session = Session(scr, conf)

    for f in args.files:
        path = Path(f)
        if path.is_dir():
            from .fileinput import FileInputDocument
            doc: Document = FileInputDocument(path)
        else:
            doc = TextDocument(session)
            doc.read(path)
        session.docs.append(doc)

    if not sys.stdin.isatty():
        doc = TextDocument(session)
        from .utils import tolines
        lines = tolines(sys.stdin)
        doc.change(0, 0, 0, 0, lines, remember=False)
        session.docs.append(doc)
        # Reopen stdin so that curses works
        import os
        f = open('/dev/tty')
        os.dup2(f.fileno(), 0)

    if not session.docs:
        session.docs.append(TextDocument(session))

    session.run()
    scr.stop()


if __name__ == '__main__':
    run()
