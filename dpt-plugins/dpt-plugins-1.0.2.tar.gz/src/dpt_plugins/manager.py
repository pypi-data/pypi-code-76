# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;plugins

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.2
dpt_plugins/manager.py
"""

# pylint: disable=import-error,invalid-name,no-name-in-module,wrong-import-order,wrong-import-position

from copy import copy
from os import path
import os

from dpt_logging import ExceptionLogTrap
from dpt_module_loader import Loader
from dpt_runtime import Environment

_MODE_IMPORTLIB = 1
"""
Use "importlib" for import
"""

_mode = _MODE_IMPORTLIB

try: import importlib
except ImportError: _mode = None

class Manager(object):
    """
"Manager" provides methods to handle plugins.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: plugins
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _plugins = { }
    """
Dict of loaded plugins
    """

    @staticmethod
    def load_plugin(plugin, prefix = None):
        """
Load and register all plugins for the given plugin name and prefix (defaults
to empty string).

:param plugin: Plugin name
:param prefix: Plugin name prefix

:return: (bool) True on success
:since:  v1.0.0
        """

        # pylint: disable=no-member

        _return = False

        if (prefix is None
            and Environment.is_application_short_name_defined()
           ): prefix = Environment.get_application_short_name()

        if (prefix != ""): plugin = "{0}_{1}".format(prefix, plugin)

        package_paths = [ ]
        sub_package = "dpt_plugins.{0}".format(plugin)
        sub_package_path = sub_package.replace(".", path.sep)

        for _path in Loader.get_base_dirs():
            for dir_entry in os.listdir(_path):
                base_package_path = path.join(_path, dir_entry)

                if (path.isdir(base_package_path)):
                    package = "{0}.{1}".format(dir_entry, sub_package)
                    package_path = path.join(base_package_path, sub_package_path)

                    if (os.access(package_path, os.R_OK)
                        and path.isdir(package_path)
                       ): package_paths.append(( package_path, package ))
                #
            #
        #

        for package_data in package_paths:
            for dir_entry in os.listdir(package_data[0]):
                if (dir_entry.endswith(".py") and dir_entry != "__init__.py"):
                    module_name = "{0}.{1}".format(package_data[1], dir_entry[:-3])

                    module = Loader.get_module(module_name)

                    if (module is not None and hasattr(module, "register_plugin") and callable(module.register_plugin)):
                        with ExceptionLogTrap("dpt_plugins"):
                            if (plugin not in Manager._plugins): Manager._plugins[plugin] = [ ]
                            if (module_name not in Manager._plugins[plugin]): Manager._plugins[plugin].append(module_name)

                            module.register_plugin()
                            _return = True
                        #
                    #
                #
            #
        #

        return _return
    #

    @staticmethod
    def reload_plugins(plugin_reload_prefix = None, prefix = None):
        """
Reload all plugins or the plugins matching the given prefix.

:param plugin_reload_prefix: Reload prefix for plugins to be reloaded
:param prefix: Plugin name prefix

:return: (bool) True on success
:since:  v1.0.0
        """

        # global: _mode, _MODE_IMPORTLIB
        # pylint: disable=broad-except, no-member

        _return = True

        if (prefix is None
            and Environment.is_application_short_name_defined()
           ): prefix = Environment.get_application_short_name()

        if (prefix != ""):
            plugin_reload_prefix = (prefix
                                    if (plugin_reload_prefix is None) else
                                    "{0}_{1}".format(prefix, plugin_reload_prefix)
                                   )
        #

        if (_mode == _MODE_IMPORTLIB
            and hasattr(importlib, "invalidate_caches")
           ): importlib.invalidate_caches()

        for plugin in Manager._plugins:
            if (plugin_reload_prefix is None or plugin.startswith("{0}.".format(plugin_reload_prefix))):
                modules = (Manager._plugins[plugin].copy()
                           if (hasattr(Manager._plugins[plugin], "copy")) else
                           copy(Manager._plugins[plugin])
                          )

                for module_name in modules:
                    try:
                        old_module = Loader.get_module(module_name)
                        reloaded_module = None

                        if (old_module is not None
                            and hasattr(old_module, "unregister_plugin")
                            and callable(old_module.unregister_plugin)
                           ): old_module.unregister_plugin()

                        try: reloaded_module = Loader.reload(module_name, False)
                        except Exception: Manager._plugins[plugin].remove(module_name)

                        if (reloaded_module is not None
                            and hasattr(reloaded_module, "on_plugin_reloaded")
                            and callable(reloaded_module.on_plugin_reloaded)
                           ): reloaded_module.on_plugin_reloaded()
                    except Exception as handled_exception:
                        if (Manager._log_handler is not None): Manager._log_handler.error(handled_exception, context = "dpt_plugins")
                        _return = False
                    #
                #

                Manager.load_plugin(plugin, "")
            #
        #

        return _return
    #
#
