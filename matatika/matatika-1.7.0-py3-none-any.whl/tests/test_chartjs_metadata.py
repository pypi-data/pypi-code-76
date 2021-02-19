"""Chart.js metadata test module"""

import unittest
from matatika.metadata import ChartJSMetadata

EMPTY_LIST = []


class TestChartJSMetadata(unittest.TestCase):
    """Test class for Chart.js metadata parsing"""

    def test_columns(self):
        """Test columns property is a populated list if metadata contains related table columns"""

        metadata = {
            'related_table': {
                'columns': [
                    {
                        'name': 'metadata.column',
                    }
                ]
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)

        self.assertListEqual(parsed_metadata.columns,
                             metadata['related_table']['columns'])

    def test_empty_columns(self):
        """Test columns property is an empty list if metadata contains no related table columns"""

        metadata = {
            'related_table': {
                'columns': []
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)

        self.assertListEqual(parsed_metadata.columns, EMPTY_LIST)

    def test_no_columns_field(self):
        """Test columns property is None if metadata has no related table columns field"""

        metadata = {
            'related_table': {}
        }

        parsed_metadata = ChartJSMetadata(metadata)

        self.assertIsNone(parsed_metadata.columns)

    def test_aggregates(self):
        """Test aggregates property is a populated list if metadata contains related table
        aggregates"""

        metadata = {
            'related_table': {
                'aggregates': [
                    {
                        'name': 'metadata.aggregate'
                    }
                ]
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)

        self.assertListEqual(parsed_metadata.aggregates,
                             metadata['related_table']['aggregates'])

    def test_empty_aggregates(self):
        """Test aggregates property is an empty list if metadata contains no related table
        aggregates"""

        metadata = {
            'related_table': {
                'aggregates': []
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)

        self.assertListEqual(parsed_metadata.aggregates, EMPTY_LIST)

    def test_no_aggregates_field(self):
        """Test aggregates property is None if metadata has no related table aggregates
        field"""

        metadata = {
            'related_table': {}
        }

        parsed_metadata = ChartJSMetadata(metadata)

        self.assertIsNone(parsed_metadata.aggregates)

    def test_no_related_table_field(self):
        """Test columns and aggregates properties are None if metadata has no related table field"""

        metadata = {}

        parsed_metadata = ChartJSMetadata(metadata)

        self.assertIsNone(parsed_metadata.columns)
        self.assertIsNone(parsed_metadata.aggregates)

    def test_remove_basename(self):
        """Test metadata basename is removed from name and returned"""

        metadata = {
            'name': 'metadata'
        }

        parsed_metadata = ChartJSMetadata(metadata)
        name = parsed_metadata.remove_basename('metadata.column')

        self.assertEqual(name, 'column')

    def test_remove_basename_not_in_name(self):
        """Test unmodified name returned"""

        metadata = {
            'name': 'metadata'
        }

        parsed_metadata = ChartJSMetadata(metadata)
        name = parsed_metadata.remove_basename('column')

        self.assertEqual(name, 'column')

    def test_remove_basename_no_basename(self):
        """Test unmodified name returned"""

        metadata = {}

        parsed_metadata = ChartJSMetadata(metadata)
        name = parsed_metadata.remove_basename('column')

        self.assertEqual(name, 'column')

    def test_get_label_from_columns(self):
        """Test column name label is found in metadata related table columns and returned"""

        metadata = {
            'name': 'metadata',
            'related_table': {
                'columns': [
                    {
                        'name': 'column',
                        'label': 'Column'
                    }
                ]
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)
        label = parsed_metadata.get_label('metadata.column')

        self.assertEqual(label, 'Column')

    def test_get_label_from_aggregates(self):
        """Test column name label is found in metadata related table aggregates and returned"""

        metadata = {
            'name': 'metadata',
            'related_table': {
                'aggregates': [
                    {
                        'name': 'aggregate',
                        'label': 'Aggregate'
                    }
                ]
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)
        label = parsed_metadata.get_label('metadata.aggregate')

        self.assertEqual(label, 'Aggregate')

    def test_get_label_no_related_table(self):
        """Test column name label is None in metadata with no related table field"""

        metadata = {
            'name': 'metadata',
        }

        parsed_metadata = ChartJSMetadata(metadata)
        label = parsed_metadata.get_label('metadata.column')

        self.assertIsNone(label)

    def test_get_label_empty_columns_and_aggregates(self):
        """Test column name label is None if metadata has no related table columns and aggregates
        fields"""

        metadata = {
            'name': 'metadata',
            'related_table': {
                'columns': [],
                'aggregates': []
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)
        label = parsed_metadata.get_label('metadata.column')

        self.assertIsNone(label)

    def test_get_label_no_matching_columns_or_aggregates(self):
        """Test column name label is None if metadata has no matching columns or aggregates"""

        metadata = {
            'name': 'metadata',
            'related_table': {
                'columns': [
                    {
                        'name': 'metadata_column',
                    }
                ],
                'aggregates': [
                    {
                        'name': 'metadata_aggregate',
                    }
                ]
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)
        label = parsed_metadata.get_label('metadata.column')

        self.assertIsNone(label)

    def test_get_label_no_basename(self):
        """Test column name label is None if metadata has no basename"""

        metadata = {
            'related_table': {
                'columns': [
                    {
                        'name': 'column',
                        'label': 'Column'
                    }
                ]
            }
        }

        parsed_metadata = ChartJSMetadata(metadata)
        label = parsed_metadata.get_label('metadata.column')

        self.assertIsNone(label)
