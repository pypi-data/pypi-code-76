import logging
from os import environ
from pathlib import Path

from astropy.io import fits

from dkist_processing_common._util.globus import submit_globus_transfer
from dkist_processing_common._util.graphql import DatasetCatalogReceiptAccountMutation
from dkist_processing_common._util.graphql import graph_ql_client
from dkist_processing_common._util.message import publish_messages
from dkist_processing_common.base import SupportTaskBase


class TransferInputData(SupportTaskBase):
    """
    Changes the status of the recipe run to "INPROGRESS"
    Starts a globus transfer of all data listed in the associated input dataset to scratch
    """

    def run(self) -> None:
        self.change_status_to_in_progress()

        bucket = self.input_dataset(section="bucket")
        frames = self.input_dataset(section="frames")

        source_files = [Path("/", bucket, frame) for frame in frames]

        submit_globus_transfer(
            source_files=source_files,
            destination_files=[
                self.globus_path(self.input_dir, source_file.name) for source_file in source_files
            ],
            source_endpoint=environ.get("OBJECT_STORE_ENDPOINT"),
            destination_endpoint=environ.get("SCRATCH_ENDPOINT"),
        )


class TagInputData(SupportTaskBase):
    """
    Tags all input data with "INPUT" and whatever is listed in "DKIST004" in the headers
    """

    def run(self) -> None:
        input_file_paths = self.input_dir.glob("*.fits")
        for f in input_file_paths:
            header = fits.open(str(f))[0].header
            self.tag(str(f.resolve()), "INPUT")
            self.tag(str(f.resolve()), header["DKIST004"].upper())


class TransferOutputData(SupportTaskBase):
    """
    Transfers all data tagged as "OUTPUT" to the object store
    """

    def run(self) -> None:
        globus_output_paths = [self.globus_path(path) for path in self.output_paths]
        logging.info(f"{globus_output_paths=}")
        destination_files = [
            Path("/data", self.proposal_id, self.dataset_id, source_file.name)
            for source_file in globus_output_paths
        ]
        logging.info(f"{destination_files=}")

        submit_globus_transfer(
            source_files=globus_output_paths,
            destination_files=destination_files,
            source_endpoint=environ["SCRATCH_ENDPOINT"],
            destination_endpoint=environ["OBJECT_STORE_ENDPOINT"],
        )


class AddDatasetReceiptAccount(SupportTaskBase):
    """
    Creates a Dataset Catalog Receipt Account record populated with the number of objects
    """

    def run(self) -> None:
        expected_object_count = len(self.output_paths)
        graph_ql_client.execute_gql_mutation(
            mutation_base="createDatasetCatalogReceiptAccount",
            mutation_parameters=DatasetCatalogReceiptAccountMutation(
                datasetId=self.dataset_id, expectedObjectCount=expected_object_count
            ),
        )


class PublishCatalogMessages(SupportTaskBase):
    """
    Publishes a message for every object transferred to the object store
    """

    def run(self) -> None:
        destination_files = [
            Path("/data", self.proposal_id, self.dataset_id, source_file.name)
            for source_file in self.output_paths
        ]
        object_filepaths = [str(file[file.find(self.proposal_id) :]) for file in destination_files]
        messages = []
        for filepath in object_filepaths:
            if filepath.lower().endswith(".fits"):
                messages.append(self.create_frame_message(object_filepath=filepath))
            elif filepath.lower().endswith(".mp4"):
                messages.append(self.create_movie_message(object_filepath=filepath))
        publish_messages(messages=messages)


class Teardown(SupportTaskBase):
    """
    Changes the status of the recipe run to "COMPLETEDSUCCESSFULLY"
    Deletes the scratch directory containing all data from this pipeline run
    """

    def run(self) -> None:
        logging.info(f"Removing data and tags for recipe run {self.recipe_run_id}")
        self.change_status_to_completed_successfully()
        self.purge_file_system()
