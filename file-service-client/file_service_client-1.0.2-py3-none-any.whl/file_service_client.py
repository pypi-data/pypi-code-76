import pathlib
from typing import Dict, Any
from marshmallow import EXCLUDE
from clients_core.service_clients import E360ServiceClient
from .models import FileSchema, FileCreateSchema


class FileServiceClient(E360ServiceClient):
    """
    Subclasses dataclass `clients_core.service_clients.E360ServiceClient`.

    Args:
        client (clients_core.rest_client.RestClient): an instance of a rest client
        user_id (str): the user_id guid

    """
    service_endpoint = ""
    extra_headers = {
        "accept": "application/json",
        "Content-Type": "application/json-patch+json",
    }

    # write your functions here
    # Use self.client to make restful calls

    def create(self, file_path: pathlib.Path, metadata: Dict = None, **kwargs: Any) -> FileSchema:
        """
        Creates a new file asset.

        Args:
            file_path: Path object to which file to upload.
            metadata: optionally pass metadata
            mime_type: optionally provide the mimetype for the file

        Raises:
            FileNotFoundError: when ``file_path`` is not found.

        """
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f'File specified is not found: {file_path}')

        headers = self.extra_headers.copy()
        headers.update(self.get_ims_claims())

        mime_type = kwargs.pop('mime_type', None)
        data = FileCreateSchema.from_file(file_path, metadata=metadata, mime_type=mime_type)
        response = self.client.post('', json=data, headers=self.service_headers, raises=True, **kwargs)

        response_json = response.json()
        return FileSchema(exclude=['contents'], unknown=EXCLUDE).load(response_json)

    def get_by_id(self, file_id: str, **kwargs: Any) -> FileSchema:
        """
        Retrieve the file object by its id.
        """
        headers = self.extra_headers.copy()
        headers.update(self.get_ims_claims())

        response = self.client.get(file_id, headers=self.service_headers, raises=True, **kwargs)

        response_json = response.json()
        return FileSchema(unknown=EXCLUDE).load(response_json)

    def get_file_bytes(self, file_id: str, **kwargs: Any) -> bytes:
        """
        Returns file bytes by ``file_id``.
        """
        return self.get_by_id(file_id, **kwargs)['contents']  # type: ignore

    def delete_by_id(self, file_id: str, **kwargs: Any) -> bool:
        """
        Delete the file object by its id. Returns True when deleted successfully.
        """
        response = self.client.delete(file_id, headers=self.service_headers, **kwargs)
        return response.ok
