import filecmp
from nbcourse.utils import update_dict, get_functions, update_material
from nbcourse.nbcourse import NbCourse
import os
from pathlib import Path
from pprint import pprint
import pytest

TESTS_PATH = Path(__file__).parent.absolute()


def test_update_dict():

    cur = {'1-a': 1,
           '1-b': {'2-a': 2,
                   '2-b': {'3-a': 3}
                   }
           }
    new = {'1-a': 11,
           '1-c': 0,
           '1-b': {'2-b': {'3-a': 31},
                   '2-c': 0
                   },
           '1-d': {'2-d': 0}
           }

    update_dict(cur, new)

    ref = {'1-a': 11,
           '1-b': {'2-a': 2,
                   '2-b': {'3-a': 31},
                   '2-c': 0},
           '1-c': 0,
           '1-d': {'2-d': 0}}

    assert cur == ref


def test_get_functions():
    """Test function that collect all doit tasks"""
    tasks = {'output_dir', 'copy_material', 'copy_reveal', 'zip_chapters',
             'build_pages', 'execute_notebooks', 'convert_to_html',
             'convert_to_slides', 'build_book', 'zip_archive'}
    assert tasks.issubset(set(get_functions(NbCourse, 'task_(.*)')))


@pytest.fixture
def temporary_directory(tmpdir):
    """Create a sample nbcourse project"""
    p = tmpdir.mkdir("test_utils")
    os.chdir(p)
    os.mkdir("build")


def test_update_material(temporary_directory):
    """Check that a directory tree is updated"""
    src = TESTS_PATH / Path("sample/fig")
    dst = Path("build/fig")
    update_material(src, dst)
    cmp = filecmp.dircmp(src, dst)
    assert not cmp.diff_files


def test_update_material_file(temporary_directory):
    """Check that a single file is updated"""
    src = TESTS_PATH / Path("sample/exos/helloworld.py")
    dst = Path("build/exos/helloworld.py")
    update_material(src, dst)
    assert filecmp.cmp(src, dst)
