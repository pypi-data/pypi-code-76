import io
import json
import shutil
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Union
from typing.io import BinaryIO
from uuid import UUID

import jwt
import requests

from unfolded.data_sdk.errors import (
    AuthenticationError, DataSDKError, UnknownDatasetNameError,
    UnknownMediaTypeError)
from unfolded.data_sdk.models import Dataset, MediaType

REFRESH_BUFFER = timedelta(minutes=1)

CREDENTIALS_NOT_WRITABLE_MSG = """\
Credentials directory not writable.
Either make $HOME/.config/unfolded writable or supply another credentials_dir.
"""


class DataSDK:
    client_id: str = 'v970dpbcqmRtr3y9XwlAB3dycpsvNRZF'
    base_url: str = 'https://api.unfolded.ai'
    auth_url: str = 'https://auth.unfolded.ai/oauth/token'

    def __init__(
        self,
        refresh_token: Optional[str] = None,
        credentials_dir: Union[Path,
                               str] = Path('~/.config/unfolded/').expanduser()):
        """Constructor for DataSDK

        Args:
            refresh_token (optional): a refresh token for interacting with
                Unfolded Studio. This only needs to be provided once; the
                refresh token will be saved to disk and will be transparently
                loaded in future uses of the DataSDK class. Default: loads
                refresh token from saved file path on disk.
            credentials_dir (optional): a path to a directory on disk to be used
                as the credentials directory. By default this is
                $HOME/.config/unfolded. If this path isn't writable, you can
                either make that path writable or define a custom credentials
                directory. If you use a custom directory, you'll need to include
                that every time you use the DataSDK class.
        """
        self.credentials_dir = Path(credentials_dir)

        if refresh_token:
            self._write_refresh_token(refresh_token)
        else:
            try:
                self._load_refresh_token()
            except:
                msg = 'refresh_token was not provided and was not previously saved.'
                raise AuthenticationError(msg)

        # Initialize access token to the past
        self._token = None

    def list_datasets(self) -> List[Dataset]:
        """List datasets for given user

        Returns:
            List of dataset objects.
        """
        url = f'{self.base_url}/v1/datasets'
        r = requests.get(url, headers=self._headers)
        r.raise_for_status()

        return [Dataset(**item) for item in r.json().get('items', [])]

    def get_dataset_by_id(self, dataset: Union[Dataset, str, UUID]) -> Dataset:
        """Get dataset given its id

        Args:
            dataset: dataset record to retrieve.

        Returns:
            Retrieved dataset record.
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.base_url}/v1/datasets/{str(dataset)}'
        r = requests.get(url, headers=self._headers)
        r.raise_for_status()

        return Dataset(**r.json())

    def download_dataset(
        self,
        dataset: Union[Dataset, str, UUID],
        output_file: Optional[Union[BinaryIO, str, Path]] = None
    ) -> Optional[bytes]:
        """Download data for dataset

        Args:
            dataset: identifier for dataset whose data should be downloaded.
            output_file: if provided, a path or file object to write dataset's data to.

        Returns:
            If output_file is None, returns bytes containing dataset's data.
            Otherwise, returns None and writes dataset's data to output_file.
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.base_url}/v1/datasets/{str(dataset)}/data'

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
            name: Optional[str] = None,
            media_type: Optional[Union[str, MediaType]] = None,
            description: Optional[str] = None) -> Dataset:
        """Upload new dataset to Unfolded Studio

        Args:
            file: path or file object to use for uploading data.
            name: name for dataset record.
            media_type: media type of data. By default, tries to infer media type from file name.
            description: description for dataset record.

        Returns:
            Updated dataset record
        """
        if not name:
            name = self._infer_new_dataset_name(file)

        if not media_type:
            media_type = self._infer_media_type(file=file)

        if isinstance(media_type, MediaType):
            media_type = media_type.value

        url = f'{self.base_url}/v1/datasets/data'
        headers = {**self._headers, 'Content-Type': media_type}

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

    def upload_dataframe(
            self, df, name: str, index: bool = True, **kwargs) -> Dataset:
        """Upload DataFrame or GeoDataFrame to Unfolded Studio

        Args:
            df: Either a pandas DataFrame or a geopandas GeoDataFrame to upload to Unfolded Studio.
            name: Name of dataset record
            index (optional): if True, include row names in output. Default: True.
            **kwargs: keyword arguments to pass on to DataSDK.upload_file

        Returns:
            Dataset record of new data.
        """
        with BytesIO(df.to_csv(index=index).encode('utf-8')) as bio:
            return self.upload_file(
                file=bio, name=name, media_type=MediaType.CSV, **kwargs)

    def update_dataset(
        self,
        file: Union[BinaryIO, str, Path],
        dataset: Union[Dataset, str, UUID],
        media_type: Optional[Union[str, MediaType]] = None,
    ) -> Dataset:
        """Update data for existing Unfolded Studio dataset

        Note that this overwrites any existing data attached to the dataset.

        Args:
            file: path or file object to use for uploading data.
            dataset: dataset whose data should be updated.
            media_type: media type of data. By default, tries to infer media type from file name.

        Returns:
            Updated dataset record
        """
        if not media_type:
            media_type = self._infer_media_type(file=file)

        if isinstance(media_type, MediaType):
            media_type = media_type.value

        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.base_url}/v1/datasets/{str(dataset)}/data'
        headers = {**self._headers, 'Content-Type': media_type}

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

        Args:
            dataset: dataset to delete from Unfolded Studio.

        Returns:
            None
        """
        if isinstance(dataset, Dataset):
            dataset = dataset.id

        url = f'{self.base_url}/v1/datasets/{str(dataset)}'
        r = requests.delete(url, headers=self._headers)
        r.raise_for_status()

    def _infer_new_dataset_name(self, file: Union[BinaryIO, str, Path]) -> str:
        general_msg = 'Please supply an explicit name for the dataset.'
        if isinstance(file, io.IOBase):
            raise UnknownDatasetNameError(
                f"Cannot infer dataset name from binary stream.\n{general_msg}")

        if isinstance(file, Path):
            return file.name

        return Path(file).name

    def _infer_media_type(self, file: Union[BinaryIO, str, Path]) -> MediaType:
        general_msg = 'Please supply an explicit Media Type for the file.'
        if isinstance(file, io.IOBase):
            raise UnknownMediaTypeError(
                f"Cannot infer Media Type from binary stream.\n{general_msg}")

        media_type = self._infer_media_type_from_path(file)

        if not media_type:
            raise UnknownMediaTypeError(
                f"Could not infer file's Media Type.\n{general_msg}")

        return media_type

    @staticmethod
    def _infer_media_type_from_path(
            path: Union[str, Path]) -> Optional[MediaType]:
        suffix = Path(path).suffix.lstrip('.').upper()

        try:
            return MediaType[suffix]
        except KeyError:
            return None

    @property
    def _headers(self):
        """Default headers to send with each request
        """
        return {'Authorization': f'Bearer {self.token}'}

    @property
    def token(self) -> str:
        """Valid access token for interacting with Unfolded Studio's backend
        """
        # If no token in memory, try to load saved access token if one exists
        if not self._token:
            try:
                self.token = self._load_saved_access_token()
            except FileNotFoundError:
                pass

        # If token is expired, refresh it
        if not self._token or (datetime.now() >=
                               self._token_expiration - REFRESH_BUFFER):
            self._refresh_access_token()

        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def _token_expiration(self) -> datetime:
        # Use _token to bypass logic that depends on token_expiration to avoid
        # recursion error
        token = self._token

        # If token doesn't exist, provide timestamp in the past to trigger token
        # refresh
        if not token:
            return datetime.now() - timedelta(seconds=1)

        decoded = jwt.decode(token, options={"verify_signature": False})

        # Leave a one minute buffer
        return datetime.fromtimestamp(decoded['exp'])

    @property
    def _refresh_token_path(self) -> Path:
        return self.credentials_dir / 'credentials.json'

    @property
    def _access_token_path(self) -> Path:
        return self.credentials_dir / 'access_token.json'

    def _load_refresh_token(self) -> str:
        """Load saved refresh token
        """
        with open(self._refresh_token_path, encoding='utf-8') as f:
            return json.load(f)['refresh_token']

    def _load_saved_access_token(self) -> str:
        """Load saved access token
        """
        with open(self._access_token_path, encoding='utf-8') as f:
            data = json.load(f)

        return data['access_token']

    def _write_refresh_token(self, refresh_token: str) -> None:
        """Write refresh token to credentials_dir
        """
        if not refresh_token.startswith('v1.'):
            raise ValueError('Refresh token should start with "v1."')

        try:
            # Create credentials directory if it doesn't exist
            self._refresh_token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._refresh_token_path, 'w', encoding='utf-8') as f:
                json.dump({'refresh_token': refresh_token}, f)
        except OSError as e:
            raise DataSDKError(CREDENTIALS_NOT_WRITABLE_MSG) from e

    def _write_access_token(self) -> None:
        """Write access token to credentials_dir
        """
        if not self._token:
            raise ValueError("No access token to write.")

        try:
            # Create credentials directory if it doesn't exist
            self._access_token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._access_token_path, 'w', encoding='utf-8') as f:
                json.dump({'access_token': self._token}, f)
        except OSError as e:
            raise DataSDKError(CREDENTIALS_NOT_WRITABLE_MSG) from e

    def _refresh_access_token(self):
        refresh_token = self._load_refresh_token()

        post_data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'refresh_token': refresh_token}

        r = requests.post(self.auth_url, json=post_data)
        r.raise_for_status()
        auth_data = r.json()

        # Because we use rotating refresh tokens, we must write the refresh
        # token returned from the API call to disk.
        new_refresh_token = auth_data['refresh_token']
        self._write_refresh_token(new_refresh_token)
        self.token = auth_data['access_token']
        self._write_access_token()
