"""CLI 'profile' command test module"""

from mock import patch
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI
from tests.api_response_mocks import PROFILES


class TestCLIPublish(TestCLI):
    """Test class for CLI profile command"""

    @patch('catalog.requests.get')
    def test_profile(self, mock_get_request):
        """Test profile"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = PROFILES

        result = self.runner.invoke(matatika, ["profile"])

        profile = PROFILES['_embedded']['profiles'][0]

        self.assertIn(profile['id'], result.output)
        self.assertIn(profile['name'], result.output)
