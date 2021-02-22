# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;module_loader

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.4
dpt_module_loader/loader.py
"""

# pylint: disable=import-error,invalid-name

from contextlib import contextmanager
from os import path
from weakref import proxy
import os
import sys

from dpt_runtime.exceptions import IOException
from dpt_threading import ThreadLock

_MODE_IMP = 1
"""
Use "imp" based methods for import
"""
_MODE_IMPORTLIB = 2
"""
Use "importlib" based methods for import
"""

_mode = _MODE_IMPORTLIB

try: import importlib
except ImportError:
    import imp
    _mode = _MODE_IMP
#

class Loader(object):
    """
"Loader" provides singletons and objects based on the package, module
and class name given as "package.module:Class".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: module_loader
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _additional_base_dir = None
    """
Additional base directory we search for python files
    """
    _lock = ThreadLock()
    """
Thread safety lock
    """
    _log_handler = None
    """
The log handler is called whenever debug messages should be logged or errors
happened.
    """
    _namespace_modules_cache = { }
    """
Cache of loaded modules using "get_module_in_namespace()".
    """

    @staticmethod
    def get_base_dirs():
        """
Returns the base directories for scanning and loading python files.

:return: (str) Base paths
:since:  v1.0.0
        """

        if (Loader._additional_base_dir is not None): yield Loader._additional_base_dir

        for _path in sys.path:
            if (_path == ""): _path = "."
            if (not path.isdir(_path)): continue

            yield _path
        #
    #

    @staticmethod
    def get_module(package_module, autoload = True):
        """
Get the module for the specified package and module name.

:param package_module: Package and module name
:param autoload: True to load the module automatically if not done already.

:return: (object) Python module; None on error
:since:  v1.0.0
        """

        package_module_data = package_module.rsplit(".", 1)

        package = (None if (len(package_module_data) < 2) else package_module_data[0])
        module = package_module_data[-1]

        _callable = (Loader._load_module if (autoload) else Loader._get_module)
        return _callable(package, module)
    #

    @staticmethod
    def get_module_in_namespace(namespace_package, package_module, autoload = True):
        """
Get the module located in the specified namespace, package and module name.

:param namespace_package: Namespace package name
:param package_module: Package and module name
:param autoload: True to load the module automatically if not done already.

:return: (object) Python module; None on error
:since:  v1.0.0
        """

        _return = None

        package_module_name = "{0}.{1}".format(namespace_package, package_module)
        cached_package_module_name = Loader._namespace_modules_cache.get(package_module_name)

        if (cached_package_module_name is not None):
            _return = Loader._get_module(cached_package_module_name)

            if (_return is None):
                with Loader._lock:
                    # Thread safety
                    if (package_module_name in Loader._namespace_modules_cache):
                        del(Loader._namespace_modules_cache[package_module_name])
                    #
                #
            #
        #

        if (_return is None):
            _callable = (Loader._load_module_without_exception_logging if (autoload) else Loader._get_module)
            package_module_data = package_module.rsplit(".", 1)

            sub_package = (namespace_package
                           if (len(package_module_data) < 2) else
                           "{0}.{1}".format(namespace_package, package_module_data[0])
                          )

            module = package_module_data[-1]

            for _path in Loader.get_base_dirs():
                for dir_entry in os.listdir(_path):
                    namespace_package_path = path.join(_path, dir_entry, namespace_package.replace(".", path.sep))
                    package = "{0}.{1}".format(dir_entry, sub_package)

                    if (path.isdir(namespace_package_path)):
                        _return = _callable(package, module)

                        if (_return is not None):
                            Loader._namespace_modules_cache[package_module_name] = "{0}.{1}".format(package, module)
                            break
                        #
                    #
                #
            #
        #

        return _return
    #

    @staticmethod
    def _get_module(package, module = None):
        """
Returns the initialized Python module if applicable.

:param package: Package name
:param module: Module name

:return: (object) Python module; None if unknown
:since:  v1.0.0
        """

        package_module_name = None

        if (package is not None and module is not None): package_module_name = "{0}.{1}".format(package, module)
        elif (module is None): package_module_name = package
        else: package_module_name = module

        return (None if (package_module_name is None) else sys.modules.get(package_module_name))
    #

    @staticmethod
    def _import(package, module = None, log_exceptions = True):
        """
Imports the Python module.

:param package: Package name
:param module: Module name
:param log_exceptions: True to log exceptions thrown

:return: (object) Python module; None if unknown
:since:  v1.0.0
        """

        # global: _mode, _MODE_IMPORTLIB
        # pylint: disable=broad-except

        _return = Loader._get_module(package, module)

        if (_return is None):
            with Loader._lock:
                # Thread safety
                _return = Loader._get_module(package, module)
                _callable = (Loader._import_with_importlib if (_mode == _MODE_IMPORTLIB) else Loader._import_with_imp)

                if (_return is None):
                    try: _return = _callable(package, module)
                    except Exception as handled_exception:
                        if (log_exceptions and Loader._log_handler is not None): Loader._log_handler.error(handled_exception, context = "dpt_module_loader")
                    #
                #
            #
        #

        return _return
    #

    @staticmethod
    def _import_with_imp(package, module):
        """
Imports the Python module with "imp".

:param package: Package name
:param module: Module name

:return: (object) Python module; None if unknown
:since:  v1.0.0
        """

        _return = None

        base_path = None
        base_path_entry = ""
        package_directory = None
        package_module_name = module

        if (package is None):
            base_path_entry = "{0}.py".format(module)
        else:
            base_path_entry = package.split(".", 1)[0]
            package_directory = package.replace(".", path.sep)
            package_module_name = "{0}.{1}".format(package, module)
        #

        if (base_path_entry == ""): raise IOException("Import base path '{0}' is empty".format(base_path_entry))

        for _path in Loader.get_base_dirs():
            if (os.access(path.join(_path, base_path_entry), os.R_OK)):
                base_path = _path
                break
            #
        #

        if (base_path is not None and package_directory is not None):
            base_path = path.join(base_path, package_directory)
        #

        if (base_path is not None):
            with _imp_lock():
                ( file_obj, file_path, description ) = imp.find_module(module, [ base_path ])
                _return = imp.load_module(package_module_name, file_obj, file_path, description)
                if (file_obj is not None): file_obj.close()
            #
        #

        return _return
    #

    @staticmethod
    def _import_with_importlib(package, module):
        """
Imports the Python module with "importlib".

:param package: Package name
:param module: Module name

:return: (object) Python module; None if unknown
:since:  v1.0.0
        """

        _return = None

        package_module_name = None

        if (package is not None and module is not None): package_module_name = "{0}.{1}".format(package, module)
        elif (module is None): package_module_name = package
        else: package_module_name = module

        if (package_module_name is not None): _return = importlib.import_module(package_module_name)
        return _return
    #

    @staticmethod
    def is_defined(package_module, autoload = True):
        """
Checks if the specified package, module and class name is defined or can be
resolved after auto loading it.

:param package_module: Package and module name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v1.0.0
        """

        return (Loader.get_module(package_module, autoload) is not None)
    #

    @staticmethod
    def _load_module(package, module, log_exceptions = True):
        """
Loads the Python package and module.

:param package: Package name
:param module: Module name
:param log_exceptions: True to log exceptions thrown

:return: (object) Python module; None if unknown
:since:  v1.0.0
        """

        if (package is not None): Loader._import(package, log_exceptions = log_exceptions)
        return Loader._import(package, module, log_exceptions)
    #

    @staticmethod
    def _load_module_without_exception_logging(package, module):
        """
Loads the Python package and module without logging any traces of
exceptions.

:param package: Package name
:param module: Module name

:return: (object) Python module; None if unknown
:since:  v1.0.0
        """

        return Loader._load_module(package, module, False)
    #

    @staticmethod
    def reload(package_module, clear_caches = True):
        """
Reloads the the specified package module.

:param package_module: Package and module name
:param clear_caches: True to clear import caches before reloading

:return: (object) Reloaded module on success
:since:  v1.0.0
        """

        # global: _mode, _MODE_IMPORTLIB
        # pylint: disable=no-member

        _return = None

        module = Loader._get_module(package_module)

        if (module is not None):
            try:
                if (_mode == _MODE_IMPORTLIB):
                    if (clear_caches and hasattr(importlib, "invalidate_caches")): importlib.invalidate_caches()
                    _return = importlib.reload(module)
                else: _return = imp.reload(module)
            except ImportError as handled_exception:
                if (Loader._log_handler is not None): Loader._log_handler.debug(handled_exception, context = "dpt_module_loader")
            #
        #

        return _return
    #

    @staticmethod
    def set_additional_base_dir(base_dir):
        """
Sets an additional base directory for scanning and loading python files.

:param base_dir: Path

:since: v1.0.0
        """

        Loader._additional_base_dir = path.abspath(base_dir)
    #

    @staticmethod
    def set_log_handler(log_handler):
        """
Sets the log handler.

:param log_handler: Log handler to use

:since: v1.0.0
        """

        Loader._log_handler = proxy(log_handler)
    #
#

@contextmanager
def _imp_lock():
    """
Helper method to lock and unlock the importer safely.

:since: v1.0.0
    """

    imp.acquire_lock()
    yield
    imp.release_lock()
#
