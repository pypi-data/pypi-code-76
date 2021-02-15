# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from typing import Union
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.options import ArgOptions


class Log(object):
    def __init__(self):
        self.level = None

    def to_capabilities(self) -> dict:
        if self.level:
            return {"log": {"level": self.level}}
        return {}


class Options(ArgOptions):
    KEY = "moz:firefoxOptions"

    def __init__(self):
        super(Options, self).__init__()
        self._binary: FirefoxBinary = None
        self._preferences: dict = {}
        self._profile = None
        self._proxy = None
        self.log = Log()

    @property
    def binary(self) -> FirefoxBinary:
        """Returns the FirefoxBinary instance"""
        return self._binary

    @binary.setter
    def binary(self, new_binary: Union[str, FirefoxBinary]):
        """Sets location of the browser binary, either by string or
        ``FirefoxBinary`` instance.

        """
        if not isinstance(new_binary, FirefoxBinary):
            new_binary = FirefoxBinary(new_binary)
        self._binary = new_binary

    @property
    def binary_location(self) -> str:
        """
        :Returns: The location of the binary.
        """
        return self.binary._start_cmd

    @binary_location.setter  # noqa
    def binary_location(self, value: str):
        """ Sets the location of the browser binary by string """
        self.binary = value

    @property
    def accept_insecure_certs(self) -> bool:
        return self._caps.get('acceptInsecureCerts')

    @accept_insecure_certs.setter
    def accept_insecure_certs(self, value: bool):
        self._caps['acceptInsecureCerts'] = value

    @property
    def preferences(self) -> dict:
        """:Returns: A dict of preferences."""
        return self._preferences

    def set_preference(self, name: str, value: Union[str, int, bool]):
        """Sets a preference."""
        self._preferences[name] = value

    @property
    def proxy(self) -> Proxy:
        """
        :Returns: Proxy if set, otherwise None.
        """
        return self._proxy

    @proxy.setter
    def proxy(self, value: Proxy):
        if not isinstance(value, Proxy):
            raise InvalidArgumentException("Only Proxy objects can be passed in.")
        self._proxy = value

    @property
    def profile(self) -> FirefoxProfile:
        """
        :Returns: The Firefox profile to use.
        """
        return self._profile

    @profile.setter
    def profile(self, new_profile: Union[str, FirefoxProfile]):
        """Sets location of the browser profile to use, either by string
        or ``FirefoxProfile``.

        """
        if not isinstance(new_profile, FirefoxProfile):
            new_profile = FirefoxProfile(new_profile)
        self._profile = new_profile

    @property
    def headless(self) -> bool:
        """
        :Returns: True if the headless argument is set, else False
        """
        return '-headless' in self._arguments

    @headless.setter
    def headless(self, value: bool):
        """
        Sets the headless argument

        Args:
          value: boolean value indicating to set the headless option
        """
        if value:
            self._arguments.append('-headless')
        elif '-headless' in self._arguments:
            self._arguments.remove('-headless')

    @property
    def page_load_strategy(self) -> str:
        return self._caps["pageLoadStrategy"]

    @page_load_strategy.setter
    def page_load_strategy(self, strategy: str):
        if strategy in ["normal", "eager", "none"]:
            self.set_capability("pageLoadStrategy", strategy)
        else:
            raise ValueError("Strategy can only be one of the following: normal, eager, none")

    def to_capabilities(self) -> dict:
        """Marshals the Firefox options to a `moz:firefoxOptions`
        object.
        """
        # This intentionally looks at the internal properties
        # so if a binary or profile has _not_ been set,
        # it will defer to geckodriver to find the system Firefox
        # and generate a fresh profile.
        caps = self._caps
        opts = {}

        if self._binary:
            opts["binary"] = self._binary._start_cmd
        if self._preferences:
            opts["prefs"] = self._preferences
        if self._proxy:
            self._proxy.add_to_capabilities(caps)
        if self._profile:
            opts["profile"] = self._profile.encoded
        if self._arguments:
            opts["args"] = self._arguments

        opts.update(self.log.to_capabilities())

        if opts:
            caps[Options.KEY] = opts

        return caps

    @property
    def default_capabilities(self) -> dict:
        return DesiredCapabilities.FIREFOX.copy()
