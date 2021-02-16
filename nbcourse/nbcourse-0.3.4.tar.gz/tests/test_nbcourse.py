from nbcourse.initialize import initialize
from nbcourse.nbcourse import NbCourse, MyDoitMain, ClassTaskLoader
from nbcourse.utils import get_functions
from nbcourse.main import get_help_epilog
import pytest
from pathlib import Path
import os
from distutils.dir_util import copy_tree


TESTS_PATH = Path(__file__).parent.absolute()
MINI_CONF = {'nb': {'dir': 'sample'}}


def test_get_help_epilog():
    """Test get_help_epilog function for CLI"""
    get_help_epilog()


def _create_project(tmpdir, sample=Path('sample')):
    """Create a sample nbcourse project"""
    p = tmpdir.mkdir("test_project")
    os.chdir(p)
    initialize()

    # Create a link to sample notebooks
    nb = Path(sample)
    nb.symlink_to(TESTS_PATH / sample, target_is_directory=True)

    # Create a link to sample yaml file
    yaml_file = Path('nbcourse.yml')
    yaml_file.unlink()
    yaml_file.symlink_to(TESTS_PATH / sample / 'nbcourse.yml')


@pytest.fixture
def create_project(tmpdir):
    _create_project(tmpdir)


@pytest.fixture
def create_wrong_project(tmpdir):
    _create_project(tmpdir, sample=Path('wrong_sample'))


def test_minimal_nbcourse(create_project):
    """Only test nbcourse object instantiation"""
    NbCourse()


@pytest.mark.parametrize('task', get_functions(NbCourse, 'task_(.*)'))
def test_minimal_nbcourse_build(create_project, task):
    """test nbcourse on list of doit tasks returned by get_functions"""
    course = NbCourse(MINI_CONF)
    assert course.build(["-n 4", task]) == 0


def test_nbcourse(create_project):
    """Test sample with nbcourse.yml sample file"""
    NbCourse(Path('nbcourse.yml'))


def test_nbcourse_build(create_project):
    """Test sample build with nbcourse.yml sample file"""
    course = NbCourse(Path('nbcourse.yml'))
    course.conf['book']
    assert course.build(["-n 4"]) == 0


def test_nbcourse_clean(create_project):
    """Test sample build then clean with nbcourse.yml sample file"""
    course = NbCourse(Path('nbcourse.yml'))
    course.conf['book']
    course.build(["-n 4"])
    course.build(["clean"])


def test_nbcourse_wrong_build(create_wrong_project):
    """Test sample build with nbcourse.yml sample file"""
    course = NbCourse(Path('nbcourse.yml'))
    course.conf['book']
    ret = 0
    try:
        ret = course.build(["-n 4"])
    except SystemExit:
        ret = 2
    except AssertionError:
        ret = 2
    assert ret == 2
