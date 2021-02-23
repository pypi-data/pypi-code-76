"Tools for printing the list of installed packages"

__all__ = [
    "lyncs_packages",
    "lyncs_packages_verbose",
    "print_packages",
]

import pkgutil
import argparse
from pip._vendor import pkg_resources


def lyncs_packages():
    "Returns the list of Lyncs packages installed"
    return sorted(mod.name for mod in pkgutil.iter_modules(None) if "lyncs" in mod.name)


def lyncs_packages_verbose():
    "Returns the list of Lyncs packages with their dependencies and version number"
    packages = pkg_resources.working_set.by_key
    lyncs = set()
    for key, pkg in packages.items():
        if "lyncs" in key:
            lyncs.add(f"{key}=={pkg.version}")
            for req in pkg.requires():
                lyncs.add(f"{req.key}=={packages[req.key].version}")
    return sorted(lyncs)


def print_packages():
    "Executable for printing packages"
    parser = argparse.ArgumentParser("Returns the list of Lyncs packages")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="prints dependencies and version number",
    )
    args = parser.parse_args()
    if args.verbose > 0:
        print("\n".join(lyncs_packages_verbose()))
    else:
        print(" ".join(lyncs_packages()))
