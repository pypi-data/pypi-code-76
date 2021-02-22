# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;mime_type

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.3
dpt_mime_type/mime_type.py
"""

from weakref import ref
import mimetypes

from dpt_cache import JsonFileContent
from dpt_logging import LogLine
from dpt_settings import Settings
from dpt_threading import InstanceLock

class MimeType(object):
    """
Provides mime type related methods on top of Python basic ones.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: mime_type
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "__weakref__", "definitions", "extensions" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _weakref_instance = None
    """
MimeType weakref instance
    """
    _weakref_lock = InstanceLock()
    """
Thread safety weakref lock
    """

    def __init__(self):
        """
Constructor __init__(MimeType)

:since: v1.0.0
        """

        self.definitions = { }
        """
Mime type definitions
        """
        self.extensions = { }
        """
Mime type extension list
        """
    #

    def get(self, extension = None, mimetype = None):
        """
Returns the mime type definition. Either extension or mime type can be
looked up.

:param extension: Extension to look up
:param mimetype: Mime type to look up

:return: (dict) Mime type definition
:since:  v1.0.0
        """

        _return = None

        if (extension is not None):
            extension = (extension[1:].lower() if (extension[:1] == ".") else extension.lower())

            if (extension in self.extensions and self.extensions[extension] in self.definitions):
                _return = self.definitions[self.extensions[extension]]
                if (len(_return) == 1 and "type" in _return): _return = self.definitions[_return['type']]

                if ("type" not in _return): _return['type'] = self.extensions[extension]
            else:
                mimetype = mimetypes.guess_type("file.{0}".format(extension), False)[0]
                if (mimetype is not None): _return = { "type": mimetype, "extension": extension }
            #

            if (mimetype is not None and mimetype != _return['type']): _return = None
        elif (mimetype is not None):
            mimetype = mimetype.lower()

            if (mimetype in self.definitions):
                _return = self.definitions[mimetype]
                if (len(_return) == 1 and "type" in _return): _return = self.definitions[_return['type']]

                if ("type" not in _return): _return['type'] = mimetype
            elif (mimetypes.guess_extension(mimetype, False) is not None): _return = { "type": mimetype }
        #

        if (_return is not None and "class" not in _return): _return['class'] = _return['type'].split("/")[0]

        return _return
    #

    def get_extensions(self, mimetype):
        """
Returns the list of extensions known for the given mime type.

:param mimetype: Mime type to return the extensions for.

:return: (list) Extensions
:since:  v1.0.0
        """

        _return = [ ]

        if (mimetype is not None and mimetype in self.definitions):
            definition = self.get(mimetype = mimetype)
            _return = definition.get("extensions")

            if (type(_return) is not list and "extension" in definition):
                _return = [ definition.get("extension") ]
            #
        #

        return _return
    #

    def refresh(self):
        """
Refresh all mime type definitions from the file.

:since: v1.0.0
        """

        json_data = JsonFileContent.get("{0}/settings/mime_types.json".format(Settings.get("path_data")))

        if (type(json_data) is dict):
            aliases = { }
            self.definitions = { }
            self.extensions = { }

            for mimetype in json_data:
                if ("type" in json_data[mimetype]): aliases[mimetype] = json_data[mimetype]['type']
                else:
                    self.definitions[mimetype] = json_data[mimetype].copy()

                    if ("class" not in json_data[mimetype]):
                        _class = mimetype.split("/", 1)[0]
                        self.definitions[mimetype]['class'] = (_class if (_class not in json_data or "class" not in json_data[_class]) else json_data[_class]['class'])
                    #

                    if (type(json_data[mimetype].get("extensions")) is list):
                        for extension in json_data[mimetype]['extensions']:
                            if (extension not in self.extensions): self.extensions[extension] = mimetype
                            else: LogLine.warning("Extension '{0}' declared for more than one mime type", self.extensions[extension], context = "dpt_mime_type")
                        #
                    elif ("extension" in json_data[mimetype]):
                        if (json_data[mimetype]['extension'] not in self.extensions): self.extensions[json_data[mimetype]['extension']] = mimetype
                        else: LogLine.warning("Extension '{0}' declared for more than one mime type", self.extensions[json_data[mimetype]['extension']], context = "dpt_mime_type")
                    #
                #
            #

            for mimetype in aliases:
                if (mimetype not in self.definitions and aliases[mimetype] in self.definitions):
                    self.definitions[mimetype] = self.definitions[aliases[mimetype]]
                    self.definitions[mimetype]['type'] = aliases[mimetype]
                #
            #
        #
    #

    @staticmethod
    def get_instance():
        """
Get the MimeType singleton.

:return: (MimeType) Object on success
:since:  v1.0.0
        """

        # pylint: disable=not-callable

        _return = None

        with MimeType._weakref_lock:
            if (MimeType._weakref_instance is not None): _return = MimeType._weakref_instance()

            if (_return is None):
                _return = MimeType()
                _return.refresh()

                MimeType._weakref_instance = ref(_return)
            #
        #

        return _return
    #
#
