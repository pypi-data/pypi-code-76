"""Base library test module"""

from unittest import TestCase
from matatika.library import MatatikaClient


class TestLibrary(TestCase):
    """Test class for library"""

    def setUp(self):

        super().setUp()

        auth_token = 'auth-token'
        endpoint_url = 'endpoint-url'
        workspace_id = 'workspace-id'
        self.client = MatatikaClient(auth_token, endpoint_url, workspace_id)
