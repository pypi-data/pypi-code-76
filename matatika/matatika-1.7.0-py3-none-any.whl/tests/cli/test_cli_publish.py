"""CLI 'publish' command test module"""

# standard
from pathlib import Path
import json
import uuid
# external
from unittest.mock import Mock, patch
# local
from matatika.cli.commands.root import matatika
from matatika.dataset import Dataset
from tests.cli.test_cli import TestCLI


class TestCLIPublish(TestCLI):
    """Test class for CLI publish command"""

    def test_publish_without_dataset_file_arg(self):
        """Test publish without dataset file argument"""

        result = self.runner.invoke(matatika, ["publish"])
        self.assertIn("Error: Missing argument 'DATASET_FILE'.", result.output)
        self.assertIs(result.exit_code, 2)

    def test_publish_with_invalid_dataset_file_arg(self):
        """Test publish with invalid dataset file argument"""

        invalid_path = "invalid-path"

        result = self.runner.invoke(matatika, ["publish",
                                               invalid_path])
        self.assertIn(f"Invalid value for 'DATASET_FILE': Path '{invalid_path}' does "
                      "not exist", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('catalog.requests.post')
    def test_publish_yml_yaml(self, mock_post: Mock):
        """Test publish with a .yml or .yaml file"""

        package_dir = Path(__file__).parent.parent.absolute()
        file_path = package_dir.joinpath('test_data/helloworld.yaml')

        mock_post.side_effect = _mock_response

        result = self.runner.invoke(matatika, ["publish",
                                               str(file_path)])

        print(result.output)

        input_datasets = [Dataset.from_dict(json.loads(
            arg[1]['data'])) for arg in mock_post.call_args_list]

        self.assertIn(f"Successfully published {len(input_datasets)} dataset(s)",
                      result.output)

        for dataset in input_datasets:
            self.assertIn(dataset.alias, result.output)
            self.assertIn(dataset.title, result.output)

    @patch('catalog.requests.post')
    def test_publish_ipynb_with_headings(self, mock_post: Mock):
        """Test publish with a .ipynb file containing headings"""

        package_dir = Path(__file__).parent.parent.absolute()
        file_path = package_dir.joinpath('test_data/test_notebook.ipynb')

        mock_post.side_effect = _mock_response

        result = self.runner.invoke(matatika, ["publish",
                                               str(file_path)])

        print(result.output)

        input_datasets = [Dataset.from_dict(json.loads(
            arg[1]['data'])) for arg in mock_post.call_args_list]

        self.assertIn(f"Successfully published {len(input_datasets)} dataset(s)",
                      result.output)

        for dataset in input_datasets:
            self.assertIn(dataset.dataset_id, result.output)
            self.assertIn(dataset.title, result.output)

    @patch('catalog.requests.post')
    def test_publish_ipynb_with_no_headings(self, mock_post: Mock):
        """Test publish with a .ipynb file containing no headings"""

        package_dir = Path(__file__).parent.parent.absolute()
        file_path = package_dir.joinpath(
            'test_data/test_notebook_no_headings.ipynb')

        mock_post.side_effect = _mock_response

        result = self.runner.invoke(matatika, ["publish",
                                               str(file_path)])

        print(result.output)

        input_datasets = [Dataset.from_dict(json.loads(
            arg[1]['data'])) for arg in mock_post.call_args_list]

        self.assertIn(f"Successfully published {len(input_datasets)} dataset(s)",
                      result.output)

        for dataset in input_datasets:
            self.assertIn(dataset.dataset_id, result.output)
            self.assertIn(dataset.title, result.output)


def _mock_response(*_args, **kwargs):

    dataset_dict = json.loads(kwargs['data'])

    if not dataset_dict.get('id'):
        dataset_dict['id'] = str(uuid.uuid4())

    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = dataset_dict

    return mock_response
