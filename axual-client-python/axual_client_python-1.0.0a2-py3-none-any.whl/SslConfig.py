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
import os

logger = logging.getLogger(__name__)


class SslConfig:

    def __init__(self, certificate_location: str, private_key_location: str, root_ca_location: str):

        if not os.path.exists(certificate_location):
            raise FileNotFoundError(f"{certificate_location} not found!")
        self.certificate_location = certificate_location

        if not os.path.exists(private_key_location):
            raise FileNotFoundError(f"{private_key_location} not found!")
        self.private_key_location = private_key_location

        if not os.path.exists(root_ca_location):
            raise FileNotFoundError(f"{root_ca_location} not found!")
        self.root_ca_location = root_ca_location
