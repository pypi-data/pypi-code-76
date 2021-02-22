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
dpt_module_loader/class_loader.py
"""

from dpt_runtime.exceptions import IOException, TypeException

from .loader import Loader

class ClassLoader(Loader):
    """
"ClassLoader" provides singletons and objects based on the package, module
and class name given as "package.module:Class".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: module_loader
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "__weakref__", "config" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _instance = None
    """
"Loader" weakref instance
    """

    def __init__(self):
        """
Constructor __init__(ClassLoader)

:since: v1.0.0
        """

        self.config = { }
        """
Underlying configuration array
        """
    #

    def get(self, _class):
        """
Returns the registered class name if applicable.

:param _class: Package, module and class name

:return: (str) Registered class name
:since:  v1.0.0
        """

        return self.config.get(_class)
    #

    def is_registered(self, _class):
        """
Checks if a given class is known.

:param _class: Package, module and class name

:return: (bool) True if defined
:since:  v1.0.0
        """

        return (_class in self.config)
    #

    def register(self, _class, registered_class):
        """
Registers an alternative class for the specified package, module and class
name.

:param _class: Package, module and class name
:param registered_class: Alternative class

:since: v1.0.0
        """

        self.config[_class] = registered_class
    #

    def unregister(self, _class):
        """
Unregisters an alternative class for the specified package, module and class
name.

:param _class: Package, module and class name

:since: v1.0.0
        """

        if (_class in self.config):
            with ClassLoader._lock:
                # Thread safety
                if (_class in self.config): del(self.config[_class])
            #
        #
    #

    @staticmethod
    def get_class(_class, autoload = True):
        """
Get the class for the specified package, module and class name.

:param _class: Package, module and class name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (object) Loaded class; None on error
:since:  v1.0.0
        """

        loader = ClassLoader.get_class_loader_instance()
        if (loader.is_registered(_class)): _class = loader.get(_class)

        class_data = _class.rsplit(":", 1)
        if (len(class_data) < 2): raise IOException("Class '{0}' given is invalid".format(_class))

        class_name = class_data[1]
        module = Loader.get_module(class_data[0], autoload)

        return (None if (module is None) else getattr(module, class_name, None))
    #

    @staticmethod
    def get_class_in_namespace(namespace_package, _class, autoload = True):
        """
Get the class located in the specified namespace, package and module name.

:param namespace_package: Namespace package name
:param _class: Package, module and class name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (object) Loaded class; None on error
:since:  v1.0.0
        """

        class_data = _class.rsplit(":", 1)
        if (len(class_data) < 2): raise IOException("Class '{0}' given is invalid".format(_class))

        class_name = class_data[1]
        module = Loader.get_module_in_namespace(namespace_package, class_data[0], autoload)

        return (None if (module is None) else getattr(module, class_name, None))
    #

    @classmethod
    def get_class_loader_instance(cls):
        """
Get the loader instance.

:param cls: Python class

:return: (object) Loader instance
:since:  v1.0.0
        """

        if (ClassLoader._instance is None):
            with ClassLoader._lock:
                # Thread safety
                if (ClassLoader._instance is None): ClassLoader._instance = ClassLoader()
            #
        #

        return ClassLoader._instance
    #

    @staticmethod
    def get_instance(_class, required = True, **kwargs):
        """
Returns a new instance based on the specified package, module and class
name.

:param _class: Package, module and class name
:param required: True if exceptions should be thrown if the class is not
                 defined.

:return: (object) Requested object on success
:since:  v1.0.0
        """

        _return = None

        instance_class = ClassLoader.get_class(_class)

        if (instance_class is not None and issubclass(instance_class, object)): _return = instance_class(**kwargs)
        if (_return is None and required): raise IOException("Class '{0}' is not defined".format(_class))

        return _return
    #

    @staticmethod
    def get_instance_in_namespace(namespace_package, _class, required = True, **kwargs):
        """
Returns a new instance based on the specified namespace, package and module
name.

:param namespace_package: Namespace package name
:param _class: Package, module and class name
:param required: True if exceptions should be thrown if the class is not
                 defined.

:return: (object) Requested object on success
:since:  v1.0.0
        """

        _return = None

        instance_class = ClassLoader.get_class_in_namespace(namespace_package, _class)

        if (instance_class is not None and issubclass(instance_class, object)): _return = instance_class(**kwargs)
        if (_return is None and required): raise IOException("Class '{0}' is not defined".format(_class))

        return _return
    #

    @staticmethod
    def get_singleton(_class, required = True, **kwargs):
        """
Returns a singleton based on the specified package, module and class name.

:param _class: Package, module and class name
:param required: True if exceptions should be thrown if the class is not
                 defined.

:return: (object) Requested object on success
:since:  v1.0.0
        """

        _return = None

        singleton_class = ClassLoader.get_class(_class)

        if (singleton_class is None and required): raise IOException("Class '{0}' is not defined".format(_class))

        if (hasattr(singleton_class, "get_instance")
            and callable(singleton_class.get_instance)
           ): _return = singleton_class.get_instance(**kwargs)
        elif (required): raise TypeException("{0} has not defined a singleton".format(_class))

        return _return
    #

    @staticmethod
    def is_defined(_class, autoload = True):
        """
Checks if the specified package, module and class name is defined or can be
resolved after auto loading it.

:param _class: Package, module and class name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v1.0.0
        """

        return (ClassLoader.get_class(_class, autoload) is not None)
    #

    @staticmethod
    def is_defined_in_namespace(namespace_package, _class, autoload = True):
        """
Checks if the specified class located in the specified namespace, package
and module name is defined or can be resolved after auto loading it.

:param namespace_package: Namespace package name
:param _class: Package, module and class name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v1.0.0
        """

        return (ClassLoader.get_class_in_namespace(namespace_package, _class, autoload) is not None)
    #

    @staticmethod
    def reload(_class, clear_caches = True):
        """
Reloads the the specified package module.

:param _class: Package, module and optional class name
:param clear_caches: True to clear import caches before reloading

:return: (object) Reloaded module on success
:since:  v1.0.0
        """

        loader = ClassLoader.get_class_loader_instance()
        if (loader.is_registered(_class)): _class = loader.get(_class)

        class_data = _class.rsplit(":", 1)
        return Loader.reload((_class if (len(class_data) < 2) else class_data[0]), clear_caches)
    #
#
