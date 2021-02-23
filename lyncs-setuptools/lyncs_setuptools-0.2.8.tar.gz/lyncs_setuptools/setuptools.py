"""
Completion of kwargs for setup
"""

__all__ = [
    "complete_kwargs",
    "setup",
    "get_kwargs",
    "print_keys",
]

import sys
import pathlib
import codecs
from functools import wraps
from collections import OrderedDict
from setuptools import find_packages
from setuptools import setup as _SETUP

from .version import find_version
from .data_files import add_to_data_files, get_data_files
from .description import find_readme, find_description, get_keywords
from .classifiers import get_classifiers
from .author import find_author, find_email, find_download_url
from .cmake import CMakeBuild


def complete_kwargs(*args, **kwargs):
    """
    Completes kwargs with deduced setup options
    """
    if args:
        assert len(args) == 1, "Only one arg allowed and it will be threated as name."
        assert "name" not in kwargs, "Repeated name parameter"
        kwargs["name"] = args[0]

    kwargs.setdefault("author", find_author())
    kwargs.setdefault("author_email", find_email())
    kwargs.setdefault("version", find_version())

    kwargs.setdefault("url", find_download_url())
    kwargs.setdefault("project_urls", OrderedDict())

    download_url = find_download_url()
    if download_url:
        kwargs["project_urls"].setdefault("Source", find_download_url())

    readme = find_readme()
    if readme and kwargs["project_urls"].get("Source", False):
        kwargs["project_urls"].setdefault(
            "Documentation", kwargs["project_urls"]["Source"] + "/" + readme
        )

    if "github" in kwargs["project_urls"].get("Source", ""):
        kwargs["project_urls"].setdefault(
            "Tracker", kwargs["project_urls"]["Source"] + "/issues"
        )

    if "github" in kwargs["project_urls"].get("Source", ""):
        kwargs["project_urls"].setdefault(
            "Download", kwargs["project_urls"]["Source"] + "/archive/master.zip"
        )

    kwargs.setdefault("packages", find_packages())
    packages = kwargs["packages"]
    test_dirs = []
    if len(packages) > 1:
        test_dirs = [pkg for pkg in packages if pkg.startswith("test")]
        packages = [pkg for pkg in packages if pkg not in test_dirs]
        kwargs["packages"] = packages

    kwargs.setdefault("name", packages[0])
    kwargs["classifiers"] = get_classifiers(kwargs.get("classifiers", None))

    dshort, dlong, dtype = find_description()
    kwargs.setdefault("description", dshort)
    kwargs.setdefault("long_description", dlong)
    kwargs.setdefault("long_description_content_type", dtype)
    kwargs.setdefault("keywords", get_keywords(dshort))

    if "ext_modules" in kwargs:
        kwargs.setdefault("cmdclass", dict())
        kwargs["cmdclass"].setdefault("build_ext", CMakeBuild)

    kwargs.setdefault("install_requires", [])
    if "name" in kwargs and kwargs["name"] != "lyncs_setuptools":
        kwargs["install_requires"].append("lyncs-setuptools")

    kwargs.setdefault("extras_require", {})
    if kwargs["extras_require"] and "all" not in kwargs["extras_require"]:
        _all = set()
        for val in kwargs["extras_require"].values():
            _all = _all.union(val)
        kwargs["extras_require"]["all"] = list(_all)

    kwargs.setdefault("data_files", [])
    add_to_data_files(*kwargs["data_files"])

    for test_dir in test_dirs:
        files = list(str(path) for path in pathlib.Path(test_dir).glob("**/*.py"))
        add_to_data_files(*files)

    kwargs["data_files"] = get_data_files()

    return kwargs


@wraps(_SETUP)
def setup(*args, **kwargs):
    "setuptools.setup wrapper"
    return _SETUP(**complete_kwargs(*args, **kwargs))


def get_kwargs():
    "Returns the complete set of kwargs passed to setup by calling setup.py"

    # pylint: disable=global-statement,exec-used
    global _SETUP
    _tmp = _SETUP
    ret = dict()
    _SETUP = ret.update
    with codecs.open("setup.py", encoding="utf-8") as _fp:
        exec(_fp.read())
    _SETUP = _tmp
    return ret


def print_keys(keys=None):
    """
    Prints all or part of the kwargs given to setup by calling setup.py.

    Parameters
    ----------
    keys: list
      List of keys to print. If empty all of them are printed.
      Note: if None is given, then sys.argv is used
    """
    keys = sys.argv[1:] if keys is None else ([keys] if isinstance(keys, str) else keys)

    try:
        kwargs = get_kwargs()
    except FileNotFoundError:
        print("No file 'setup.py' found in the current directory.")
        sys.exit(1)

    if len(keys) == 1:
        assert keys[0] in kwargs, "Allowed options are '%s'" % ("', '".join(kwargs))
        print(kwargs[keys[0]])
    else:
        for key, res in kwargs.items():
            if isinstance(res, str) and "\n" in res:
                res = '"""\n' + res + '\n"""'
            elif isinstance(res, str):
                res = '"' + res + '"'
            elif isinstance(res, list) and res:
                res = "[\n" + ",\n".join((repr(i) for i in res)) + "\n]"
            else:
                res = repr(res)

            res = res.replace("\n", "\n |  ")
            if not keys or key in keys:
                print("%s: %s\n" % (key, res))
