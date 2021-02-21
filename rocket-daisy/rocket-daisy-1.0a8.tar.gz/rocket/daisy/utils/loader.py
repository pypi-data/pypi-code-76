import imp
from rocket.daisy.utils.logger import info, exception, debug
import rocket.daisy.utils.thread as thread
SCRIPTS = {}

def loadScript(name, source, handler = None):
    info("Loading %s from %s" % (name, source))
    script = imp.load_source(name, source)
    SCRIPTS[name] = script

    if hasattr(script, "setup"):
        script.setup()
    if handler:
        for aname in dir(script):
            attr = getattr(script, aname)
            if callable(attr) and hasattr(attr, "macro"):
                debug("### daisy, gulliversoft, loadScript %s handler %s" % (aname, handler))
                handler.addMacro(attr)
            else:
                debug("### daisy, gulliversoft, loadScript %s is not callable" % (aname))
    else:
        debug("### daisy, gulliversoft, loadScript called without handler")

    if hasattr(script, "loop"):
        thread.runLoop(script.loop, True)

def unloadScripts():
    for name in SCRIPTS:
        script = SCRIPTS[name]
        if hasattr(script, "destroy"):
            script.destroy()
    
