from pathlib import Path
from typing import Optional, Union

import pydantic
from flex_config import construct_config, EnvSource, YAMLSource

from certdumper import exc


_ENV_PREFIX = 'CERTDUMPER_'
_CONFIG_FILE_NAME = 'certdumper.yaml'
__all__ = [
    'config'
]


class CertDumperConfig(pydantic.BaseModel):
    work_dir: Optional[str] = None
    acme_path: str = 'acme.json'
    prev_acme_path: str = 'prev_acme.json'
    out_dir: str = 'certs'
    domain: Optional[str] = None
    log_file: str = 'logs'
    out_path: str = '{domain}'
    key_ext: str = '.key'
    cert_ext: str = '.crt'

    def rel_path(self, path: Optional[Union[str, Path]] = None) -> Path:
        path = Path(path)

        if self.work_dir and not path.is_absolute():
            work_dir = Path(self.work_dir)
            return (work_dir / path) if path else work_dir

        return path

    @property
    def config_path(self) -> Path:
        if not self.work_dir:
            raise exc.NoProject(work_dir=Path.cwd())

        return Path(self.work_dir) / _CONFIG_FILE_NAME


def _load_config():
    if proj_config := _discover_config():
        sources = [
            # We know _proj_config exists at this point.
            YAMLSource(proj_config),
            # Inject config path (will be used for relative paths)
            {'work_dir': str(proj_config.parent)},
            EnvSource(prefix=_ENV_PREFIX, separator='__'),
        ]
    else:
        sources = [EnvSource(prefix=_ENV_PREFIX, separator='__')]

    return construct_config(CertDumperConfig, sources)


def _discover_config() -> Optional[Path]:
    """ Find the project path by going up the file tree.

    This will look in the current directory and upwards for sokoban.yaml
    """
    curr = Path.cwd()
    root_path = Path('/')

    while curr != root_path:
        if next((p for p in curr.iterdir() if p.name == _CONFIG_FILE_NAME), None):
            return curr / _CONFIG_FILE_NAME
        else:
            curr = curr.parent

    return None


config = _load_config()
