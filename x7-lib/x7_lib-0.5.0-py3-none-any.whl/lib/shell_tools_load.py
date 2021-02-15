"""
    Loader code for shell tools.  Don't call directly, use:
    >>> from x7.shell import *
"""

import importlib

loaded_tools = {}
loaded_modules = []


class ShellTool(object):
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def doc(self):
        return self.action.__doc__.strip().splitlines()[0].strip()

    def __repr__(self):
        return '%s - %s: use %s() to invoke' % (self.name, self.doc(), self.name)

    def __call__(self, *args, **kwargs):
        self.action(*args, **kwargs)


def load_tools(other_globals: dict):
    import x7.lib.shell_tools

    all_x7 = ['lib', 'testing', 'geom', 'view']

    for mod_name in all_x7:
        try:
            importlib.import_module('x7.%s' % mod_name)
        except ModuleNotFoundError:
            continue

        loaded_modules.append(mod_name)

        mod = importlib.import_module('x7.%s.shell_tools' % mod_name)
        for k in getattr(mod, '__all__'):
            val = ShellTool(k, getattr(mod, k))
            other_globals[k] = val
            loaded_tools[k] = val

    if not loaded_modules:
        print('No shell tools found')   # pragma: no cover
    else:
        x7.lib.shell_tools.tools()
