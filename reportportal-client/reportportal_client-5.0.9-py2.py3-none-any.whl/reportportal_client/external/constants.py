"""This module contains constants for the external services.

Copyright (c) 2020 http://reportportal.io .

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64


def _decode_string(text):
    """Decode value of the given string.

    :param text: Encoded string
    :return:     Decoded value
    """
    base64_bytes = text.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')


GA_INSTANCE = _decode_string('VUEtMTczNDU2ODA5LTE=')
GA_ENDPOINT = 'https://www.google-analytics.com/collect'
