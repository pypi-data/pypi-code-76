"""Base CLI test module"""

# standard
import copy
from unittest import TestCase
from unittest.mock import patch
# external
from click.testing import CliRunner
# local
from matatika.context import DEFAULT, CONTEXTS

MOCK_CONTEXTS_JSON = {
    DEFAULT: 'context1',
    CONTEXTS: {
        'context1': {
            'auth_token': 'context1_auth_token',
            'endpoint_url': 'context1_endpoint_url',
            'workspace_id': 'context1_workspace_id'
        },
        'context2': {
            'auth_token': 'context2_auth_token',
            'endpoint_url': 'context2_endpoint_url',
            'workspace_id': 'context2_workspace_id'
        },
        'context3': {
            'auth_token': 'context3_auth_token',
            'endpoint_url': 'context3_endpoint_url',
            'workspace_id': 'context3_workspace_id'
        }
    }
}


class TestCLI(TestCase):
    """Test class for CLI"""

    def setUp(self):

        super().setUp()

        mock__read_json = patch(
            'matatika.context.MatatikaContext._read_json')
        self.mock__read_json = mock__read_json.start()
        self.mock__read_json.return_value = copy.deepcopy(MOCK_CONTEXTS_JSON)
        self.addCleanup(mock__read_json.stop)

        mock__write_json = patch(
            'matatika.context.MatatikaContext._write_json')
        self.mock__write_json = mock__write_json.start()
        self.addCleanup(mock__write_json.stop)

        # instantiate a cli runner
        self.runner = CliRunner()
