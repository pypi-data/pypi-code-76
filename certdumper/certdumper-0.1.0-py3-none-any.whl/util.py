import re
import sys
from datetime import datetime
from typing import Any


is_tty = sys.stdout.isatty()


def clog(msg, *args, **kw):
    date_tag = datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
    cprint(f"{date_tag} | {msg}", *args, **kw)


def cprint(msg: str, *args: Any, **kw: Any) -> None:
    print(_cfmt(f"{msg}<0>", *args, **kw))


def _cfmt(msg: str, *args: Any, **kw: Any) -> str:
    """ Generate shell color opcodes from a pretty coloring syntax. """
    if len(args) or len(kw):
        msg = msg.format(*args, **kw)

    opcode_subst = '\x1b[\\1m' if is_tty else ''
    return re.sub(r'<(\d{1,2})>', opcode_subst, msg)
