import sys
import importlib
import pkgutil


def import_submodules(package_name):
    """Import all submodules of a module, recursively

    From https://stackoverflow.com/a/25083161
    """
    package = sys.modules[package_name]
    return {
        name: importlib.import_module(package_name + "." + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }


__all__ = import_submodules(__name__).keys()
