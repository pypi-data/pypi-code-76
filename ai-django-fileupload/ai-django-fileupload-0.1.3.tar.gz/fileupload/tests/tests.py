import json
import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from fileupload.constants import UPLOADER_UPLOAD_DIRECTORY
from fileupload.models import upload_to
from fileupload.tests.test_utils import build_url
from model_mommy import mommy


class AttachmentListViewTests(TestCase):
    def setUp(self):
        """
        Set up all the tests
        """
        self.user = mommy.make(User)
        self.content_type_user = ContentType.objects.get(model="user")
        self.attachments = mommy.make('fileupload.Attachment',
                                      content_type=self.content_type_user,
                                      object_id=self.user.id,
                                      _create_files=True,
                                      _quantity=3)

    def test_show_all_attachments(self):
        """
        All existent attachments should be retrieved
        """
        response = self.client.get(build_url('upload-view', get={'content_type_id': self.content_type_user.id,
                                                                 'object_id': self.user.id}),
                                   HTTP_ACCEPT='application/json')
        response_files = json.loads(response.content)['files']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_files), len(self.attachments))


class AttachmentUploadToTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mommy.make(User)
        cls.content_type_user = ContentType.objects.get(model="user")
        cls.attachment = mommy.make('fileupload.Attachment',
                                    content_type=cls.content_type_user,
                                    object_id=cls.user.id,
                                    _create_files=True)
        cls.filename = 'test_filename'

    def test_upload_to_default(self):
        self.assertEqual(os.path.dirname(upload_to(self.attachment, self.filename)) + '/', UPLOADER_UPLOAD_DIRECTORY)
        self.assertNotEqual(os.path.basename(upload_to(self.attachment, self.filename)), self.filename)

    @override_settings(UPLOADER_PERSIST_FILENAME=True)
    def test_upload_to_persist_filename(self):
        self.assertEqual(os.path.dirname(upload_to(self.attachment, self.filename)) + '/', UPLOADER_UPLOAD_DIRECTORY)
        self.assertEqual(os.path.basename(upload_to(self.attachment, self.filename)), self.filename)
