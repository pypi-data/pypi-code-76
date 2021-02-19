"""metadata module"""

import json


class ChartJSMetadata:
    """Class for Chart.js metadata objects"""

    def __init__(self, metadata: dict):
        self.metadata = metadata
        self.columns = self._get_columns()
        self.aggregates = self._get_aggregates()

    def _get_related_table(self) -> dict:
        return self.metadata.get('related_table')

    def _get_columns(self) -> list:
        """Returns the related table columns"""

        related_table = self._get_related_table()
        if related_table is None:
            return None

        return related_table.get('columns')

    def _get_aggregates(self) -> list:
        """Returns the related table aggregates"""

        related_table = self._get_related_table()
        if related_table is None:
            return None

        return related_table.get('aggregates')

    def remove_basename(self, column_name: str):
        """Removes the metadata basename from the column name"""

        basename: str
        basename = self.metadata.get('name')

        if not basename:
            return column_name

        name_components = column_name.split('.')

        for basename_component in basename.split('.'):
            if basename_component in name_components:
                name_components.remove(basename_component)

        return '.'.join(name_components)

    def get_label(self, column_name: str):
        """Returns a label for a specific column name"""

        if self._get_related_table() is None:
            return None

        columns_and_aggregates = self.columns if self.columns else []
        columns_and_aggregates += self.aggregates if self.aggregates else []

        field: dict
        for field in columns_and_aggregates:
            if self.remove_basename(column_name) == field['name']:
                return field['label']
        return None

    def get_labels(self):
        """Returns all labels"""

        labels = []

        for label in _yield_values_by_key(self._get_related_table(), 'label'):
            labels.append(label)

        return labels

    @staticmethod
    def from_str(metadata_str):
        """Resolves a metadata object from a string"""

        return ChartJSMetadata(json.loads(metadata_str))


def data_with_metadata_labels(data, metadata):
    """Creates a copy of data with keys replaced by labels resolved from metadata"""

    label_sources = {
        k: v for (k, v) in metadata['related_table'].items() if isinstance(v, list)}

    new_data = []

    for data_point in data:
        new_data_point = {}
        for old_key in data_point.keys():

            result = _search_for_key_value(label_sources, 'key', old_key)
            new_key = result['label'] if result else old_key
            new_data_point[new_key] = data_point[old_key]

        new_data.append(new_data_point)

    return new_data


def _search_for_key_value(node, key, val):

    if isinstance(node, dict):
        key_val = node.get(key)
        if key_val:
            if key_val == val:
                return node

        for sub_node in node.values():
            result = _search_for_key_value(sub_node, key, val)
            if result:
                return result

    elif isinstance(node, list):
        for sub_node in node:
            result = _search_for_key_value(sub_node, key, val)
            if result:
                return result

    return None


def _yield_values_by_key(node, key):

    if isinstance(node, dict):
        key_val = node.get(key)
        if key_val:
            yield key_val

        for sub_node in node.values():
            yield from _yield_values_by_key(sub_node, key)

    elif isinstance(node, list):
        for sub_node in node:
            yield from _yield_values_by_key(sub_node, key)
