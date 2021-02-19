import datetime
import subprocess
import tempfile
from pathlib import Path


def create_dir(parent_dir: Path, db_name: str) -> Path:
    """ Create a directory. """

    temp_dir = (
        parent_dir / f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        f"_{db_name}"
    )
    temp_dir.mkdir(parents=True)

    return temp_dir


def create_temp_dir(parent_dir: Path) -> Path:
    """ Create a temp directory, which will be deleted on object destruction. """

    temp_dir = tempfile.TemporaryDirectory(
        prefix=f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_",
        dir=parent_dir,
    )

    return Path(temp_dir.name)


def symlink(frm: Path, to: Path, force: bool = False):
    """ Create a symlink from one file to another. """

    if force:
        cmd = f"ln -sfT {frm} {to}"
    else:
        cmd = f"ln -s {frm} {to}"

    completed_process = subprocess.run(cmd, shell=True)

    if completed_process.returncode:
        raise Exception(f"Can't create a symlink: {cmd}")

    return to
