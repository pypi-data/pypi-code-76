import os
from contextlib import contextmanager
from typing import ContextManager, Union
import tempfile
from src.pset1.hash_str import get_user_id


@contextmanager
def atomic_write(filepath: Union[str, os.PathLike], mode: str = "w", as_file: bool = True, **kwargs) -> ContextManager:
    """Write a file atomically

    :param filepath: str or :class:`os.PathLike` target to write
    :param mode: the mode in which the file is opened, defaults to "w" (writing in text mode)
    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string

    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if target exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = os.path.join(tmp, get_user_id(str(filepath)))
        if os.path.isfile(filepath):
            raise Exception("Target File Already Exists")
        try:
            with open(tmp_path, mode, **kwargs) as file:
                if as_file:
                    yield file
                else:
                    yield file.name
                file.flush()
                os.fsync(file.fileno())
            os.rename(tmp_path, filepath)
        finally:
            try:
                os.remove(tmp_path)
            except (IOError, OSError):
                pass
