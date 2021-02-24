import atexit
import sys
from typing import Any, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel
import requests

from terality.exceptions import _error_mapping
from terality.version import __version__
from .. import TeralityNetworkError, TeralityInternalError, TeralityError
from . import UploadConfig, DownloadConfig, TeralityConfig, logger, config_not_found, config_helper, TeralityCredentials


class _Process(BaseModel):
    """ Info about the python process using terality"""
    python_version_major: str = str(sys.version_info.major)
    python_version_minor: str = str(sys.version_info.minor)
    python_version_micro: str = str(sys.version_info.micro)
    numpy_version: str = np.__version__
    pandas_version: str = pd.__version__
    terality_version: str = __version__


class _Session(BaseModel):
    id: str
    upload_config: UploadConfig
    download_config: DownloadConfig


class ErrorResponse(BaseModel):
    type: Optional[str] = None
    message: str


class Connection:
    _config: TeralityConfig
    _credentials: TeralityCredentials
    _process: _Process = _Process()
    session: Optional[_Session] = None

    @classmethod
    def send_request(cls, action: str, payload: Any, without_session: bool = False) -> str:
        if cls._config is None:
            raise RuntimeError('Please specify user credentials')
        # Create new session on the fly if needed.
        if not without_session and cls.session is None:
            cls._create_session()
        try:
            full_url = f'{"https" if cls._config.use_https else "http"}://{cls._config.url}/{action}'
            r = requests.post(
                full_url,
                json={'session_id': None if without_session else cls.session.id, 'payload': payload},
                auth=(cls._credentials.user_id, cls._credentials.user_password),
                verify=cls._config.requests_ssl_verification,
                timeout=cls._config.timeout,
                headers=cls._process.dict(),
            )
            response = r.text
        except requests.RequestException as e:
            raise TeralityNetworkError('Trouble contacting the API') from e

        if not r.ok:
            server_error = ErrorResponse.parse_raw(response)
            error_class = _error_mapping.get(server_error.type, TeralityInternalError)
            raise error_class(server_error.message)
        return response

    @classmethod
    def _deserialize_session(cls, session_serialized: str) -> _Session:
        """ In a function rather than inline to allow monkey patching in tests"""
        return _Session.parse_raw(session_serialized)

    @classmethod
    def _create_session(cls) -> None:
        session_serialized = cls.send_request('create_session', None, without_session=True)
        cls.session = cls._deserialize_session(session_serialized)

    @classmethod
    def delete_session(cls) -> None:
        if cls.session is not None:
            cls.send_request('delete_session', {})
            cls.session = None

    @classmethod
    def set_up(cls, config: TeralityConfig, credentials: TeralityCredentials) -> None:
        cls._config = config
        cls._credentials = credentials
        cls._create_session()

    @classmethod
    def init(cls):
        if cls.session is None:
            logger.info('Initializing Terality')
            try:
                cls.set_up(TeralityConfig.load(), TeralityCredentials.load())
            except Exception as exc:
                logger.warning(exc)
                logger.warning(f'{config_not_found}\n{config_helper}')


def configure(user_id: str, user_password: str, *, check_connection: bool = True) -> None:
    """
    Provide Terality credentials and store them in the user's configuration directory.
    This also creates a configuration file if necessary.
    """
    credentials = TeralityCredentials(user_id=user_id, user_password=user_password)
    credentials.save()
    config = TeralityConfig.load(allow_missing=True)
    if config is None:
        config = TeralityConfig()
        config.save()
    if check_connection:
        Connection.set_up(config, credentials)


Connection.init()


def _atexit_delete_session():
    # Try to delete the current session, using a best effort policy. => Swallow any (Terality) exception.
    try:
        Connection.delete_session()
    except TeralityError:
        pass  # nosec: B110 (try_except_pass)


atexit.register(_atexit_delete_session)
