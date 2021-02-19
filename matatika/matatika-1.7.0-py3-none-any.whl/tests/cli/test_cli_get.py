"""CLI 'list' command test module"""

# standard
import json
from unittest.mock import patch
import uuid
# local
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI
from tests.api_response_mocks import DATASET


class TestCLIGet(TestCLI):
    """Test class for CLI get command"""

    def test_get_no_subcommmand(self):
        """Test get with no subcommand"""

        result = self.runner.invoke(matatika, ["get"])
        self.assertIn(
            "Usage: matatika get [OPTIONS] COMMAND [ARGS]...", result.output)
        self.assertIs(result.exit_code, 0)

    def test_get_invalid_subcommand(self):
        """Test get with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["get", resource_type])
        self.assertIn(
            f"Error: No such command '{resource_type}'.", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('catalog.requests.get')
    def test_get_dataset(self, mock_get_request):
        """Test get dataset"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = DATASET

        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               str(uuid.uuid4())])

        self.assertIn(json.dumps(DATASET), result.output)
