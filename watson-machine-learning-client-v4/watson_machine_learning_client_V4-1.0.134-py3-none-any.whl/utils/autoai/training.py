__all__ = [
    'is_run_id_exists'
]

from typing import Dict, Optional

from watson_machine_learning_client import WatsonMachineLearningAPIClient
from watson_machine_learning_client.wml_client_error import ApiRequestFailure


def is_run_id_exists(wml_credentials: Dict, run_id: str, space_id: Optional[str] = None) -> bool:
    """
    Check if specified run_id exists for WML client initialized with passed credentials.

    Parameters
    ----------
    wml_credentials: dictionary, required

    run_id: str, required
        Training run id of AutoAI experiment.

    space_id: str, optional
        Optional space id for WMLS and CP4D.
    """
    client = WatsonMachineLearningAPIClient(wml_credentials)

    if space_id is not None:
        client.set.default_space(space_id)

    try:
        client.training.get_details(run_id)

    except ApiRequestFailure as e:
        if 'Status code: 404' in str(e):
            return False

        else:
            raise e

    return True
