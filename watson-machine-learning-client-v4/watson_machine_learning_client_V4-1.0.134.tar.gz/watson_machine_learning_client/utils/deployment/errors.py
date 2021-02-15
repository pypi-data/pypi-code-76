__all__ = [
    "WrongDeploymnetType",
    "ModelTypeNotSupported",
    "NotAutoAIExperiment",
    "EnvironmentNotSupported",
    'BatchJobFailed',
    'MissingScoringResults',
    'ModelStoringFailed',
    'DeploymentNotSupported'
]

from watson_machine_learning_client.utils import WMLClientError


class WrongDeploymnetType(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This deployment is not of type: {value_name} ", reason)


class ModelTypeNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This model type is not supported yet: {value_name} ", reason)


class NotAutoAIExperiment(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This experiment_run_id is not from an AutoAI experiment: {value_name} ", reason)


class EnvironmentNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name, reason=None):
        WMLClientError.__init__(self, f"This environment is not supported: {value_name}", reason)


class BatchJobFailed(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Batch job failed for job: {value_name}", reason)


class MissingScoringResults(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Scoring of deployment job: {value_name} not completed.", reason)


class ModelStoringFailed(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Model: {value_name} store failed.", reason)


class DeploymentNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name=None, reason=None):
        WMLClientError.__init__(self, f"Deployment of type: {value_name} is not supported.", reason)
