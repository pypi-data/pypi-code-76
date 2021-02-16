import nbcourse
from nbcourse.initialize import initialize, SKEL_PATH
import contextlib
from pathlib import Path
import os


def test_initialize(tmpdir):
    """Test if initialize function creates the right project skeleton"""
    # Get skeleton content
    skeleton_paths = set((path.relative_to(SKEL_PATH)
                          for path in SKEL_PATH.glob('**/*')))

    # Create a temporary project dir
    p = tmpdir.mkdir("test_project")
    os.chdir(p)

    # Initialize and compare
    initialize()
    paths = set((path.relative_to(p) for path in Path(p).glob('**/*')))
    assert paths == skeleton_paths
