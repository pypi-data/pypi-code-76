import os

from abc import ABC
from pathlib import Path
from typing import ClassVar, Optional, Tuple

from botocore.config import Config
from pydantic import BaseModel, BaseSettings, Field


class _Paths(BaseSettings):
    terality_home: Path = Field(Path.home() / '.terality', env='TERALITY_HOME')


class BaseConfig(BaseModel, ABC):
    _rel_path: ClassVar[str]  # path to the configuration file relative to `$TERALITY_HOME`
    _permissions: ClassVar[int] = 0o644  # rw-r--r--

    @classmethod
    def _file_path(cls) -> Path:
        return _Paths().terality_home / cls._rel_path

    @classmethod
    def load(cls, allow_missing: bool = False):
        file_path = cls._file_path()
        if allow_missing and not file_path.exists():
            return None
        return cls.parse_file(file_path)

    def save(self) -> None:
        file_path = self._file_path()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=self._permissions), 'w') as f:
            f.write(self.json(indent=4))


class TeralityCredentials(BaseConfig):
    _rel_path: ClassVar[str] = 'credentials.json'
    _permissions: ClassVar[int] = 0o600  # rw-------
    user_id: str
    user_password: str


class TeralityConfig(BaseConfig):
    _rel_path: ClassVar[str] = 'config.json'
    url: str = 'api.terality2.com/prod-main'
    use_https: bool = True
    requests_ssl_verification: bool = True
    timeout: Tuple[int, int] = (3, 180)


class UploadConfig(BaseModel):
    default_aws_region: str
    bucket: str
    key_prefix: str

    def bucket_region(self, aws_region: Optional[str] = None) -> str:
        return f'{self.bucket}-{self.default_aws_region if aws_region is None else aws_region}'


class DownloadConfig(BaseModel):
    default_aws_region: str
    bucket: str
    key_prefix: str

    def bucket_region(self, aws_region: Optional[str] = None) -> str:
        return f'{self.bucket}-{self.default_aws_region if aws_region is None else aws_region}'


class ConfigS3:
    max_conns: int = 1000
    max_retries: int = 1
    connect_timeout: int = 5
    read_timeout: int = 5

    @classmethod
    def config(cls) -> Config:
        return Config(
            max_pool_connections=cls.max_conns,
            retries=dict(max_attempts=cls.max_retries),
            connect_timeout=cls.connect_timeout
        )
