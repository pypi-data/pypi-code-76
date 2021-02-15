# **************************************************************************** #
#                           This file is part of:                              #
#                                BITSMITHS                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/bitsmiths                             #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #
import os.path

from .xloco import xLoco

from bs_lib import Pod


class Config:
    """
    Class that loads config values on demand from the database. The config values are cached
    for as long as the config is set to.
    """

    def __init__(self, pod: Pod, dao):
        """
        Constructor.

        :param pod: The pod to use.
        :param dao: The dao module to use.
        """
        self._pod       = pod
        self._dao       = dao
        self.cache_time = 60  # min
        self.cache      = {}


    def load(self, values: 'list|str', ignore_missing: bool = False, expand_env_vars: bool = True) -> dict:
        """
        Loads config values and caches them.

        :param values: List of string values to read.
        :param ignore_missing: If true, simply ignores missing parameters.
        :param expand_env_vars: If set to false, won't attempt to expand the env vars.
        :return: The config loaded.
        """
        fc = None

        if type(values) == str:
            values = [values]

        for val in values:
            if self.cache.get(val):
                continue

            if fc is None:
                fc = self._dao.dConfig(self._pod.dbcon)

            if fc.try_select_one_deft(val):
                if expand_env_vars:
                    self.cache[val] = os.path.expandvars(fc.rec.value)
                else:
                    self.cache[val] = fc.rec.value
            else:
                if not ignore_missing:
                    raise xLoco('Config setting not found [%s]' % val)

        return self.cache


    def read(self, value: str, expand_env_vars=True):
        """
        Reads a single value from the config.

        :param value: (string) The config value to read.
        :return: (string) The value.
        """
        val = self.cache.get(value)

        if val is None:
            self.load(value, False, expand_env_vars)

        return self.cache[value]
