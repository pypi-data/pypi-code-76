"""CLI 'list' command test module"""

# standard
from unittest.mock import patch
import uuid
# local
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI
from tests.api_response_mocks import (
    DATASETS,
    WORKSPACES
)


class TestCLIList(TestCLI):
    """Test class for CLI list command"""

    def test_list_no_subcommmand(self):
        """Test list with no subcommand"""

        result = self.runner.invoke(matatika, ["list"])
        self.assertIn(
            "Usage: matatika list [OPTIONS] COMMAND [ARGS]...", result.output)
        self.assertIs(result.exit_code, 0)

    def test_list_invalid_subcommand(self):
        """Test list with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["list", resource_type])
        self.assertIn(
            f"Error: No such command '{resource_type}'.", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('catalog.requests.get')
    def test_list_workspaces(self, mock_get_request):
        """Test list workspaces"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = WORKSPACES

        result = self.runner.invoke(matatika, ["list",
                                               "workspaces"])

        workspaces = WORKSPACES['_embedded']['workspaces']
        for workspace in workspaces:
            self.assertIn(workspace['id'], result.output)
            self.assertIn(workspace['name'], result.output)

        self.assertIn(f"Total workspaces: {len(workspaces)}",
                      result.output)

    @patch('catalog.requests.get')
    def test_list_datasets(self, mock_get_request):
        """Test list datasets"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = DATASETS

        result = self.runner.invoke(matatika, ["list",
                                               "datasets",
                                               "-w",
                                               str(uuid.uuid4())])

        datasets = DATASETS['_embedded']['datasets']
        for dataset in datasets:
            self.assertIn(dataset['id'], result.output)
            self.assertIn(dataset['title'], result.output)

        self.assertIn(f"Total datasets: {len(datasets)}",
                      result.output)
