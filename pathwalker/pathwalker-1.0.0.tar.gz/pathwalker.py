__author__ = "David Scheliga"
__email__ = "david.scheliga@gmx.de"
__version__ = "1.0.0"
__all__ = ["walk_file_paths", "walk_folder_paths"]


from pathlib import Path
from typing import Callable, Generator, Optional, Iterator, Union

APath = Union[str, Path]


def _get_path_generator(
    root_path: Path, recursive: bool = False
) -> Callable[[str], Generator]:
    searched_root_path = Path(root_path)
    if recursive:
        return searched_root_path.rglob
    else:
        return searched_root_path.glob


def _get_filter_pattern(pattern: Optional[str]):
    retrieve_all_paths = pattern is None
    if retrieve_all_paths:
        return "*"
    return pattern


def walk_folder_paths(
    root_path: APath, filter_pattern: Optional[str] = None, recursive: bool = False
) -> Iterator[Path]:
    """
    Yields only paths of directories.

    Args:
        root_path(Path):
            Root path to walk thourgh.

        filter_pattern(str):
            Unix path pattern for filtering retrieved paths.

        recursive(bool:
            Returns also paths of all sub folders.

    Yields:
        Path

    Examples:
        >>> from doctestprinter import doctest_iter_print
        >>> from pathwalker import walk_folder_paths
        >>> found_files = sorted(
        ...     walk_folder_paths(".", filter_pattern = "[!._]*"),
        ...     key=lambda x: str(x)
        ... )
        >>> doctest_iter_print(found_files)
        docs
        tests

    """
    path_generator = _get_path_generator(root_path=root_path, recursive=recursive)
    used_filter_pattern = _get_filter_pattern(filter_pattern)

    for child_path in path_generator(used_filter_pattern):
        if child_path.is_file():
            continue
        yield child_path


def walk_file_paths(
    root_path: APath, filter_pattern: Optional[str] = None, recursive: bool = False
) -> Generator[Path, None, None]:
    """
    Yields only file paths.

    Args:
        root_path(Path):
            Root path to walk through.

        filter_pattern(str):
            Unix path pattern for filtering retrieved paths.

        recursive(bool:
            Returns also paths of all sub folders.

    Yields:
        Path
    """
    path_generator = _get_path_generator(root_path=root_path, recursive=recursive)
    used_filter_pattern = _get_filter_pattern(filter_pattern)

    for child_path in path_generator(used_filter_pattern):
        if child_path.is_dir():
            continue
        yield child_path