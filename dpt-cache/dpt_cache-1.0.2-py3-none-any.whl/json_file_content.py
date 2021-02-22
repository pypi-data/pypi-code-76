# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;cache

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.2
dpt_cache/json_file_content.py
"""

# pylint: disable=import-error, no-name-in-module

from dpt_json import JsonResource
from dpt_logging import LogLine
from dpt_runtime.exceptions import ValueException

from .file_content import FileContent

class JsonFileContent(FileContent):
    """
"JsonFileContent" provides access to JSON files on disk or cached.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: cache
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    @staticmethod
    def get(file_path_name, required = False):
        """
Get file content from cache or file.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v1.0.0
        """

        _return = None

        # @TODO: Check if changed and clear AbstractValue if applicable

        file_content = FileContent.get(file_path_name)
        if (file_content is not None): _return = JsonResource.json_to_data(file_content)

        if (_return is None):
            if (required): raise ValueException("{0} is not a valid JSON encoded file".format(file_path_name))
            LogLine.warning("{0} is not a valid JSON encoded file", file_path_name, context = "dpt_cache")
        #

        # @TODO: Use AbstractValue to cache JSON

        return _return
    #
#
