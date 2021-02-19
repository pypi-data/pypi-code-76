"""Dataset test module"""

import sys
import unittest
from matatika.dataset import Dataset

sys.path.append('../src/')


class TestDataset(unittest.TestCase):
    """Test class for dataset operations"""

    def test_dataset_attrs(self):
        """Test dataset attributes"""

        dataset = Dataset()

        self.assertIsNone(dataset.dataset_id)
        self.assertIsNone(dataset.alias)
        self.assertIsNone(dataset.workspace_id)
        self.assertIsNone(dataset.title)
        self.assertIsNone(dataset.description)
        self.assertIsNone(dataset.questions)
        self.assertIsNone(dataset.raw_data)
        self.assertIsNone(dataset.visualisation)
        self.assertIsNone(dataset.metadata)
        self.assertIsNone(dataset.query)

        dataset_id = 'dataset-id'
        alias = 'alias'
        workspace_id = 'workspace-id'
        title = 'title'
        description = 'description'
        questions = 'questions'
        raw_data = 'raw-data'
        visualisation = 'visualisation'
        metadata = 'metadata'
        query = 'query'

        dataset.dataset_id = dataset_id
        dataset.alias = alias
        dataset.workspace_id = workspace_id
        dataset.title = title
        dataset.description = description
        dataset.questions = questions
        dataset.raw_data = raw_data
        dataset.visualisation = visualisation
        dataset.metadata = metadata
        dataset.query = query

        self.assertEqual(dataset.dataset_id, dataset_id)
        self.assertEqual(dataset.alias, alias)
        self.assertEqual(dataset.workspace_id, workspace_id)
        self.assertEqual(dataset.title, title)
        self.assertEqual(dataset.description, description)
        self.assertEqual(dataset.questions, questions)
        self.assertEqual(dataset.raw_data, raw_data)
        self.assertEqual(dataset.visualisation, visualisation)
        self.assertEqual(dataset.metadata, metadata)
        self.assertEqual(dataset.query, query)

    def test_to_dict_all_attrs(self):
        """Tests to_dict behaviour with all attributes"""

        dataset = Dataset()
        dataset.dataset_id = 'dataset-id'
        dataset.alias = 'alias'
        dataset.workspace_id = 'workspace-id'
        dataset.title = 'title'
        dataset.description = 'description'
        dataset.questions = 'questions'
        dataset.raw_data = 'raw-data'
        dataset.visualisation = 'visualisation'
        dataset.metadata = 'metadata'
        dataset.query = 'query'

        dataset_dict = {
            'id': dataset.dataset_id,
            'alias': dataset.alias,
            'workspaceId': dataset.workspace_id,
            'title': dataset.title,
            'description': dataset.description,
            'questions': dataset.questions,
            'rawData': dataset.raw_data,
            'visualisation': dataset.visualisation,
            'metadata': dataset.metadata,
            'query': dataset.query
        }

        self.assertDictEqual(dataset.to_dict(), dataset_dict)

    def test_to_dict_partial_attrs(self):
        """Tests to_dict behaviour with partial attributes"""

        dataset = Dataset()
        dataset.alias = 'alias'

        dataset_dict = {
            'alias': dataset.alias
        }

        self.assertDictEqual(dataset.to_dict(), dataset_dict)

    def test_to_dict_no_attrs(self):
        """Tests to_dict behaviour with no attributes"""

        dataset = Dataset()

        dataset_dict = {}

        self.assertDictEqual(dataset.to_dict(), dataset_dict)

    def test_to_json_str_all_attrs(self):
        """Tests to_json_str behaviour with all attributes"""

        dataset = Dataset()
        dataset.dataset_id = 'dataset-id'
        dataset.alias = 'alias'
        dataset.workspace_id = 'workspace-id'
        dataset.title = 'title'
        dataset.description = 'description'
        dataset.questions = 'questions'
        dataset.raw_data = 'raw-data'
        dataset.visualisation = 'visualisation'
        dataset.metadata = 'metadata'
        dataset.query = 'query'

        dataset_json_str = \
            '{' \
            f'"id": "{dataset.dataset_id}", ' \
            f'"alias": "{dataset.alias}", ' \
            f'"workspaceId": "{dataset.workspace_id}", ' \
            f'"title": "{dataset.title}", ' \
            f'"description": "{dataset.description}", ' \
            f'"questions": "{dataset.questions}", ' \
            f'"rawData": "{dataset.raw_data}", ' \
            f'"visualisation": "{dataset.visualisation}", ' \
            f'"metadata": "{dataset.metadata}", ' \
            f'"query": "{dataset.query}"' \
            '}'

        self.assertEqual(dataset.to_json_str(), dataset_json_str)

    def test_to_json_str_partial_attrs(self):
        """Tests to_json_str behaviour with partial attributes"""

        dataset = Dataset()
        dataset.alias = 'alias'

        dataset_json_str = \
            '{' \
            f'"alias": "{dataset.alias}"' \
            '}'

        self.assertEqual(dataset.to_json_str(), dataset_json_str)

    def test_to_json_str_no_attrs(self):
        """Tests to_json_str behaviour with no attributes"""

        dataset = Dataset()

        dataset_json_str = '{}'

        self.assertEqual(dataset.to_json_str(), dataset_json_str)

    def test_from_dict_all_attrs(self):
        """Tests from_dict behaviour with all attributes"""

        dataset_dict = {
            'id': 'id',
            'alias': 'alias',
            'workspaceId': 'workspace-id',
            'title': 'title',
            'description': 'description',
            'questions': 'questions',
            'rawData': 'raw-data',
            'visualisation': 'visualisation',
            'metadata': 'metadata',
            'query': 'query'
        }

        dataset = Dataset.from_dict(dataset_dict)

        self.assertEqual(dataset.dataset_id, dataset_dict['id'])
        self.assertEqual(dataset.alias, dataset_dict['alias'])
        self.assertEqual(dataset.workspace_id, dataset_dict['workspaceId'])
        self.assertEqual(dataset.title, dataset_dict['title'])
        self.assertEqual(dataset.description, dataset_dict['description'])
        self.assertEqual(dataset.questions, dataset_dict['questions'])
        self.assertEqual(dataset.raw_data, dataset_dict['rawData'])
        self.assertEqual(dataset.visualisation, dataset_dict['visualisation'])
        self.assertEqual(dataset.metadata, dataset_dict['metadata'])
        self.assertEqual(dataset.query, dataset_dict['query'])

    def test_from_dict_partial_attrs(self):
        """Tests from_dict behaviour with partial attributes"""

        dataset_dict = {
            'alias': 'alias'
        }

        dataset = Dataset.from_dict(dataset_dict)

        self.assertIsNone(dataset.dataset_id)
        self.assertEqual(dataset.alias, dataset_dict['alias'])
        self.assertIsNone(dataset.workspace_id)
        self.assertIsNone(dataset.title)
        self.assertIsNone(dataset.description)
        self.assertIsNone(dataset.questions)
        self.assertIsNone(dataset.raw_data)
        self.assertIsNone(dataset.visualisation)
        self.assertIsNone(dataset.metadata)
        self.assertIsNone(dataset.query)

    def test_from_dict_no_attrs(self):
        """Tests from_dict behaviour with no attributes"""

        dataset_dict = {}

        dataset = Dataset.from_dict(dataset_dict)

        self.assertIsNone(dataset.dataset_id)
        self.assertIsNone(dataset.alias)
        self.assertIsNone(dataset.workspace_id)
        self.assertIsNone(dataset.title)
        self.assertIsNone(dataset.description)
        self.assertIsNone(dataset.questions)
        self.assertIsNone(dataset.raw_data)
        self.assertIsNone(dataset.visualisation)
        self.assertIsNone(dataset.metadata)
        self.assertIsNone(dataset.query)

    def test_from_dict_invalid_attrs(self):
        """Tests from_dict behaviour with invalid attributes"""

        invalid_attr = 'invalid_attr'

        dataset_dict = {
            invalid_attr: 'invalid-value'
        }

        dataset = Dataset.from_dict(dataset_dict)

        self.assertIsNone(dataset.dataset_id)
        self.assertIsNone(dataset.alias)
        self.assertIsNone(dataset.workspace_id)
        self.assertIsNone(dataset.title)
        self.assertIsNone(dataset.description)
        self.assertIsNone(dataset.questions)
        self.assertIsNone(dataset.raw_data)
        self.assertIsNone(dataset.visualisation)
        self.assertIsNone(dataset.metadata)
        self.assertIsNone(dataset.query)

        self.assertFalse(hasattr(dataset, invalid_attr))


if __name__ == '__main__':
    unittest.main()
