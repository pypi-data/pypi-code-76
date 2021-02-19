import os
import pathlib


class Path(pathlib.Path):
    def __new__(cls, *args, **kwargs):
        if cls is Path:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        self = super().__new__(cls, *args, **kwargs)
        return self

    def unique(self):
        """Ensure this path doesn't already exist, will append a number to make it unique."""
        obj = self
        unique_folder = 0
        while obj.exists():
            obj = self.parent / f"{self.stem}_{str(unique_folder)}{self.suffix}"
            unique_folder += 1
        return obj


class PosixPath(Path, pathlib.PosixPath):
    pass


class WindowsPath(Path, pathlib.WindowsPath):
    pass
