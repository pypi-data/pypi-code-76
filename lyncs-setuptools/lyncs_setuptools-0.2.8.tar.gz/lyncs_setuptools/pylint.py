"""
Functions for generating code badges
"""

__all__ = [
    "print_pylint_badge",
]

import pkgutil
from collections import OrderedDict
import sys

try:
    from pylint.lint import Run
    import enchant
    from lyncs_utils import redirect_stdout
except ModuleNotFoundError as err:
    raise ModuleNotFoundError("Please install lyncs_setuptools[pylint].") from err

from .setuptools import get_kwargs
from . import __path__


def run_pylint(do_exit=True, spelling=True):
    "Runs the pylint executable with some additional options"

    if "." in sys.argv:
        sys.argv.remove(".")
        pkgs = []
        for pkg in get_kwargs()["packages"]:
            if pkg.split(".")[0] not in pkgs:
                pkgs.append(pkg)
        sys.argv += pkgs

    if spelling and "spelling" not in sys.argv and enchant.dict_exists("en"):
        sys.argv += [
            "--enable",
            "spelling",
            "--spelling-dict",
            "en",
            "--spelling-ignore-words",
            ",".join(ignore_words),
        ]

    return Run(sys.argv[1:], exit=do_exit)


def print_pylint_badge(do_exit=True, **kwargs):
    "Runs the pylint executable and prints the badge with the score"

    with redirect_stdout(sys.stderr):
        results = run_pylint(do_exit=False, **kwargs)

    score = results.linter.stats["global_note"]
    colors = OrderedDict(
        {
            9.95: "brightgreen",
            8.95: "green",
            7.95: "yellowgreen",
            6.95: "yellow",
            5.95: "orange",
            0.00: "red",
        }
    )

    color = "brightgreen"
    for val, color in colors.items():
        if score >= val:
            break

    print(
        "[![pylint](https://img.shields.io/badge/pylint%%20score-%.1f%%2F10-%s?logo=python&logoColor=white)](http://pylint.pycqa.org/)"
        % (score, color)
    )

    if not do_exit:
        return
    if results.linter.config.exit_zero:
        sys.exit(0)
    if score > results.linter.config.fail_under:
        sys.exit(0)
    sys.exit(results.linter.msg_status)


ignore_words = sorted(
    [
        "anymore",
        "API",
        "arg",
        "args",
        "argv",
        "bool",
        "cartesian",
        "cls",
        "color",
        "config",
        "coord",
        "coords",
        "cwd",
        "dict",
        "dofs",
        "dtype",
        "etc",
        "filename",
        "func",
        "i",
        "idxs",
        "int",
        "iterable",
        "itertools",
        "Iwasaki",
        "j",
        "kwargs",
        "lyncs",
        "metaclass",
        "mpi",
        "mpirun",
        "namespace",
        "openmp",
        "parallelize",
        "params",
        "plaquette",
        "procs",
        "QCD",
        "rhs",
        "Schwinger",
        "stdout",
        "str",
        "Symanzik",
        "sys",
        "TBA",
        "TBD",
        "tuple",
        "url",
        "utils",
        "vals",
        "varnames",
    ]
    + list(
        set(
            part
            for mod in pkgutil.iter_modules(None)
            for part in mod.name.replace("-", "_").split("_")
        ).difference([""])
    )
)
