__all__ = [
    'get_project',
    'get_wmls_credentials_and_space_ids',
    'get_iam_token',
    'get_project_environments_details',
    'create_spark_header',
    'change_client_get_headers'
]

import base64
import json
from typing import Any, Dict, Tuple, List, TYPE_CHECKING

import requests

from watson_machine_learning_client.href_definitions import IAM_TOKEN_API, HrefDefinitions
from watson_machine_learning_client.wml_client_error import ApiRequestFailure
from .errors import NotInWatsonStudio, CredentialsNotFound

if TYPE_CHECKING:
    from watson_machine_learning_client.workspace import WorkSpace


def get_project() -> Any:
    """Try to import project_lib and get user corresponding project."""
    try:
        from project_lib import Project

    except ModuleNotFoundError:
        raise NotInWatsonStudio(reason="You are not in Watson Studio or Watson Studio Desktop environment. "
                                       "Cannot access to project metadata.")

    try:
        access = Project.access()

    except RuntimeError:
        raise CredentialsNotFound(reason="Your WSD environment does not have correctly configured "
                                         "connection to WML Server or you are not in WSD environment. "
                                         "In that case, please provide WMLS credentials and space_id.")

    return access


def get_wmls_credentials_and_space_ids(local_path: str) -> Tuple[List[Dict], List[str]]:
    """
    Parse project.json file and get WMLS credentials associated with WSD project.

    Parameters
    ----------
    local_path: str, required
        Path to project.json file with project configuration in WSD.

    Returns
    -------
    Two lists with WMLS credentials and corresponding space_ids.
    """
    try:
        with open(local_path, 'r') as f:
            data = json.load(f)

        credentials = [instance['credentials'] for instance in data['compute']]
        for instance in credentials:
            instance['version'] = "2.0"
            instance['instance_id'] = "wml_local"
            instance['password'] = base64.decodebytes(bytes(instance['password'].encode())).decode()

        space_ids = [instance['properties']['space_guid'] for instance in data['compute']]

    except (FileNotFoundError, KeyError):
        raise CredentialsNotFound(reason="Your WSD environment does not have correctly configured "
                                         "connection to WML Server or you are not in WSD environment. "
                                         "In that case, please provide WMLS credentials and space_id.")

    return credentials, space_ids


def get_iam_token(workspace: 'WorkSpace') -> str:
    """
    Fetch IAM token for given workspace.

    Parameters
    ----------
    workspace: WorkSpace, required

    Returns
    -------
    String with IAM token
    """
    _href_definitions = HrefDefinitions(workspace.wml_client.wml_credentials)
    try:
        iam_api_key = workspace.wml_credentials['iam_api_key']

    except KeyError:
        raise AttributeError("You need to pass an IAM api key in WML credentials "
                             "to be able to run multiple files preprocessing step.")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic Yng6Yng='
    }
    data = f"apikey={IAM_TOKEN_API.format(iam_api_key)}"

    response = requests.post(
        url=_href_definitions.get_iam_token_url(),
        data=data,
        headers=headers
    )

    if response.status_code == 200:
        token = response.json().get(u'access_token')
    else:
        raise ApiRequestFailure(u'Error during getting IAM Token.', response)
    return token


def create_ws_env_url(workspace: 'WorkSpace') -> str:
    """Make url to Watson Studio Environments.

    Parameters
    ----------
    workspace: WorkSpace, required

    Returns
    -------
    str with url
    """
    if workspace.project_id is None:
        raise ValueError("Missing project_id. It is required to pass project_id from Watson Studio "
                         "for Data Join + AutoAI training and deployment.")

    if 'test' in workspace.wml_credentials['url']:
        url = f'https://api.dataplatform.dev.cloud.ibm.com/v2/environments?project_id={workspace.project_id}'

    else:
        url = f'https://api.dataplatform.cloud.ibm.com/v2/environments?project_id={workspace.project_id}'

    return url


def get_project_environments_details(workspace: 'WorkSpace') -> Dict:
    """
    Fetch environments details related to user project in Watson Studio.

    Parameters
    ----------
    workspace: WorkSpace, required

    Returns
    -------
    Dictionary with environments details.
    """
    token = get_iam_token(workspace)
    url = create_ws_env_url(workspace)

    headers = {
        'Authorization': f"Bearer {token}",
        'X-WML-User-Client': 'PythonClient',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        url=url,
        headers=headers
    )

    if response.status_code == 200:
        return response.json()

    else:
        raise ApiRequestFailure(u'Getting project environment details failed.', response)


def create_spark_header(environments_details: Dict, workspace: 'WorkSpace') -> str:
    """Creates header with spark environment."""
    env_guid = None

    for resource in environments_details['resources']:
        if 'spark24scala' == resource['metadata']['name']:
            env_guid = resource['metadata']['asset_id']

    if env_guid is None:
        raise ValueError("Cannot find spark environment guid.")

    token = get_iam_token(workspace)
    url = create_ws_env_url(workspace)
    url = f"{url.split('?project_id')[0]}/{env_guid}/access_info?project_id={workspace.project_id}"

    headers = {
        'Authorization': f"Bearer {token}",
        'X-WML-User-Client': 'PythonClient',
        'Content-Type': 'application/json'
    }

    response = requests.get(
        url=url,
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()

    else:
        raise ApiRequestFailure(u'Getting spark access details failed.', response)

    spark_header = {
        "credentials": {
            "host": data['entity']['url'].split('/')[2],
            "instance_id": data['entity']['instance_id'],
            "api_key": data['entity']['api_key']
        },
        "kernel_id": data['entity']['url'].split('/')[4]
    }

    # note: encode spark header with base64
    spark_header = json.dumps(spark_header)
    spark_header = base64.encodebytes(bytes(spark_header.encode()))
    spark_header = spark_header.replace(b'\n', b'')
    spark_header = spark_header.decode()
    # --- end note

    return spark_header


def change_client_get_headers(client: 'WatsonMachineLearningAPIClient', _type: str, workspace: 'WorkSpace'):
    """Replace client _get_headers() method body with new one (including spark header)."""

    from types import MethodType
    from watson_machine_learning_client import WatsonMachineLearningAPIClient

    def _get_headers_new(self, content_type='application/json', no_content_type=False,
                         spark_header=create_spark_header(get_project_environments_details(workspace), workspace)):
        if self.WSD:
            headers = {'X-WML-User-Client': 'PythonClient'}
            if self.project_id is not None:
                headers.update({'X-Watson-Project-ID': self.project_id})
            if not no_content_type:
                headers.update({'Content-Type': content_type})
        else:
            if self.proceed is True:
                token = "Bearer " + self.wml_credentials["token"]
            else:
                token = "Bearer " + self.service_instance._get_token()
            headers = {
                'Authorization': token,
                'X-WML-User-Client': 'PythonClient'
            }
            if self._is_IAM() or (self.service_instance._is_iam() is None):
                headers['ML-Instance-ID'] = self.wml_credentials['instance_id']

            headers.update({'x-wml-internal-switch-to-new-v4': "true"})
            if not self.ICP:
                # headers.update({'x-wml-internal-switch-to-new-v4': "true"})
                if self.project_id is not None:
                    headers.update({'X-Watson-Project-ID': self.project_id})

            if not no_content_type:
                headers.update({'Content-Type': content_type})

        headers["X-SparkHB-Service-Instance"] = spark_header

        return headers

    if _type == 'new':
        client._get_headers = MethodType(_get_headers_new, client)

    else:
        client._get_headers = MethodType(WatsonMachineLearningAPIClient._get_headers, client)
