
import importlib
import logging
from mcutk.debugger.general import DebuggerBase

__all__ = ["getdebugger"]

LOGGER = logging.getLogger(__name__)

def getdebugger(type, *args, **kwargs):
    """Return debugger instance."""

    supported = {
        "jlink": "jlink.JLINK",
        "pyocd": "pyocd.PYOCD",
        "redlink": "redlink.RedLink",
        'ide': "ide.IDE",
        'blhost': "blhost.Blhost"
    }
    if type not in supported:
        return DebuggerBase('general_%s' % str(type), *args, **kwargs)

    importlib.import_module("mcutk.debugger.%s" % type)
    return eval(supported[type])(*args, **kwargs)
