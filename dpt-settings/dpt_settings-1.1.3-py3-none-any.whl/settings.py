# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;settings

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.1.3
dpt_settings/settings.py
"""

# pylint: disable=import-error

from os import path
from weakref import proxy
import os
import re

try: from threading import RLock
except ImportError: RLock = None

try: from appdirs import AppDirs
except ImportError: AppDirs = None

from dpt_file import File
from dpt_json import JsonResource
from dpt_runtime import Binary, Environment, StackedDict
from dpt_runtime.exceptions import IOException, ValueException

class Settings(object):
    """
The settings singleton provides a central configuration facility.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: settings
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_EXTENDED_JSON_COMMENT_LINE = re.compile("^\\s*#.*$", re.M)
    """
Comments in (invalid) JSON setting files are replaced before getting parsed.
    """

    __slots__ = [ "__weakref__", "_file_dict", "_runtime_dict" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _cache_instance = None
    """
Cache instance
    """
    _files = [ ]
    """
Settings files read
    """
    _instance = None
    """
Settings instance
    """
    _lock = (None if (RLock is None) else RLock())
    """
Thread safety lock
    """
    _log_handler = None
    """
The log handler is called whenever debug messages should be logged or errors
happened.
    """

    def __init__(self):
        """
Constructor __init__(Settings)

:since: v1.0.0
        """

        self._file_dict = { }
        """
Underlying file-backed settings dict
        """
        self._runtime_dict = StackedDict()
        """
Runtime settings dict
        """

        self._runtime_dict.add_dict(self._file_dict)
    #

    @property
    def file_dict(self):
        """
Returns the file-backed settings dictionary. This dictionary does not
contain values changed at runtime.

:return: (dict) Underlying file-backed settings dict
:since:  v1.0.0
        """

        return self._file_dict
    #

    @property
    def runtime_dict(self):
        """
Returns the runtime settings dictionary.

:return: (dict) Runtime settings dict
:since:  v1.0.0
        """

        return self._runtime_dict
    #

    def _process_environment(self):
        """
Sets path values in the runtime settings dictionary based on the OS
environment.

:since: v1.0.0
        """

        base_path = Environment.get_base_path()

        if ("path_base" not in self._runtime_dict
            or base_path != self._runtime_dict['path_base']
           ): self._runtime_dict['path_base'] = base_path

        path_data = (Binary.str(os.environ['DPT_PATH_DATA']) if ("DPT_PATH_DATA" in os.environ) else None)

        if (path_data is None and AppDirs is not None):
            app_name = Environment.get_application_short_name()
            app_vendor = Environment.get_application_vendor()

            app_dirs = AppDirs(app_name, app_vendor)
            if (os.access(app_dirs.site_data_dir, (os.R_OK | os.X_OK))): path_data = app_dirs.site_data_dir
        #

        if (path_data is None): path_data = path.join(base_path, "data")

        if (os.access(path_data, (os.R_OK | os.X_OK))):
            self._runtime_dict['path_data'] = path_data
            Settings.read_file("{0}/settings/core.json".format(self._runtime_dict['path_data']))
        #
    #

    def update(self, other):
        """
python.org: Update the dictionary with the key/value pairs from other,
overwriting existing keys.

:param other: Other dictionary

:since: v1.0.0
        """

        self._runtime_dict.update(other)
    #

    def _update_file_dict(self, _dict):
        """
Updates the file-backed settings dict with values from the given one.

:param _dict: Updated dictionary

:since: v1.0.0
        """

        self._file_dict.update(_dict)
    #

    @staticmethod
    def get(key, default = None):
        """
Returns the value with the specified key.

:param key: Settings key
:param default: Default value if not set

:return: (mixed) Value
:since:  v1.0.0
        """

        return Settings.get_dict().get(key, default)
    #

    @staticmethod
    def get_dict():
        """
Returns all settings currently defined as a dict.

:return: (dict) Settings dict
:since:  v1.0.0
        """

        # pylint: disable=protected-access

        return Settings.get_instance().runtime_dict
    #

    @staticmethod
    def get_lang_associated(key, lang, default = None):
        """
Returns the value associated with the given language. Otherwise the default
one with the specified key is returned. Default is used if both values are
not defined.

:param key: Settings key
:param lang: Language code
:param default: Default value if not set

:return: (mixed) Value
:since:  v1.0.0
        """

        _dict = Settings.get_dict()

        key_with_lang = "{0}_{1}".format(key, lang)
        _return = (_dict[key_with_lang] if (key_with_lang in _dict) else None)

        if (_return is None): _return = _dict.get(key, default)

        return _return
    #

    @staticmethod
    def get_instance():
        """
Get the settings singleton.

:return: (Settings) Object on success
:since:  v1.0.0
        """

        if (Settings._instance is None):
            if (Settings._lock is None): Settings._new_instance()
            else:
                with Settings._lock:
                    # Thread safety
                    if (Settings._instance is None): Settings._new_instance()
                #
            #
        #

        return Settings._instance
    #

    @staticmethod
    def _new_instance():
        """
Initializes a new settings singleton instance.

:since: v1.0.0
        """

        # pylint: disable=protected-access

        Settings._instance = Settings()
        Settings._instance._process_environment()
    #

    @staticmethod
    def _import_file_json(json):
        """
Import a given JSON encoded string as an dict of file-backed settings.

:param json: JSON encoded dict of settings

:return: (bool) True on success
:since:  v1.0.0
        """

        # pylint: disable=protected-access

        _return = True

        json_data = JsonResource.json_to_data(json)

        if (json_data is None): _return = False
        else: Settings.get_instance()._update_file_dict(json_data)

        return _return
    #

    @staticmethod
    def is_defined(key):
        """
Checks if a given key is a defined setting.

:param key: Settings key

:return: (bool) True if defined
:since:  v1.0.0
        """

        return (key in Settings.get_dict())
    #

    @staticmethod
    def is_file_known(file_path_name):
        """
Return true if the given file path and name is cached.

:param file_path_name: File path and name of the settings file

:return: (bool) True if currently cached
:since:  v1.0.0
        """

        file_path_name = path.normpath(file_path_name)
        return (file_path_name in Settings._files)
    #

    @staticmethod
    def read_file(file_path_name, required = False):
        """
Read all settings from the given file.

:param file_path_name: File path and name of the settings file
:param required: True if missing files should throw exceptions

:return: (bool) True on success
:since:  v1.0.0
        """

        # pylint: disable=protected-access

        _return = True

        file_path_name = path.normpath(file_path_name)
        file_content = (None if (Settings._cache_instance is None) else Settings._cache_instance.get_from_file(file_path_name))

        if (file_content is None):
            file_object = File()

            if (file_object.open(file_path_name, True, "r")):
                file_content = file_object.read()
                file_object.close()

                if (file_content is not None
                    and Settings._cache_instance is not None
                   ): Settings._cache_instance.set_file(file_path_name, file_content)
            #
        else: file_content = Binary.str(file_content)

        if (file_content is not None):
            file_content = file_content.replace("\r", "")
            file_content = Settings.RE_EXTENDED_JSON_COMMENT_LINE.sub("", file_content)
        #

        if (file_content is None):
            if (required): raise IOException("{0} not found".format(file_path_name))
            if (Settings._log_handler is not None): Settings._log_handler.debug("{0} not found", file_path_name, context = "dpt_settings")

            _return = False
        elif (not Settings._import_file_json(file_content)):
            if (required): raise ValueException("{0} is not a valid JSON encoded settings file".format(file_path_name))
            if (Settings._log_handler is not None): Settings._log_handler.warning("{0} is not a valid JSON encoded settings file", file_path_name, context = "dpt_settings")

            _return = False
        elif (file_path_name not in Settings._files):
            with Settings._lock:
                # Thread safety
                if (file_path_name in Settings._files): Settings._files.append(file_path_name)
            #
        #

        return _return
    #

    @staticmethod
    def _reprocess_environment():
        """
This method should only be called after changing the OS environment to
process it.

:since: v1.0.0
        """

        # pylint: disable=protected-access

        Settings.get_instance()._process_environment()
    #

    @staticmethod
    def set(key, value = None):
        """
Sets the value for the specified key.

:param key: Settings key
:param value: Value

:since: v1.0.0
        """

        Settings.get_dict()[key] = value
    #

    @staticmethod
    def set_cache_instance(cache_instance):
        """
Sets the cache instance.

:param cache_instance: Cache instance to use

:since: v1.0.0
        """

        if (Settings._log_handler is not None): Settings._log_handler.debug("dpt_settings/settings.py -Settings.set_cache_instance()- (421)", context = "dpt_settings")
        Settings._cache_instance = proxy(cache_instance)
    #

    @staticmethod
    def set_log_handler(log_handler):
        """
Sets the log handler.

:param log_handler: Log handler to use

:since: v1.0.0
        """

        # pylint: disable=protected-access

        Settings._log_handler = proxy(log_handler)
    #

    @staticmethod
    def write_file(file_path_name, template_path_name):
        """
Write all settings to the given file using the given template.

:param file_path_name: File path and name of the settings file
:param template_path_name: File path and name of the settings template
       file

:return: (bool) True on success
:since:  v1.0.0
        """

        return False
    #
#
