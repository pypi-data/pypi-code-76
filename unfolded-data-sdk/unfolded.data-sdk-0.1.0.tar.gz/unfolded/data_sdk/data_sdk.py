import io
import shutil
from pathlib import Path
from typing import List, Optional, Union
from typing.io import BinaryIO
from uuid import UUID

import requests

from unfolded.data_sdk.errors import UnknownContentTypeError
from unfolded.data_sdk.models import ContentType, Dataset


class DataSDK:
    def __init__(self, token: str, baseurl: str = 'https://api.unfolded.ai'):
        self.token = token
        self.baseurl = baseurl

    def list_datasets(self) -> List[Dataset]:
        """List datasets for given user
        """
        url = f'{self.baseurl}/v1/datasets'
        r = requests.get(url, headers=self._headers)
        r.raise_for_status()

        return [Dataset(**item) for item in r.json().get('items', [])]

    def get_dataset_by_id(self, dataset: Union[Dataset, str, UUID]) -> Dataset:
        """Get dataset given its id
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.baseurl}/v1/datasets/{str(dataset)}'
        r = requests.get(url, headers=self._headers)
        r.raise_for_status()

        return Dataset(**r.json())

    def download_dataset(
        self,
        dataset: Union[Dataset, str, UUID],
        output_file: Optional[Union[BinaryIO, str, Path]] = None
    ) -> Optional[bytes]:
        """Download data for dataset given its id
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.baseurl}/v1/datasets/{str(dataset)}/data'

        if output_file:
            if isinstance(output_file, io.IOBase):
                return self._download_dataset_to_fileobj(
                    url=url, fileobj=output_file)

            with open(output_file, 'wb') as f:
                return self._download_dataset_to_fileobj(url=url, fileobj=f)
        else:
            return self._download_dataset_to_bytes(url=url)

    def _download_dataset_to_fileobj(self, url: str, fileobj: BinaryIO) -> None:
        """Download dataset to file object
        """
        # TODO: progress bar here?
        # Looks like there's no callback in copyfileobj
        with requests.get(url, headers=self._headers, stream=True) as r:
            shutil.copyfileobj(r.raw, fileobj)

    def _download_dataset_to_bytes(self, url: str) -> bytes:
        """Download dataset to bytes object
        """
        r = requests.get(url, headers=self._headers)
        r.raise_for_status()
        return r.content

    def upload_file(
            self,
            file: Union[BinaryIO, str, Path],
            name: str,
            content_type: Optional[Union[str, ContentType]],
            description: Optional[str] = None) -> Dataset:
        """Upload new dataset to Unfolded Studio
        """
        if not content_type:
            content_type = self._infer_content_type(
                content_type=content_type, file=file)

        url = f'{self.baseurl}/v1/datasets/data'
        headers = {**self._headers, 'Content-Type': content_type}

        params = {'name': name}
        if description:
            params['description'] = description

        if isinstance(file, io.IOBase):
            r = requests.post(url, data=file, params=params, headers=headers)
            r.raise_for_status()
            return Dataset(**r.json())

        # TODO: progress bar here
        with open(file, 'rb') as f:
            r = requests.post(url, data=f, params=params, headers=headers)

        r.raise_for_status()
        return Dataset(**r.json())

    def update_dataset(
        self,
        file: Union[BinaryIO, str, Path],
        dataset: Union[Dataset, str, UUID],
        content_type: Optional[Union[str, ContentType]],
    ) -> Dataset:
        """Update data for existing Unfolded Studio dataset
        """
        if not content_type:
            content_type = self._infer_content_type(
                content_type=content_type, file=file)

        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.baseurl}/v1/datasets/{str(dataset)}/data'
        headers = {**self._headers, 'Content-Type': content_type}

        if isinstance(file, io.IOBase):
            r = requests.put(url, data=file, headers=headers)
            r.raise_for_status()
            return Dataset(**r.json())

        # TODO: progress bar here
        with open(file, 'rb') as f:
            r = requests.put(url, data=f, headers=headers)

        r.raise_for_status()
        return Dataset(**r.json())

    def delete_dataset(self, dataset: Union[Dataset, str, UUID]) -> None:
        """Delete dataset from Unfolded Studio

        Warning: This operation cannot be undone. If you delete a dataset
        currently used in one or more maps, the dataset will be removed from
        those maps, possibly causing them to render incorrectly.
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.baseurl}/v1/datasets/{str(dataset)}'
        r = requests.delete(url, headers=self._headers)
        r.raise_for_status()

    def _infer_content_type(
            self, content_type: Optional[Union[str, ContentType]],
            file: Union[BinaryIO, str, Path]) -> str:
        if content_type:
            return content_type

        general_msg = 'Please supply an explicit Content-Type for the file.'
        if isinstance(file, io.IOBase):
            raise UnknownContentTypeError(
                f"Cannot infer Content-Type from binary stream.\n{general_msg}")

        content_type = self._infer_content_type_from_path(file)

        if not content_type:
            raise UnknownContentTypeError(
                f"Could not infer file's Content-Type.\n{general_msg}")

        if isinstance(content_type, ContentType):
            content_type = content_type.value

        return content_type

    @staticmethod
    def _infer_content_type_from_path(
            path: Union[str, Path]) -> Optional[ContentType]:
        suffix = Path(path).suffix.lstrip('.').upper()

        try:
            return ContentType[suffix]
        except KeyError:
            return None

    @property
    def _headers(self):
        """Default headers to send with each request
        """
        return {'Authorization': f'Bearer {self.token}'}
