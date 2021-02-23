from pathlib import Path

import pytest
from astropy.io import fits

from dkist_processing_common._util.graphql import CreateRecipeRunStatusResponse
from dkist_processing_common._util.graphql import InputDatasetResponse
from dkist_processing_common._util.graphql import ProcessingCandidateResponse
from dkist_processing_common._util.graphql import RecipeInstanceResponse
from dkist_processing_common._util.graphql import RecipeRunResponse
from dkist_processing_common._util.graphql import RecipeRunStatusResponse
from dkist_processing_common._util.scratch import WorkflowFileSystem


class FakeGQLClient:
    @staticmethod
    def execute_gql_query(**kwargs):
        query_base = kwargs["query_base"]

        if query_base == "recipeRunStatuses":
            return [RecipeRunStatusResponse(recipeRunStatusId=1)]
        if query_base == "recipeRuns":
            return [
                RecipeRunResponse(
                    recipeInstance=RecipeInstanceResponse(
                        processingCandidate=ProcessingCandidateResponse(
                            observingProgramExecutionId="abc", proposalId="123"
                        ),
                        inputDataset=InputDatasetResponse(
                            inputDatasetDocument='{"bucket": "bucket-name", "parameters": [{"parameterName": "", "parameterValues": [{"parameterValueId": 1, "parameterValue": "[[1,2,3],[4,5,6],[7,8,9]]", "parameterValueStartDate": "1/1/2000"}]}], "frames": ["objectKey1", "objectKey2", "objectKeyN"]}'
                        ),
                    )
                )
            ]

    @staticmethod
    def execute_gql_mutation(**kwargs):
        mutation_base = kwargs["mutation_base"]

        if mutation_base == "updateRecipeRun":
            return
        if mutation_base == "createRecipeRunStatus":
            return CreateRecipeRunStatusResponse(
                recipeRunStatus=RecipeRunStatusResponse(recipeRunStatusId=1)
            )


def test_change_status_to_in_progress(support_task, mocker):
    """
    Given: a support task
    When: requesting that the status of its recipe run is changed
    Then: the recipe run status changes
    """
    mocker.patch("dkist_processing_common._util.graphql.graph_ql_client", new=FakeGQLClient)
    support_task.change_status_to_in_progress()


def test_change_status_to_completed_successfully(support_task, mocker):
    """
    Given: a support task
    When: requesting that the status of its recipe run is changed
    Then: the recipe run status changes
    """
    mocker.patch("dkist_processing_common._util.graphql.graph_ql_client", new=FakeGQLClient)
    support_task.change_status_to_completed_successfully()


def test_input_dataset(support_task, mocker):
    """
    Given: a support task
    When: requesting an input data set
    Then: the input data set is returned either from a db query or local storage
    """
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    r_all = support_task.input_dataset()
    r_section = support_task.input_dataset(section="parameters")
    assert r_all["bucket"] == "bucket-name"
    assert len(r_all["frames"]) == 3
    assert r_section[0]["parameterValues"][0]["parameterValueId"] == 1
    assert r_section[0]["parameterValues"][0]["parameterValue"] == "[[1,2,3],[4,5,6],[7,8,9]]"
    assert r_section[0]["parameterValues"][0]["parameterValueStartDate"] == "1/1/2000"


def test_get_proposal_id(support_task, mocker):
    """
    Given: a support task
    When: the proposal id is requested
    Then: the proposal task is obtained via a db query and returned
    """
    mocker.patch("dkist_processing_common.base.graph_ql_client", new=FakeGQLClient)
    assert support_task.proposal_id == "123"


def test_frame_message(support_task):
    """
    Given: a support task
    When: a frame message is created
    Then: the components of the frame message are correctly populated
    """
    msg = support_task.create_frame_message(object_filepath="/test/object/path.ext")
    assert msg.objectName == "/test/object/path.ext"
    assert msg.conversationId == str(support_task.recipe_run_id)
    assert msg.bucket == "data"
    assert msg.incrementDatasetCatalogReceiptCount


def test_movie_message(support_task):
    """
    Given: a support task
    When: a movie message is created
    Then: the components of the movie message are correctly populated
    """
    msg = support_task.create_movie_message(object_filepath="/test/object/path.ext")
    assert msg.objectName == "/test/object/path.ext"
    assert msg.conversationId == str(support_task.recipe_run_id)
    assert msg.bucket == "data"
    assert msg.objectType == "MOVIE"
    assert msg.groupName == "DATASET"
    assert msg.incrementDatasetCatalogReceiptCount


def test_write_intermediate_fits(science_task, intermediate_fits, tmp_path):
    """
    Given: a fits file
    When: writing the file
    Then: the file exists
    """
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_intermediate_fits(
        data=intermediate_fits, datatype="TEST_WRITE", tags=["INT1", "INT2"]
    )
    assert Path(science_task._scratch.workflow_base_path, "TEST_WRITE.fits").exists()


def test_write_output_fits(science_task, output_fits, tmp_path):
    """
    Given: a fits file
    When: writing the file
    Then: the file exists
    """
    relative_path = "test_output.fits"
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_output_fits(
        data=output_fits, relative_path=relative_path, tags=["OUTPUT1", "OUTPUT2"]
    )
    assert Path(science_task._scratch.workflow_base_path, relative_path).exists()


def test_read_intermediate_fits(science_task, intermediate_fits, tmp_path):
    """
    Given: a type of file
    When: reading that file
    Then: the file is read correctly and the contents can be examined
    """
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_intermediate_fits(data=intermediate_fits, datatype="TEST_READ")
    hdul = science_task.read_intermediate_fits(datatype="TEST_READ")
    assert hdul[0].header["DKIST004"] == "TEST_INTERMEDIATE"


@pytest.mark.parametrize(
    "tags",
    [
        pytest.param(["INPUT", "DARK"], id="DARK"),
        pytest.param(["INPUT", "GAIN"], id="GAIN"),
        pytest.param(["INPUT", "TARGET"], id="TARGET"),
        pytest.param(["INPUT", "INSTPOLCAL"], id="INSTPOLCAL"),
        pytest.param(["INPUT", "TELPOLCAL"], id="TELPOLCAL"),
        pytest.param(["INPUT", "GEOMETRIC"], id="GEOMETRIC"),
    ],
)
def test_read_fits(science_task_with_inputs, tags):
    """
    Given: a type of file
    When: reading that file
    Then: the file is read correctly and the contents can be examined
    """
    frames = science_task_with_inputs.read_fits(tags=tags)
    frame = next(frames)
    assert frame[0].header["DKIST004"] == tags[1]


def test_input_dark_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_dark_frames
    frame = next(frames)
    assert frame[0].header["DKIST004"] == "DARK"


def test_input_gain_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_gain_frames
    frame = next(frames)
    assert frame[0].header["DKIST004"] == "GAIN"


def test_input_target_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_target_frames
    frame = next(frames)
    assert frame[0].header["DKIST004"] == "TARGET"


def test_input_instpolcal_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_instpolcal_frames
    frame = next(frames)
    assert frame[0].header["DKIST004"] == "INSTPOLCAL"


def test_input_telpolcal_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_telpolcal_frames
    frame = next(frames)
    assert frame[0].header["DKIST004"] == "TELPOLCAL"


def test_input_geometric_frames(science_task_with_inputs):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    frames = science_task_with_inputs.input_geometric_frames
    frame = next(frames)
    assert frame[0].header["DKIST004"] == "GEOMETRIC"


def test_intermediate_dark(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "DARK"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_dark(data=hdul)
    assert science_task.intermediate_dark[0].header["datatype"] == datatype


def test_intermediate_gain(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "GAIN"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_gain(data=hdul)
    assert science_task.intermediate_gain[0].header["datatype"] == datatype


def test_intermediate_target(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "TARGET"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_target(data=hdul)
    assert science_task.intermediate_target[0].header["datatype"] == datatype


def test_intermediate_instpolcal(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "INSTPOLCAL"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_instpolcal(data=hdul)
    assert science_task.intermediate_instpolcal[0].header["datatype"] == datatype


def test_intermediate_telpolcal(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "TELPOLCAL"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_telpolcal(data=hdul)
    assert science_task.intermediate_telpolcal[0].header["datatype"] == datatype


def test_intermediate_geometric(science_task, tmp_path):
    """
    Given: a specific type of input
    When: reading frames that match the input
    Then: the correct number of frames are read and the contents can be examined
    """
    datatype = "GEOMETRIC"
    hdu = fits.PrimaryHDU()
    hdu.header["datatype"] = datatype
    hdul = fits.HDUList([hdu])
    science_task._scratch = WorkflowFileSystem(scratch_base_path=tmp_path)
    science_task.write_geometric(data=hdul)
    assert science_task.intermediate_geometric[0].header["datatype"] == datatype


def test_input_dir(science_task, tmp_path):
    science_task._scratch = WorkflowFileSystem(
        scratch_base_path=tmp_path, recipe_run_id=science_task.recipe_run_id
    )
    assert science_task.input_dir == tmp_path / str(science_task.recipe_run_id) / "input"


def test_output_dir(science_task, tmp_path):
    science_task._scratch = WorkflowFileSystem(
        scratch_base_path=tmp_path, recipe_run_id=science_task.recipe_run_id
    )
    assert science_task.output_dir == tmp_path / str(science_task.recipe_run_id) / "output"


def test_globus_path(science_task, tmp_path):
    """
    Given: An instance of WorkflowFileSystem
    When: call globus path method
    Then: Retrieve path to recipe run id
    """
    science_task._scratch = WorkflowFileSystem(
        scratch_base_path=tmp_path, recipe_run_id=science_task.recipe_run_id
    )
    assert science_task.globus_path() == Path(f"{science_task.recipe_run_id}/")
    assert science_task.globus_path(science_task._scratch.workflow_base_path, "foo.txt") == Path(
        f"{science_task.recipe_run_id}/foo.txt"
    )


def test_output_paths(support_task_with_outputs):
    assert len(support_task_with_outputs.output_paths) == 10
