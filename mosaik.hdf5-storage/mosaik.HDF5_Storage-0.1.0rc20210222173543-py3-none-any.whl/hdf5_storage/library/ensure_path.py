from pathlib import Path
from typing import Union


def ensure_path(path: Union[Path, str]):
    Path(path).mkdir(
        parents=True,
        exist_ok=True,
    )
