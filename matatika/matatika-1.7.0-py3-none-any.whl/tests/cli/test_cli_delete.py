"""CLI 'delete' command test module"""

# standard
from unittest.mock import patch, Mock
from uuid import uuid4
# pip
from requests.models import Response
# local
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI


class TestCLIDelete(TestCLI):
    """Test class for CLI delete command"""

    def test_delete_no_subcommand(self):
        """Test delete with no subcommand"""

        result = self.runner.invoke(matatika, ["delete"])

        expected_message = "Usage: matatika delete [OPTIONS] COMMAND [ARGS]..."
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 0)

    def test_delete_invalid_subcommand(self):
        """Test delete with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["delete", resource_type])

        expected_message = f"Error: No such command '{resource_type}'."
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 2)


class TestCLIDeleteWorkspace(TestCLI):
    """Test class for CLI delete workspace command"""

    def test_delete_workspace_no_argument(self):
        """Test command error when workspace ID argument is not provided"""

        result = self.runner.invoke(matatika, ["delete",
                                               "workspace"])

        expected_message = "Missing argument 'WORKSPACE_ID'"
        self.assertIn(expected_message, result.output)

    def test_delete_workspace_confirm_no(self):
        """Test workspace is not deleted after rejected client confirmation"""

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspace",
                                               workspace_id], input='n')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: n"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('catalog.requests.delete')
    def test_delete_workspace_confirm_yes(self, mock_delete_request: Mock):
        """Test workspace is deleted after client confirmation"""

        mock_delete_request.return_value.status_code = 204

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspace",
                                               workspace_id], input='y')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: y"
        self.assertIn(expected_message, result.output)

        expected_message = f"Successfully deleted workspace {workspace_id}"
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 0)

    @patch('catalog.requests.delete')
    def test_delete_workspace_bypass_confirm(self, mock_delete_request: Mock):
        """Test workspace is deleted with no client confirmation"""

        mock_delete_request.return_value.status_code = 204

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "workspace",
                                               workspace_id])

        expected_message = f"Successfully deleted workspace {workspace_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('catalog.requests.delete')
    def test_delete_workspace_not_found(self, mock_delete_request: Mock):
        """Test workspace is not found when trying to delete"""

        mock_delete_request.return_value.status_code = 404

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspace",
                                               workspace_id], input='y')

        expected_message = f"Workspace {workspace_id} does not exist within the current " \
            "authorisation context"
        self.assertIn(expected_message, result.output)

    @patch('catalog.requests.delete')
    def test_delete_workspace_server_error(self, mock_delete_request: Mock):
        """Test server error encountered when trying to delete workspace"""

        mock_response = Response()
        mock_response.status_code = 503
        mock_delete_request.return_value = mock_response

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspace",
                                               workspace_id], input='y')

        expected_message = f"{mock_response.status_code} Server Error"
        self.assertIn(expected_message, result.output)


class TestCLIDeleteDataset(TestCLI):
    """Test class for CLI delete dataset command"""

    def test_delete_dataset_no_argument(self):
        """Test command error when dataset ID argument is not provided"""

        result = self.runner.invoke(matatika, ["delete",
                                               "dataset"])

        expected_message = "Missing argument 'DATASET_ID'"
        self.assertIn(expected_message, result.output)
        self.assertIs(result.exit_code, 2)

    def test_delete_dataset_confirm_no(self):
        """Test dataset is not deleted after rejected client confirmation"""

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "dataset",
                                               dataset_id], input='n')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: n"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('catalog.requests.delete')
    def test_delete_dataset_confirm_yes(self, mock_delete_request: Mock):
        """Test dataset is deleted after client confirmation"""

        mock_delete_request.return_value.status_code = 204

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "dataset",
                                               dataset_id], input='y')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: y"
        self.assertIn(expected_message, result.output)

        expected_message = f"Successfully deleted dataset {dataset_id}"
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 0)

    @patch('catalog.requests.delete')
    def test_delete_dataset_bypass_confirm(self, mock_delete_request: Mock):
        """Test dataset is deleted with no client confirmation"""

        mock_delete_request.return_value.status_code = 204

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "dataset",
                                               dataset_id])

        expected_message = f"Successfully deleted dataset {dataset_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('catalog.requests.delete')
    def test_delete_dataset_not_found(self, mock_delete_request: Mock):
        """Test dataset is not found when trying to delete"""

        mock_delete_request.return_value.status_code = 404

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "dataset",
                                               dataset_id], input='y')

        expected_message = f"Dataset {dataset_id} does not exist within the current " \
            "authorisation context"
        self.assertIn(expected_message, result.output)

    @patch('catalog.requests.delete')
    def test_delete_dataset_server_error(self, mock_delete_request: Mock):
        """Test server error encountered when trying to delete dataset"""

        mock_response = Response()
        mock_response.status_code = 503
        mock_delete_request.return_value = mock_response

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "dataset",
                                               dataset_id], input='y')

        expected_message = f"{mock_response.status_code} Server Error"
        self.assertIn(expected_message, result.output)
