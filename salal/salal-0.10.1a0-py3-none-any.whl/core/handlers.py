import os
import importlib
from salal.core.log import log
from salal.core.config import config

class Handlers:

    #---------------------------------------------------------------------------

    @classmethod
    def load_handlers (cls, directory):
        # Handlers are a way to determine what processing to carry out in a
        # particular instance based on a 'tag' value. To implement a set
        # of handlers, in <directory> have separate .py files for each
        # handler. Each file should create an object called <handler>.
        # The handler object should have a method <get_tags> that returns
        # a list of the tags that should be associated with this particular
        # handler. This method will real all those files, and return a
        # dict where the keys are all the tags, and the values are the
        # corresponding handler objects. Generally each handler object
        # should have one or more additional methods that carry out the
        # actual processing, but what those are and how they are called
        # is up to the code that calls the <load_handler> method.

        handlers = dict()
        with os.scandir(os.path.join(config.system['paths']['salal_root'], directory)) as entries:
            for entry in entries:
                # filter files that start with a period or don't end
                # with .py
                if entry.is_file() and (not entry.name.startswith('.')) and entry.name.endswith('.py') and entry.name != '__init__.py':
                    package_specifier = 'salal.' + os.path.normpath(os.path.join(directory, entry.name)).replace(os.sep, '.').replace('.py', '')
                    log.message('TRACE', 'Loading handler from ' + package_specifier)
                    handler_module = importlib.import_module(package_specifier)
                    for tag in handler_module.handler.get_tags():
                        log.message('TRACE', tag)
                        handlers[tag] = handler_module.handler
        return handlers
    
    #---------------------------------------------------------------------------

handlers = Handlers
