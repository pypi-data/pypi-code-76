"""
Module with API test
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
from test.base_test_context import BaseTestContext
import groupdocsassemblycloud.models.requests
from groupdocsassemblycloud import AssembleOptions, TemplateFileInfo
from groupdocsassemblycloud.models.requests import AssembleDocumentRequest, UploadFileRequest

class TestApi(BaseTestContext):
    """
    Test API class
    """
    test_folder = 'GroupDocs.Assembly'

    def test_assembly(self):
        """Assemble document test

        """
        filename = 'TableFeatures.odt'
        with open(os.path.join(self.local_test_folder, 'TableData.json')) as f:
            data = f.read()
        remote_name = os.path.join(self.remote_test_folder, filename)
        self.uploadFileToStorage(open(os.path.join(self.local_test_folder, filename), 'rb'), remote_name)

        template_file_info = groupdocsassemblycloud.models.TemplateFileInfo(remote_name)
        assemble_data = groupdocsassemblycloud.models.AssembleOptions(template_file_info, "pdf", data)
        request = groupdocsassemblycloud.models.requests.AssembleDocumentRequest(assemble_data)
        result = self.assembly_api.assemble_document(request)
        self.assertTrue(len(result) > 0, 'Error has occurred while building document')

    def test_bug_assembly(self):
        """
        Test assemble document
        """
        filename = 'template.docx'
        # Upload the template
        with open(os.path.join(self.local_test_folder, filename), 'rb') as template_file:
            upload_request = UploadFileRequest(template_file, path='tt.docx')
            self.assembly_api.upload_file(upload_request)

        with open(os.path.join(self.local_test_folder, 'data.json')) as f:
            data = f.read()
        template_file_info = TemplateFileInfo('tt.docx')
        options = AssembleOptions(template_file_info, save_format='docx', report_data=data)
        request = AssembleDocumentRequest(options)
        result = self.assembly_api.assemble_document(request)
        self.assertTrue(len(result) > 0, 'Error has occurred while building document')
