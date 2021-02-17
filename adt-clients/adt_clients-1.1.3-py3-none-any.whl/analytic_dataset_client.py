import math
import uuid
import pathlib
import requests
from typing import Dict, Any
from typing.io import BinaryIO
from dataclasses import dataclass
from clients_core.service_clients import E360ServiceClient
from .models import AnalyticDatasetModel, Granularity, AnalyticDatasetFormat
from marshmallow import EXCLUDE


@dataclass
class AnalyticDatasetClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid
        correlation_id (str): the correlation_id guid

    """
    correlation_id: str = str(uuid.uuid4())

    service_endpoint = ""
    extra_headers = {}  # type: Dict[str, str]

    def __post_init__(self) -> None:
        self.extra_headers.update({
            'x-correlation-id': self.correlation_id,
            **self.get_ims_claims()
        })

    def get(self, dataset_id: str, **kwargs: Any) -> AnalyticDatasetModel:
        """
        Gets the analytic dataset object by id.
        """
        response = self.client.get(dataset_id, headers=self.extra_headers, raises=True, **kwargs)
        return AnalyticDatasetModel.Schema(unknown=EXCLUDE).load(response.json())

    @staticmethod
    def _file_writer(response: requests.Response, output_path: pathlib.Path) -> None:
        with output_path.open(mode='wb') as file_writer:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    file_writer.write(chunk)

    def download_report(self,
                        dataset_id: str,
                        output_path: pathlib.Path,
                        accept: str,
                        overwrite_output: bool = False,
                        impersonate_id: str = None,
                        **kwargs: Any) -> bool:
        """
        Downloads a provided dataset_id to the output path.

        Args:
            dataset_id: download dataset_id for a dataset file.
            output_path: Path object where to save the file to.
            accept: header value for accept; this needs to match the expected download file.
            overwrite_output: if set to True, will overwrite existing output.
            impersonate_id: the user Id to perform the operation on behalf of
            **kwargs: passed onto the self.client

        Resturns:
            bool: that an output file has been created successfully.

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
            FileExistsError: if the ``output_path`` already exists.

        """
        if all([output_path.exists(), overwrite_output is False]):
            raise FileExistsError('Specified `output_path` already exists. Set `overwrite_output=True` to overwrite it.')

        endpoint_path = f'{dataset_id}/download'
        if impersonate_id:
            if not hasattr(kwargs, "params"):
                kwargs["params"] = {}
            kwargs["params"] = {"workspaceImpersonationId": impersonate_id}
        response = self.client.get(endpoint_path, stream=True, headers={"accept": accept, **self.extra_headers}, raises=True, **kwargs)

        self._file_writer(response, output_path)

        return all([output_path.exists(), output_path.is_file()])

    @staticmethod
    def _get_timeout_for_data(file_path: pathlib.Path, kbps: int = 200_000) -> int:
        """
        Get a reasonable request timeout value in seconds by the size of the ``file_path``.

        Args:
            file_path: file which is intended to be uploaded.
            kbps: minimum upload speed.
        """
        file_size = file_path.stat().st_size or 1
        return math.ceil(file_size / kbps)

    def upload_stream(self, obj_buffer: BinaryIO, granularity: Granularity, dataset_type: AnalyticDatasetFormat, dataset_release_id: str = None, timeout: int = None, **kwargs: Any) -> AnalyticDatasetModel:
        """
        Upload dataset creating datasetinfo and asset if valid.

        Args:
            obj_buffer: buffer object for the content to be uploaded.
            granularity: one of supported ``adt_clients.models.Granularity``
            dataset_type: one of supported ``adt_clients.models.AnalyticDatasetFormat``
            dataset_release_id: dataset release id, optional.
            timeout: timeout in seconds, optional.

        Returns:
            dict: serialised instance of ``adt_clients.models.AnalyticDatasetModel``

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
            ValueError: when incorrect ``granularity`` or ``dataset_type`` specified.

        """
        endpoint_path = 'upload'
        headers = self.extra_headers.copy()
        headers.update({
            "content-type": "application/octet-stream",
            # raises ValueError if not valid granularity/dataset_type
            "x-adt-granularity": Granularity(granularity).value,
            "x-adt-file-type": AnalyticDatasetFormat(dataset_type).value,
            "X-ADT-Output-Type": AnalyticDatasetFormat(dataset_type).value,
        })
        if dataset_release_id is not None:
            headers["X-ADT-Dataset-Release-Identifier"] = dataset_release_id

        response = self.client.post(
            endpoint_path,
            data=obj_buffer,
            timeout=timeout,
            headers=headers,
            raises=True,
            **kwargs
        )

        return AnalyticDatasetModel.Schema(unknown=EXCLUDE).load(response.json())

    def upload_file(self, file_path: pathlib.Path, granularity: Granularity, dataset_type: AnalyticDatasetFormat, dataset_release_id: str = None, **kwargs: Any) -> AnalyticDatasetModel:
        """
        Same as `upload_stream`, but takes a file path as the main parameter.

        Args:
            file_path: Path object to which file to upload.

        Raises:
            FileNotFoundError: when ``file_path`` is not found.

        """
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f'File specified is not found: {file_path}')

        timeout = max(self._get_timeout_for_data(file_path), 60 * 10)
        with file_path.open('rb') as _file:
            return self.upload_stream(_file, granularity, dataset_type, dataset_release_id=dataset_release_id, timeout=timeout, **kwargs)

    def delete(self, id_: str, **kwargs: Any) -> bool:
        """
        Delete the report object by its id. Returns True when deleted successfully.
        """
        response = self.client.delete(id_, headers=self.service_headers, raises=True, **kwargs)
        return response.ok
