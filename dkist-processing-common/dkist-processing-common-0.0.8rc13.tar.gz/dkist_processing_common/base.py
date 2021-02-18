"""
Wrappers for all workflow tasks
"""
import json
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Generator
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from astropy.io import fits
from dkist_processing_core import TaskBase

from dkist_processing_common._util.graphql import add_new_recipe_run_status
from dkist_processing_common._util.graphql import apply_status_id_to_recipe_run
from dkist_processing_common._util.graphql import get_message_status_query
from dkist_processing_common._util.graphql import graph_ql_client
from dkist_processing_common._util.graphql import RecipeRunInputDatasetQuery
from dkist_processing_common._util.graphql import RecipeRunResponse
from dkist_processing_common._util.interservice_bus import CatalogFrameMessage
from dkist_processing_common._util.interservice_bus import CatalogObjectMessage
from dkist_processing_common._util.scratch import WorkflowFileSystem


class TaskBaseExt(TaskBase, ABC):
    """
    Wrapper for all tasks. Contains the data access layer.
    """

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
        is_task_manual: bool = False,
        apm_client_config: Optional[dict] = None,
    ):
        self._scratch = WorkflowFileSystem(
            recipe_run_id=recipe_run_id, task_name=self.__class__.__name__
        )
        super().__init__(
            recipe_run_id, workflow_name, workflow_version, is_task_manual, apm_client_config
        )

    def tag(self, path: Union[Path, str], tags: Union[Iterable[str], str]) -> None:
        """
        Wrapper for the tag method in WorkflowFileSystem
        """
        return self._scratch.tag(path=path, tags=tags)

    @property
    def input_dataset_path(self) -> Path:
        """
        Path to the input dataset in scratch
        """
        return self._scratch.workflow_base_path / "input_dataset.json"

    def purge_file_system(self) -> None:
        """
        Wrapper for the purge method in WorkflowFileSystem
        """
        self._scratch.purge()

    def globus_path(self, *args) -> Path:
        """
        Return the Path to the root of a Globus transfer for the instance of the WorkflowFileSystem
        :param args: ordered list of path elements
        :return: Path to the root of a Globus transfer for the instance of the WorkflowFileSystem
        """
        if not args:
            return self._scratch.workflow_base_path.relative_to(self._scratch.scratch_base_path)
        path = Path(*args)
        return path.relative_to(self._scratch.scratch_base_path)

    @property
    def input_dir(self) -> Path:
        """
        Path to the 'input' dir in scratch
        """
        return self._scratch.workflow_base_path / "input"

    @property
    def output_dir(self) -> Path:
        """
        Path to the 'output' dir in scratch
        """
        return self._scratch.workflow_base_path / "output"

    @property
    def output_paths(self) -> List:
        """
        Paths of all objects tagged as "OUTPUT"
        """
        return list(self._scratch.find_all(tags=["OUTPUT"]))

    def input_dataset(self, section: str = "all") -> Union[dict, None]:
        """
        Input dataset document for the recipe run
        """
        if not self.input_dataset_path.exists():
            # Get input dataset from db
            input_dataset_response = graph_ql_client.execute_gql_query(
                query_base="recipeRuns",
                query_response_cls=RecipeRunResponse,
                query_parameters=RecipeRunInputDatasetQuery(recipeRunId=self.recipe_run_id),
            )
            # Write document to disk for future use
            self._write_input_dataset(
                input_dataset_response[0].recipeInstance.inputDataset.inputDatasetDocument
            )

        input_dataset_document = self._read_input_dataset()

        section = section.lower()
        if section == "all":
            return input_dataset_document
        return input_dataset_document.get(section, None)

    def _write_input_dataset(self, input_dataset):
        """
        Interface for writing the input dataset document to scratch
        """
        self._scratch.write(
            bytes(input_dataset, "utf-8"), self.input_dataset_path.parts[-1], tags=["INPUTDATASET"]
        )

    def _read_input_dataset(self) -> dict:
        """
        Interface for reading the input dataset document from scratch
        """
        with self.input_dataset_path.open("r") as f:
            return json.loads(f.read())

    def read_input_fits(self, datatype: str) -> Generator[fits.HDUList, None, None]:
        """
        Get paths for all data tagged with "INPUT" and the datatype requested
        """
        return self.read_fits(tags=["INPUT", datatype.upper()])

    def write_intermediate_fits(
        self, data: fits.HDUList, datatype: str, tags: Optional[List] = None
    ) -> None:
        """
        Write a calibration product tagged with "INTERMEDIATE", the datatype supplied,
        and any extra tags supplied
        """
        relative_path = f"{datatype}.fits"
        full_tags = ["INTERMEDIATE", datatype.upper()]
        if tags:
            for tag in tags:
                full_tags.append(tag)
        self._scratch.write_fits(data=data, relative_path=relative_path, tags=full_tags)

    def write_output_fits(
        self, data: fits.HDUList, relative_path: Union[str, Path], tags: Optional[List] = None
    ) -> None:
        """
        Write an output frame tagged with "OUTPUT", "OBSERVE", "L1", and any extra tags supplied
        """
        # TODO how are filenames determined for output data?
        full_tags = ["OUTPUT", "OBSERVE", "L1"]
        if tags:
            for tag in tags:
                full_tags.append(tag)
        self._scratch.write_fits(data=data, relative_path=relative_path, tags=full_tags)

    def read_intermediate_fits(self, datatype: str):
        """
        Get paths for all data tagged with "INTERMEDIATE" and the datatype requested
        """
        try:
            paths = self._scratch.find_all(["INTERMEDIATE", datatype.upper()])
            filepath = next(paths)
        except StopIteration:
            raise FileNotFoundError(f"No files found of type {datatype}")
        try:
            next(paths)
        except StopIteration:
            return fits.open(filepath)
        raise RuntimeError(f"More than one file found of type {datatype}")

    def read_fits(self, tags: Union[List, str]):
        filepaths = self._scratch.find_all(tags=tags)
        return (fits.open(filepath) for filepath in filepaths)

    def write_movie(
        self, data
    ):  # TODO Write this method and potentially move it to the movie writing class in 'common'
        pass


class SupportTaskBase(TaskBaseExt, ABC):
    """
    Wrapper for all support tasks (tasks that do not impact the data)
    """

    recipe_run_statuses = {
        "INPROGRESS": "Recipe run is currently undergoing processing",
        "COMPLETEDSUCCESSFULLY": "Recipe run processing completed with no errors",
    }

    def change_status_to_in_progress(self):
        """
        Set the recipe run status to "INPROGRESS"
        """
        self._change_status(status="INPROGRESS", is_complete=False)

    def change_status_to_completed_successfully(self):
        """
        Set the recipe run status to "COMPLETEDSUCCESSFULLY"
        """
        self._change_status(status="COMPLETEDSUCCESSFULLY", is_complete=True)

    def _change_status(self, status: str, is_complete: bool):
        """
        Change the recipe run status of a recipe run to the given status
        """
        status_response = get_message_status_query(status=status)

        # If the status was found
        if len(status_response) > 0:
            # Get the status ID
            recipe_run_status_id = status_response[0].recipeRunStatusId
        else:
            # Add the status to the db and get the new status ID
            recipe_run_status_id = add_new_recipe_run_status(status=status, is_complete=is_complete)

        apply_status_id_to_recipe_run(
            recipe_run_status_id=recipe_run_status_id, recipe_run_id=self.recipe_run_id
        )

    @property
    def proposal_id(self) -> str:
        """
        Get the proposal id of the current recipe run
        """
        try:
            getattr(self, "_proposal_id")
        except AttributeError:
            self._proposal_id = graph_ql_client.execute_gql_query(
                query_base="recipeRuns",
                query_response_cls=RecipeRunResponse,
                query_parameters=RecipeRunInputDatasetQuery(recipeRunId=self.recipe_run_id),
            )[0].recipeInstance.processingCandidate.proposalId
        return self._proposal_id

    def create_frame_message(self, object_filepath: str):
        catalog_frame_message = CatalogFrameMessage(
            objectName=object_filepath, conversationId=str(self.recipe_run_id)
        )
        return catalog_frame_message

    def create_movie_message(self, object_filepath: str):
        catalog_movie_message = CatalogObjectMessage(
            objectType="MOVIE",
            objectName=object_filepath,
            groupId=self.dataset_id,
            conversationId=str(self.recipe_run_id),
        )
        return catalog_movie_message


class ScienceTaskL0ToL1(TaskBaseExt):
    """
    Wrapper for all science tasks creating L1 data from L0 raw inputs
    """

    def record_provenance(self):
        pass  # TODO

    @property
    def input_dark_frames(self) -> Generator[fits.HDUList, None, None]:
        """
        Get the list of input dark frames
        """
        return self.read_input_fits(datatype="DARK")

    @property
    def input_gain_frames(self) -> Generator[fits.HDUList, None, None]:
        """
        Get the list of input gain frames
        """
        return self.read_input_fits(datatype="GAIN")

    @property
    def input_target_frames(self) -> Generator[fits.HDUList, None, None]:
        """
        Get the list of input target frames
        """
        return self.read_input_fits(datatype="TARGET")

    @property
    def input_instpolcal_frames(self) -> Generator[fits.HDUList, None, None]:
        """
        Get the list of input instpolcal frames
        """
        return self.read_input_fits(datatype="INSTPOLCAL")

    @property
    def input_telpolcal_frames(self) -> Generator[fits.HDUList, None, None]:
        """
        Get the list of input telpolcal frames
        """
        return self.read_input_fits(datatype="TELPOLCAL")

    @property
    def input_geometric_frames(self) -> Generator[fits.HDUList, None, None]:
        """
        Get the list of input geometric frames
        """
        return self.read_input_fits(datatype="GEOMETRIC")

    def write_dark(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        """
        Write the calibrated dark frame
        """
        self.write_intermediate_fits(data=data, datatype="DARK", tags=tags)

    def write_gain(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        """
        Write the calibrated gain frame
        """
        self.write_intermediate_fits(data=data, datatype="GAIN", tags=tags)

    def write_target(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        """
        Write the calibrated target frame
        """
        self.write_intermediate_fits(data=data, datatype="TARGET", tags=tags)

    def write_instpolcal(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        """
        Write the calibrated instpolcal frame
        """
        self.write_intermediate_fits(data=data, datatype="INSTPOLCAL", tags=tags)

    def write_telpolcal(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        """
        Write the calibrated telpolcal frame
        """
        self.write_intermediate_fits(data=data, datatype="TELPOLCAL", tags=tags)

    def write_geometric(self, data: fits.HDUList, tags: Optional[List] = None) -> None:
        """
        Write the calibrated geometric frame
        """
        self.write_intermediate_fits(data=data, datatype="GEOMETRIC", tags=tags)

    @property
    def intermediate_dark(self) -> fits.HDUList:
        """
        Get the calibrated dark frame
        """
        return self.read_intermediate_fits(datatype="DARK")

    @property
    def intermediate_gain(self) -> fits.HDUList:
        """
        Get the calibrated gain frame
        """
        return self.read_intermediate_fits(datatype="GAIN")

    @property
    def intermediate_target(self) -> fits.HDUList:
        """
        Get the calibrated target frame
        """
        return self.read_intermediate_fits(datatype="TARGET")

    @property
    def intermediate_instpolcal(self) -> fits.HDUList:
        """
        Get the calibrated instpolcal frame
        """
        return self.read_intermediate_fits(datatype="INSTPOLCAL")

    @property
    def intermediate_telpolcal(self) -> fits.HDUList:
        """
        Get the calibrated telpolcal frame
        """
        return self.read_intermediate_fits(datatype="TELPOLCAL")

    @property
    def intermediate_geometric(self) -> fits.HDUList:
        """
        Get the calibrated geometric frame
        """
        return self.read_intermediate_fits(datatype="GEOMETRIC")

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method that must be overridden to execute the desired DAG task.
        """
