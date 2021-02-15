__all__ = [
    "BaseDataConnection"
]

import io
import json


from abc import ABC, abstractmethod
from typing import Union, Tuple, TYPE_CHECKING

import requests
from pandas import concat

from watson_machine_learning_client.utils.autoai.utils import try_load_dataset
from watson_machine_learning_client.utils.autoai.enums import DataConnectionTypes
from watson_machine_learning_client.wml_client_error import ApiRequestFailure


if TYPE_CHECKING:
    from pandas import DataFrame
    from ibm_boto3 import resource


class BaseDataConnection(ABC):
    """
    Base class for  DataConnection.
    """

    def __init__(self):

        self.type = None
        self.connection = None
        self.location = None
        self.auto_pipeline_params = None
        self._wml_client = None
        self._run_id = None
        self._obm = None
        self._obm_cos_path = None
        self.id = None

    @abstractmethod
    def _to_dict(self) -> dict:
        """Convert DataConnection object to dictionary representation."""
        pass

    @classmethod
    @abstractmethod
    def _from_dict(cls, _dict: dict) -> 'BaseDataConnection':
        """Create a DataConnection object from dictionary."""
        pass

    @abstractmethod
    def read(self, with_holdout_split: bool = False) -> Union['DataFrame', Tuple['DataFrame', 'DataFrame']]:
        """Download dataset stored in remote data storage."""
        pass

    @abstractmethod
    def write(self, data: Union[str, 'DataFrame'], remote_name: str) -> None:
        """Upload file to a remote data storage."""
        pass

    def _fill_experiment_parameters(self, prediction_type: str, prediction_column: str, test_size: float,
                                    csv_separator: str = ',', excel_sheet: Union[str, int] = 0) -> None:
        """
        To be able to recreate a holdout split, this method need to be called.
        """
        self.auto_pipeline_params = {
            'prediction_type': prediction_type,
            'prediction_column': prediction_column,
            'test_size': test_size,
            'csv_separator': csv_separator,
            'excel_sheet': excel_sheet
        }

    def _download_obm_data_from_cos(self, cos_client: 'resource') -> 'DataFrame':
        """Download preprocessed OBM data. COS version."""

        # note: fetch all OBM file part names
        cos_summary = cos_client.Bucket(self.location.bucket).objects.filter(Prefix=self._obm_cos_path)
        file_names = [file_name.key for file_name in cos_summary]

        # note: if path does not exist, try to find in different one
        if not file_names:
            cos_summary = cos_client.Bucket(self.location.bucket).objects.filter(
                Prefix=self._obm_cos_path.split('./')[-1])
            file_names = [file_name.key for file_name in cos_summary]
            # --- end note
        # --- end note

        # TODO: this can be done simultaneously (multithreading / multiprocessing)
        # note: download all data parts and concatenate them into one output
        parts = []
        for file_name in file_names:
            file = cos_client.Object(self.location.bucket, file_name).get()
            buffer = io.BytesIO(file['Body'].read())
            parts.append(try_load_dataset(buffer=buffer))

        data = concat(parts)
        # --- end note
        return data

    def _download_obm_json_from_cos(self) -> dict:
        """Download obm.json log. COS version."""
        data = {}

        if self.type == DataConnectionTypes.S3 and self._obm:
            cos_client = self._init_cos_client()

            try:
                obm_json_path = self._obm_cos_path.rsplit('features', 1)[0] + 'obm.json'
                file = cos_client.Object(self.location.bucket, obm_json_path).get()
                content = file["Body"].read()
                data = json.loads(content.decode('utf-8'))
            except Exception as cos_access_exception:
                raise ConnectionError(
                    f"Unable to access data object in cloud object storage with credentials supplied. "
                    f"Error: {cos_access_exception}")

        else:
            raise NotImplementedError("OBM is not supported for CP4D and WML Server yet.")

        return data

    def _download_data_from_cos(self, cos_client: 'resource') -> 'DataFrame':
        """Download training data for this connection. COS version"""

        file = cos_client.Object(self.location.bucket,
                                 self.location.path).get()
        buffer = io.BytesIO(file['Body'].read())
        data = try_load_dataset(buffer=buffer,
                                sheet_name=self.auto_pipeline_params.get('excel_sheet', 0),
                                separator=self.auto_pipeline_params.get('csv_separator', ','))

        return data

    def _download_training_data_from_data_asset_storage(self) -> 'DataFrame':
        """Download training data for this connection. Data Storage."""

        # note: as we need to load a data into the memory,
        # we are using pure requests and helpers from the WML client
        asset_id = self.location.href.split('?')[0].split('/')[-1]

        # note: download data asset details
        asset_response = requests.get(self._wml_client.data_assets._href_definitions.get_data_asset_href(asset_id),
                                      params=self._wml_client._params(),
                                      headers=self._wml_client._get_headers(),
                                      verify=False)

        asset_details = self._wml_client.data_assets._handle_response(200, u'get assets', asset_response)

        # note: read the csv url
        attachment_url = asset_details['attachments'][0]['handle']['key']

        # note: make the whole url pointing out the csv
        artifact_content_url = (f"{self._wml_client.data_assets._href_definitions.get_wsd_model_attachment_href()}"
                                f"{attachment_url}")

        # note: stream the whole CSV file
        csv_response = requests.get(artifact_content_url,
                                    params=self._wml_client._params(),
                                    headers=self._wml_client._get_headers(),
                                    stream=True,
                                    verify=False)

        if csv_response.status_code != 200:
            raise ApiRequestFailure(u'Failure during {}.'.format("downloading model"), csv_response)

        downloaded_asset = csv_response.content

        # note: read the csv/xlsx file from the memory directly into the pandas DataFrame
        buffer = io.BytesIO(downloaded_asset)
        data = try_load_dataset(buffer=buffer,
                                sheet_name=self.auto_pipeline_params.get('excel_sheet', 0),
                                separator=self.auto_pipeline_params.get('csv_separator', ','))

        return data

    def _download_training_data_from_file_system(self) -> 'DataFrame':
        """Download training data for this connection. File system version."""

        try:
            url = f"{self._wml_client.wml_credentials['url']}/v2/asset_files/{self.location.path.split('/assets/')[-1]}"
            # note: stream the whole CSV file
            csv_response = requests.get(url,
                                        params=self._wml_client._params(),
                                        headers=self._wml_client._get_headers(),
                                        stream=True,
                                        verify=False)

            if csv_response.status_code != 200:
                raise ApiRequestFailure(u'Failure during {}.'.format("downloading model"), csv_response)

            downloaded_asset = csv_response.content
            # note: read the csv/xlsx file from the memory directly into the pandas DataFrame
            buffer = io.BytesIO(downloaded_asset)
            data = try_load_dataset(buffer=buffer,
                                    sheet_name=self.auto_pipeline_params.get('excel_sheet', 0),
                                    separator=self.auto_pipeline_params.get('csv_separator', ','))
        except (ApiRequestFailure, AttributeError):
            with open(self.location.path, 'rb') as data_buffer:
                data = try_load_dataset(buffer=data_buffer,
                                        sheet_name=self.auto_pipeline_params.get('excel_sheet', 0),
                                        separator=self.auto_pipeline_params.get('csv_separator', ','))

        return data
