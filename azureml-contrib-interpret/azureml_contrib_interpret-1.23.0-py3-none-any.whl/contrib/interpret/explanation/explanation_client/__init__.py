# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Init file for azureml-contrib-interpret/azureml/contrib/interpret/explanation_client."""
from azureml.interpret import ExplanationClient as NewExplanationClient
from warnings import warn

__all__ = ["ExplanationClient"]


class ExplanationClient(NewExplanationClient):
    """Create the client used to interact with explanations and run history.

    :param service_context: Holder for service information.
    :type service_context: ServiceContext
    :param run_id: A GUID that represents a run.
    :type run_id: str
    :param _run: A run. If passed in, other args will be ignored.
    :type _run: azureml.core.run.Run
    """

    def __init__(self, service_context, experiment_name, run_id, _run=None):
        """Create the client used to interact with explanations and run history.

        :param service_context: Holder for service information.
        :type service_context: ServiceContext
        :param run_id: A GUID that represents a run.
        :type run_id: str
        :param _run: A run. If passed in, other args will be ignored.
        :type _run: azureml.core.run.Run
        """
        msg = 'Please use the explanation client from azureml-interpret package, this one will be deprecated'
        warn(msg, UserWarning)
        super(ExplanationClient, self).__init__(service_context, experiment_name, run_id, _run)
