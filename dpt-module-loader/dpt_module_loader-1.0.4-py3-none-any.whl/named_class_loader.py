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
dpt_module_loader/named_class_loader.py
"""

import re

from .class_loader import ClassLoader

class NamedClassLoader(ClassLoader):
    """
"NamedClassLoader" provides singletons and objects based on a callable
common name.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: module_loader
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_CAMEL_CASE_SPLITTER = re.compile("([A-Z]+|[a-z0-9])([A-Z])(?!$)")
    """
CamelCase splitter RegExp
    """
    RE_NON_WORD_CAMEL_CASE_SPLITTER = re.compile("[^a-zA-Z0-9]+")
    """
CamelCase generation RegExp
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    @staticmethod
    def get_camel_case_class_name(name):
        """
Returns the class name in camel case for the given name.

:param name: Class name like "example_class_name"

:return: (str) Class name in camel case
:since:  v1.0.0
        """

        return "".join([ word.capitalize() for word in NamedClassLoader.RE_NON_WORD_CAMEL_CASE_SPLITTER.split(name) ])
    #

    @staticmethod
    def get_class(common_name, autoload = True):
        """
Get the class name for the given common name.

:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (object) Loaded class; None on error
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.get_class(_class, autoload)
    #

    @staticmethod
    def get_class_from_common_name(common_name):
        """
Returns the package, module and class name for the common one.

:param common_name: Common name like "dpt_module_loader.ClassLoader"

:return: (str) Package, module and class name
:since:  v1.0.0
        """

        _return = None

        common_name_data = common_name.rsplit(".", 1)
        module_name = NamedClassLoader.RE_CAMEL_CASE_SPLITTER.sub("\\1_\\2", common_name_data[-1]).lower()

        return ("{0}:{1}".format(module_name, common_name_data[0])
                if (len(common_name_data) < 2) else
                "{0}.{1}:{2}".format(common_name_data[0], module_name, common_name_data[1])
               )
    #

    @staticmethod
    def get_class_in_namespace(namespace_package, common_name, autoload = True):
        """
Get the class name for the given namespace package and common name.

:param namespace_package: Namespace package name
:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (object) Loaded class; None on error
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.get_class_in_namespace(namespace_package, _class, autoload)
    #

    @staticmethod
    def get_instance(common_name, required = True, **kwargs):
        """
Returns a new instance based on its common name.

:param common_name: Common name
:param required: True if exceptions should be thrown if the class is not
                 defined.
:param autoload: True to load the class automatically if not done already

:return: (object) Requested object on success
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.get_instance(_class, required, **kwargs)
    #

    @staticmethod
    def get_instance_in_namespace(namespace_package, common_name, required = True, **kwargs):
        """
Returns a new instance based on the specified namespace package and common
name.

:param namespace_package: Namespace package name
:param common_name: Common name
:param required: True if exceptions should be thrown if the class is not
                 defined.

:return: (object) Requested object on success
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.get_instance_in_namespace(namespace_package, _class, required, **kwargs)
    #

    @staticmethod
    def get_singleton(common_name, required = True, **kwargs):
        """
Returns a singleton based on its common name.

:param common_name: Common name
:param required: True if exceptions should be thrown if the class is not
                 defined.

:return: (object) Requested object on success
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.get_singleton(_class, required, **kwargs)
    #

    @staticmethod
    def is_defined(common_name, autoload = True):
        """
Checks if a common name is defined or can be resolved to a class name.

:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.is_defined(_class, autoload)
    #

    @staticmethod
    def is_defined_in_namespace(namespace_package, common_name, autoload = True):
        """
Checks if the specified class located in the specified namespace, package
and module name is defined or can be resolved after auto loading it.

:param namespace_package: Namespace package name
:param common_name: Common name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.is_defined_in_namespace(namespace_package, _class, autoload)
    #

    @staticmethod
    def reload(common_name, clear_caches = True):
        """
Reloads the the specified package module.

:param common_name: Common name
:param clear_caches: True to clear import caches before reloading

:return: (object) Reloaded module on success
:since:  v1.0.0
        """

        _class = NamedClassLoader.get_class_from_common_name(common_name)
        return ClassLoader.reload(_class, clear_caches)
    #
#
