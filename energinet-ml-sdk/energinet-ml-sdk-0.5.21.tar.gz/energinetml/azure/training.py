from azureml.core import Experiment, Run

from energinetml.core.training import AbstractTrainingContext

from .logger import AzureMlLogger
from .datasets import DownloadedAzureMLDataStore, MountedAzureMLDataStore


class AzureLocalTrainingContext(AbstractTrainingContext):
    def __init__(self, backend, force_download):
        """
        :param energinetml.azure.AzureBackend backend:
        :param bool force_download:
        """
        self.backend = backend
        self.force_download = force_download
        self.az_run = None

    def train_model(self, model, tags, **kwargs):
        az_workspace = self.backend.get_workspace(
            name=model.project.workspace_name,
            subscription_id=model.project.subscription_id,
            resource_group=model.project.resource_group,
        )

        az_experiment = Experiment(
            workspace=az_workspace,
            name=model.experiment,
        )

        datasets = DownloadedAzureMLDataStore.from_model(
            model=model,
            workspace=az_workspace,
            force_download=self.force_download,
        )

        with model.temporary_folder() as temp_path:
            # The "outputs" parameter is provided here with a non-existing
            # folder path to avoid having azureml upload files. We will do
            # this manually somewhere else.
            self.az_run = az_experiment.start_logging(
                snapshot_directory=temp_path,
                outputs='a-folder-that-does-not-exists',
            )
            self.az_run.set_tags(tags)
            try:
                return model.train(
                    datasets=datasets,
                    logger=AzureMlLogger(self.az_run),
                    **kwargs,
                )
            finally:
                self.az_run.complete()

    def save_output_files(self, model):
        self.az_run.upload_file('outputs/model.pkl', model.trained_model_path)

    def get_portal_url(self):
        return self.az_run.get_portal_url()


class AzureCloudTrainingContext(AbstractTrainingContext):
    def __init__(self):
        self.az_run = None

    def train_model(self, model, tags, **kwargs):
        self.az_run = Run.get_context(allow_offline=False)
        self.az_run.set_tags(tags)

        datasets = MountedAzureMLDataStore.from_model(
            model=model,
            workspace=self.az_run.experiment.workspace,
        )

        try:
            return model.train(
                datasets=datasets,
                logger=AzureMlLogger(self.az_run),
                **kwargs,
            )
        finally:
            self.az_run.complete()

    def save_output_files(self, model):
        pass

    def get_portal_url(self):
        return self.az_run.get_portal_url()
