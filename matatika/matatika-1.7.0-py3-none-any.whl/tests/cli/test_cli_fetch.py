"""CLI 'fetch' command test module"""

# standard
import unittest
from unittest.mock import patch
from uuid import uuid4
# local
from matatika.cli.commands.root import matatika
from matatika.context import CONTEXTS
from matatika.exceptions import VariableNotSetError
from tests.cli.test_cli import TestCLI
from tests.api_response_mocks import DATA, DATA_CSV


class TestCLIFetch(TestCLI):
    """Test class for CLI fetch command"""

    def test_fetch_without_dataset_id_or_alias_argument(self):
        """Test fetch without dataset ID or alias argument"""

        result = self.runner.invoke(matatika, ["fetch"])
        self.assertIn(
            "Error: Missing argument 'DATASET_ID_OR_ALIAS'.", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('catalog.requests.get')
    def test_fetch_by_invalid_dataset_id(self, mock_get_request):
        """Test fetch by an invalid dataset ID"""

        mock_get_request.return_value.status_code = 404

        invalid_uuid = str(uuid4())
        result = self.runner.invoke(matatika, ["fetch",
                                               invalid_uuid])
        self.assertIn(
            f"Dataset {invalid_uuid} does not exist within the current authorisation context",
            result.output)

    @patch('catalog.requests.get')
    def test_fetch_by_invalid_alias(self, mock_get_request):
        """Test fetch by an invalid dataset alias"""

        mock_get_request.return_value.status_code = 404

        invalid_alias = 'invalid-alias'
        result = self.runner.invoke(matatika, ["fetch",
                                               invalid_alias,
                                               "-w",
                                               str(uuid4())])
        self.assertIn(
            f"Dataset {invalid_alias} does not exist within the current authorisation context",
            result.output)

    def test_fetch_by_alias_no_workspace_id(self):
        """Test fetch by dataset alias without specifying a workspace ID"""

        self.mock__read_json.return_value[CONTEXTS]['context1']['workspace_id'] = None

        workspace_id_not_set_msg = str(VariableNotSetError('workspace_id'))

        invalid_alias = 'invalid-alias'
        result = self.runner.invoke(matatika, ["fetch",
                                               invalid_alias])
        self.assertIn(workspace_id_not_set_msg, result.output)

    @patch('catalog.requests.get')
    def test_fetch_by_id(self, mock_get_request):
        """Test fetch with dataset ID"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.text = str(DATA)

        result = self.runner.invoke(matatika, ["fetch",
                                               str(uuid4())])
        self.assertIn(str(DATA), result.output)

    @patch('catalog.requests.get')
    def test_fetch_by_alias(self, mock_get_request):
        """Test fetch with dataset ID"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.text = str(DATA)

        result = self.runner.invoke(matatika, ["fetch",
                                               "alias",
                                               "-w",
                                               str(uuid4())])
        self.assertIn(str(DATA), result.output)

    @patch('catalog.requests.get')
    def test_fetch_as_csv(self, mock_get_request):
        """Test fetch with dataset ID"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.text = DATA_CSV

        result = self.runner.invoke(matatika, ["fetch",
                                               str(uuid4()),
                                               "--as",
                                               "csv"])
        self.assertIn(DATA_CSV, result.output)

    @unittest.skip
    @patch('cli.commands.fetch.open')
    @patch('catalog.requests.get')
    def test_fetch_with_output_file_opt(self, mock_get_request, _mock_open):
        """Test fetch with output file option"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.text = str(DATA)

        dataset_id = str(uuid4())

        file_ = "test.txt"
        result = self.runner.invoke(matatika, ["fetch",
                                               dataset_id,
                                               "-f", file_])
        self.assertIn(f"Dataset {dataset_id} data successfully written to {file_}",
                      result.output)
