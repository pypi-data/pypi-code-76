# pylint: disable=too-many-instance-attributes

"""dataset module"""

from dataclasses import asdict, dataclass
import json


@dataclass
class Dataset():
    """Class for dataset objects"""

    dataset_id: str = None
    alias: str = None
    workspace_id: str = None
    title: str = None
    description: str = None
    questions: str = None
    raw_data: str = None
    visualisation: str = None
    metadata: str = None
    query: str = None

    def to_dict(self, filter_none=True):
        """Converts the dataset object to a dictionary"""

        attr_translations = {
            ('id', 'dataset_id'),
            ('workspaceId', 'workspace_id'),
            ('rawData', 'raw_data'),
        }

        dict_repr = asdict(self)

        for translation in attr_translations:
            dict_repr = {translation[0] if k == translation[1]
                         else k: v for k, v in dict_repr.items()}

        if filter_none:
            return {k: v for k, v in dict_repr.items() if v is not None}
        return dict_repr

    def to_json_str(self, filter_none=True):
        """Converts the dataset object to a JSON string"""

        return json.dumps(self.to_dict(filter_none=filter_none))

    @staticmethod
    def from_dict(datasets_dict):
        """Resolves a dataset object from a dictionary"""

        dataset = Dataset()

        dataset.dataset_id = datasets_dict.get('id')
        dataset.alias = datasets_dict.get('alias')
        dataset.workspace_id = datasets_dict.get('workspaceId')
        dataset.title = datasets_dict.get('title')
        dataset.description = datasets_dict.get('description')
        dataset.questions = datasets_dict.get('questions')
        dataset.raw_data = datasets_dict.get('rawData')
        dataset.visualisation = datasets_dict.get('visualisation')
        dataset.metadata = datasets_dict.get('metadata')
        dataset.query = datasets_dict.get('query')

        return dataset
