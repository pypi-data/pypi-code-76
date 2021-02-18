from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, List
from pathwalker import walk_folder_paths, walk_file_paths
from doctestprinter import EditingItem


_test_file_paths = [
    "file0.txt",
    "file0.png",
    "sub1/file1.txt",
    "sub1/file1.png",
    "sub2/file2.txt",
    "sub2/file2.png",
    "sub1/sub11/file11.txt",
    "sub1/sub11/file11.png",
]


_temp_test_dir: Optional[TemporaryDirectory] = None
_temp_test_dir_path: Optional[Path] = None


def relative_to_temp_path(temp_path: Path) -> str:
    global _temp_test_dir_path
    return str(temp_path.relative_to(_temp_test_dir_path))


def sort_paths(walker) -> List[Path]:
    return list(sorted(walker, key=lambda x: str(x)))


make_relative = EditingItem(editor=relative_to_temp_path)


def setup_module(module: Optional = None):
    """
    setup any state specific to the execution of the given module.
    """
    global _temp_test_dir
    global _temp_test_dir_path
    _temp_test_dir = TemporaryDirectory()
    _temp_test_dir_path = Path(_temp_test_dir.name)

    for test_path in _test_file_paths:
        full_test_path = _temp_test_dir_path.joinpath(test_path)
        full_test_path.parent.mkdir(parents=True, exist_ok=True)
        full_test_path.touch()


def teardown_module(module: Optional = None):
    """
    teardown any state that was previously setup with a setup_module method.
    """
    global _temp_test_dir
    assert _temp_test_dir is not None
    _temp_test_dir.cleanup()
    assert not _temp_test_dir_path.exists()


def test_walk_folders_without_recursion():
    """
    >>> from doctestprinter import doctest_iter_print, EditingItem
    >>> walked_test_paths = test_walk_folders_without_recursion()
    >>> doctest_iter_print(walked_test_paths, edits_item=make_relative)
    sub1
    sub2
    """
    global _temp_test_dir_path
    return sort_paths(walk_folder_paths(root_path=_temp_test_dir_path, recursive=False))


def test_walk_folders_with_recursion():
    """
    >>> from doctestprinter import doctest_iter_print, EditingItem
    >>> make_relative = EditingItem(editor=relative_to_temp_path)
    >>> walked_test_paths = test_walk_folders_with_recursion()
    >>> doctest_iter_print(walked_test_paths, edits_item=make_relative)
    sub1
    sub1/sub11
    sub2
    """
    global _temp_test_dir_path
    return sort_paths(walk_folder_paths(root_path=_temp_test_dir_path, recursive=True))


def test_walk_folders_with_recursion_and_1_only():
    """
    >>> from doctestprinter import doctest_iter_print, EditingItem
    >>> make_relative = EditingItem(editor=relative_to_temp_path)
    >>> walked_test_paths = test_walk_folders_with_recursion_and_1_only()
    >>> doctest_iter_print(walked_test_paths, edits_item=make_relative)
    sub1
    sub1/sub11
    """
    global _temp_test_dir_path
    return sort_paths(
        walk_folder_paths(
            root_path=_temp_test_dir_path, filter_pattern="*1", recursive=True
        )
    )


def test_walk_files_without_recursion():
    """
    >>> from doctestprinter import doctest_iter_print, EditingItem
    >>> walked_test_paths = test_walk_files_without_recursion()
    >>> doctest_iter_print(walked_test_paths, edits_item=make_relative)
    file0.png
    file0.txt
    """
    global _temp_test_dir_path
    return sort_paths(walk_file_paths(root_path=_temp_test_dir_path, recursive=False))


def test_walk_files_with_recursion():
    """
    >>> from doctestprinter import doctest_iter_print, EditingItem
    >>> make_relative = EditingItem(editor=relative_to_temp_path)
    >>> walked_test_paths = test_walk_files_with_recursion()
    >>> doctest_iter_print(walked_test_paths, edits_item=make_relative)
    file0.png
    file0.txt
    sub1/file1.png
    sub1/file1.txt
    sub1/sub11/file11.png
    sub1/sub11/file11.txt
    sub2/file2.png
    sub2/file2.txt
    """
    global _temp_test_dir_path
    return sort_paths(walk_file_paths(root_path=_temp_test_dir_path, recursive=True))


def test_walk_files_with_recursion_and_txt_only():
    """
    >>> from doctestprinter import doctest_iter_print, EditingItem
    >>> make_relative = EditingItem(editor=relative_to_temp_path)
    >>> walked_test_paths = test_walk_files_with_recursion_and_txt_only()
    >>> doctest_iter_print(walked_test_paths, edits_item=make_relative)
    file0.txt
    sub1/file1.txt
    sub1/sub11/file11.txt
    sub2/file2.txt
    """
    global _temp_test_dir_path
    return sort_paths(
        walk_file_paths(
            root_path=_temp_test_dir_path, filter_pattern="*.txt", recursive=True
        )
    )