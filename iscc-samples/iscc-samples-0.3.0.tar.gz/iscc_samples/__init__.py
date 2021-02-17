from pathlib import Path
from os.path import realpath, dirname
from typing import List


HERE = Path(dirname(realpath(__file__)))
ROOT = HERE / "files"
TEXT = ROOT / "text"
IMAGE = ROOT / "image"
AUDIO = ROOT / "audio"
VIDEO = ROOT / "video"


def all():
    return texts() + images() + audios() + videos()


def texts() -> List[Path]:
    return sorted(TEXT.rglob("*"))


def images() -> List[Path]:
    return sorted(IMAGE.rglob("*"))


def audios() -> List[Path]:
    return sorted(AUDIO.rglob("*"))


def videos() -> List[Path]:
    return sorted(VIDEO.rglob("*"))

