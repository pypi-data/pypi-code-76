"""
Base context for testing
"""
#
# --------------------------------------------------------------------------------------------------------------------
# <copyright company="GroupDocs" file="base_test_context.py">
#   Copyright (c) 2019 GroupDocs.Assembly for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# --------------------------------------------------------------------------------------------------------------------
#

import os
import json
import unittest
import warnings
import six
import groupdocsassemblycloud
from groupdocsassemblycloud.models import requests

class BaseTestContext(unittest.TestCase):
    """
    Base class for all test classes
    """
    def setUp(self):
        root_path = os.path.abspath(os.path.realpath(os.path.dirname(__file__)) + "/..")
        self.local_test_folder = os.path.join(root_path, 'TestData')
        self.remote_test_folder = os.path.join('Temp', 'SdkTests', 'python')
        self.remote_test_out = os.path.join('Temp', 'SdkTests', 'python', 'TestOut')
        self.local_common_folder = os.path.join(self.local_test_folder, 'Common')
        with open(os.path.join(root_path, 'Settings', 'servercreds.json')) as f:
            creds = json.loads(f.read())
        self.assembly_api = groupdocsassemblycloud.AssemblyApi(creds['AppSid'], creds['AppKey'])
        self.assembly_api.api_client.configuration.host = creds['BaseUrl']
        if six.PY3:
            warnings.simplefilter("ignore", ResourceWarning)

    def uploadFileToStorage(self, file, path):
        upload_request = requests.UploadFileRequest(file, path)
        self.assembly_api.upload_file(upload_request)
