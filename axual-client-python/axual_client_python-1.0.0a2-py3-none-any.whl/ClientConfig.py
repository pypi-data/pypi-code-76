# -*- coding: utf-8 -*-
#
#      Copyright (C) 2020 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging

from axualclient import SslConfig

logger = logging.getLogger(__name__)


class ClientConfig:

    def __init__(self, endpoint: str, tenant: str, environment: str,
                 application_id: str, ssl_config: SslConfig, version: str = None):
        self._endpoint = endpoint
        self._tenant = tenant
        self._environment = environment
        self._application_id = application_id
        self.ssl_config = ssl_config
        self._version = version
