"""
Global test fixtures
"""
from pathlib import Path
from random import randint
from typing import Tuple

import pytest
from astropy.io import fits

from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common._util.tags import TagDB
from dkist_processing_common.base import ScienceTaskL0ToL1
from dkist_processing_common.base import SupportTaskBase


@pytest.fixture(scope="function")
def support_task():
    """
    Create task class for usage in tests
    """

    class TaskClass(SupportTaskBase):
        def run(self) -> None:
            pass

    i = randint(0, 1000000000)

    task = TaskClass(
        recipe_run_id=i,
        workflow_name=f"workflow_name_{i}",
        workflow_version=f"version{i}",
    )

    yield task

    task._scratch.purge()


@pytest.fixture(scope="function")
def science_task():
    """
    Create task class for usage in tests
    """

    class TaskClass(ScienceTaskL0ToL1):
        def run(self) -> None:
            pass

    i = randint(0, 1000000000)

    task = TaskClass(
        recipe_run_id=i,
        workflow_name=f"workflow_name_{i}",
        workflow_version=f"version{i}",
    )

    yield task

    task._scratch.purge()


@pytest.fixture(scope="function")
def science_task_with_inputs(science_task, tmp_path):
    datatypes = ["DARK", "GAIN", "TARGET", "INSTPOLCAL", "TELPOLCAL", "GEOMETRIC"]
    for datatype in datatypes:
        hdu = fits.PrimaryHDU()
        hdu.header["DKIST004"] = datatype
        hdul = fits.HDUList([hdu])
        science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        science_task._scratch.write_fits(hdul, f"{datatype}.fits", tags=["INPUT", datatype])
    return science_task


@pytest.fixture(scope="function")
def support_task_with_outputs(support_task, tmp_path):
    paths = [f"output/{i}.fits" for i in range(10)]
    for path in paths:
        hdu = fits.PrimaryHDU()
        hdul = fits.HDUList([hdu])
        support_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
        support_task._scratch.write_fits(hdul, path, tags=["OUTPUT"])
    return support_task


@pytest.fixture(scope="session")
def input_dark_fits():
    hdu = fits.PrimaryHDU()
    hdu.header["DKIST004"] = "DARK"
    return fits.HDUList([hdu])


@pytest.fixture(scope="session")
def intermediate_fits():
    hdu = fits.PrimaryHDU()
    hdu.header["DKIST004"] = "TEST_INTERMEDIATE"
    return fits.HDUList([hdu])


@pytest.fixture(scope="session")
def output_fits():
    hdu = fits.PrimaryHDU()
    hdu.header["DKIST004"] = "OBSERVE"
    return fits.HDUList([hdu])


@pytest.fixture()
def recipe_run_id():
    return randint(0, 99999)


@pytest.fixture()
def tag_db(recipe_run_id) -> TagDB:
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags")
    yield t
    t.purge()
    t.close()


@pytest.fixture()
def tag_db2(recipe_run_id) -> TagDB:
    """
    Another instance of a tag db in the same redis db
    """
    recipe_run_id = recipe_run_id + 15  # same db number but different namespace
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags2")
    yield t
    t.purge()
    t.close()


@pytest.fixture(params=[None, "use_tmp_path"])
def workflow_file_system(request, recipe_run_id, tmp_path) -> Tuple[WorkflowFileSystem, int, Path]:
    if request.param == "use_tmp_path":
        path = tmp_path
    else:
        path = request.param
    wkflow_fs = WorkflowFileSystem(
        recipe_run_id=recipe_run_id,
        task_name="wkflow_fs_test",
        scratch_base_path=path,
    )
    yield wkflow_fs, recipe_run_id, tmp_path
    wkflow_fs.purge()
    tmp_path.rmdir()
    wkflow_fs.close()
