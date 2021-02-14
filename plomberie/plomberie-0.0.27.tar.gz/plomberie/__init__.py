import os
import pkgutil

from plomberie.task import Task
from plomberie.manager import Manager

__all__ = [
    Task.__name__,
    Manager.__name__
]

__path__ = [x[0] for x in os.walk(os.path.dirname(__file__))]


def load_tests(loader, suite, pattern):
    for imp, modname, _ in pkgutil.walk_packages(__path__):
        if not modname.endswith('_test'):
            continue
        for test in loader.loadTestsFromModule(imp.find_module(modname).load_module(modname)):
            suite.addTests(test)
    return suite
