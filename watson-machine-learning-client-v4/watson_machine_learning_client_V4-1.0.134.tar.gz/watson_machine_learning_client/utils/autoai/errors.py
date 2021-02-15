__all__ = [
    "MissingPipeline",
    "FitNotCompleted",
    "FitNeeded",
    "AutoAIComputeError",
    "MissingAutoPipelinesParameters",
    "UseWMLClient",
    "PipelineNotLoaded",
    "MissingCOSStudioConnection",
    "MissingProjectLib",
    "LocalInstanceButRemoteParameter",
    "DataFormatNotSupported",
    "HoldoutSplitNotSupported",
    'LibraryNotCompatible',
    'CannotInstallLibrary',
    'InvalidCOSCredentials',
    'CannotDownloadTrainingDetails',
    'TShirtSizeNotSupported',
    'MissingPositiveLabel',
    'MissingDataPreprocessingStep',
    'CannotDownloadWMLPipelineDetails',
    'WrongDataJoinGraphNodeName',
    'NotInWatsonStudio',
    'WrongWMLServer',
    'CredentialsNotFound',
    'SetIDFailed',
    'MissingLocalAsset',
    'DataSourceSizeNotSupported',
    'TrainingDataSourceIsNotFile',
    'VisualizationFailed',
    'InvalidPredictionType'
]

from watson_machine_learning_client.utils import WMLClientError


class MissingPipeline(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"There is no such a Pipeline like: {value_name}", reason)


class FitNotCompleted(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"Fit run is not completed or the status is failed for run: {value_name}", reason)


class FitNeeded(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Fit run was not performed.", reason)


class AutoAIComputeError(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"Fit run failed for run_id: {value_name}.", reason)


class MissingAutoPipelinesParameters(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"AutoPipelines parameters are {value_name}", reason)


class UseWMLClient(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"Use WML v4 Client instead of {value_name}", reason)


class PipelineNotLoaded(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"Pipeline model: {value_name} cannot load.", reason)


class MissingCOSStudioConnection(WMLClientError, ValueError):
    def __init__(self, reason=None):
        WMLClientError.__init__(self, f"Missing COS Studio connection.", reason)


class MissingProjectLib(WMLClientError, ValueError):
    def __init__(self, reason=None):
        WMLClientError.__init__(self,
                                f"project-lib package missing in the environment, please make sure you are on Watson Studio"
                                f" and want to automatically initialize your COS connection."
                                f" If you want to initialize COS connection manually, do not use from_studio() method.",
                                reason)


class LocalInstanceButRemoteParameter(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Provided {value_name} parameter to local optimizer instance.", reason)


class DataFormatNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self,
                                f"This data format is not supported by SDK. (CSV and XLSX formats are supported.)",
                                reason)


class HoldoutSplitNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Holdout split is not supported for xlsx data.", reason)


class LibraryNotCompatible(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Library not compatible or missing!", reason)


class CannotInstallLibrary(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Library cannot be installed! Error: {value_name}", reason)


class InvalidCOSCredentials(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Wrong COS credentials!", reason)


class CannotDownloadTrainingDetails(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"Cannot download training details, training is not done yet. "
                                      f"Please try again after training is finished.", reason)


class TShirtSizeNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"This t-shirt size: \"{value_name}\" is not supported on this environment.",
                                reason)


class MissingPositiveLabel(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Missing positive label for \"{value_name}\"", reason)


class MissingDataPreprocessingStep(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Data preprocessing step not performed.", reason)


class CannotDownloadWMLPipelineDetails(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"Cannot download WML pipeline details ", reason)


class WrongDataJoinGraphNodeName(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"{value_name} is not a correct node name.", reason)


class NotInWatsonStudio(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Wrong environment.", reason)


class WrongWMLServer(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Wrong WML Server instance.", reason)


class CredentialsNotFound(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Cannot find WMLS credentials in WSD.", reason)


class SetIDFailed(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Cannot set {value_name}.", reason)


class MissingLocalAsset(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Local asset: {value_name} cannot be found.", reason)


class DataSourceSizeNotSupported(WMLClientError, ValueError):
    def __init__(self, reason=None):
        WMLClientError.__init__(self, f"The selected data source is too large for selected compute configuration "
                                      f"and might fail to run. Consider increasing the compute configuration", reason)


class TrainingDataSourceIsNotFile(WMLClientError, ValueError):
    def __init__(self, data_location=None, reason=None):
        WMLClientError.__init__(self, f"Training data location: {data_location} is a directory or does not exist."
                                      f"Please set training data location to dataset file location.", reason)


class VisualizationFailed(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Cannot perform visualization.", reason)


class InvalidPredictionType(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Cannot recognize prediction type: {value_name}", reason)
