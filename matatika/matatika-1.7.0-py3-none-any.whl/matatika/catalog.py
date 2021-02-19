"""catalog module"""

import requests
from matatika.exceptions import (
    DatasetNotFoundError,
    MatatikaException,
    WorkspaceNotFoundError,
)
from matatika.types import DataFormat


class Catalog:
    """Class to handle client-side HTTP requests to the Matatika API"""

    def __init__(self, client):
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + client.auth_token
        }

        self.endpoint_url = client.endpoint_url
        self.workspaces_url = f'{self.endpoint_url}/workspaces'

        if client.workspace_id:
            self.workspace_id = str(client.workspace_id)
            self.datasets_url = f'{self.endpoint_url}/workspaces/{self.workspace_id}/datasets'

    def post_datasets(self, datasets):
        """Publishes a dataset into a workspace"""

        publish_responses = []

        for dataset in datasets:
            response = requests.post(
                self.datasets_url, headers=self.headers, data=dataset.to_json_str())

            if response.status_code == 400:
                raise MatatikaException(f"An error occurred while publishing dataset: "
                                        f"{response.json()['message']}")

            if response.status_code == 404:
                raise WorkspaceNotFoundError(
                    self.endpoint_url, self.workspace_id)

            response.raise_for_status()

            publish_responses.append(response)

        return publish_responses

    def get_workspaces(self):
        """Returns all workspaces the user profile is a member of"""

        response = requests.get(self.workspaces_url, headers=self.headers)
        response.raise_for_status()

        json_data = response.json()
        workspaces = {}

        if json_data['page']['totalElements'] > 0:
            workspaces = json_data['_embedded']['workspaces']

        return workspaces

    def get_datasets(self):
        """Returns all datasets in the supplied workspace"""

        response = requests.get(self.datasets_url, headers=self.headers)
        response.raise_for_status()

        json_data = response.json()
        datasets = {}

        if json_data['page']['totalElements'] > 0:
            datasets = json_data['_embedded']['datasets']

        return datasets

    def get_profile(self):
        """Returns the user profile"""

        response = requests.get(
            f'{self.endpoint_url}/profiles', headers=self.headers)
        response.raise_for_status()

        return response.json()['_embedded']['profiles'][0]

    def get_data(self, dataset_id, data_format: DataFormat):
        """Returns the data from a dataset"""

        if data_format is DataFormat.CSV:
            self.headers['Accept'] = 'text/csv'

        url = f'{self.endpoint_url}/datasets/{dataset_id}/data'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 404:
            raise DatasetNotFoundError(dataset_id, self.endpoint_url)

        response.raise_for_status()

        return response.text

    def get_dataset(self, dataset_id):
        """Returns a dataset"""

        url = f'{self.endpoint_url}/datasets/{dataset_id}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 404:
            raise DatasetNotFoundError(dataset_id, self.endpoint_url)

        response.raise_for_status()

        return response.json()

    def get_workspace_dataset(self, dataset_id_or_alias):
        """Returns a workspace dataset"""

        url = f'{self.endpoint_url}/workspaces/{self.workspace_id}/datasets/{dataset_id_or_alias}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 404:
            raise DatasetNotFoundError(dataset_id_or_alias, self.endpoint_url)

        response.raise_for_status()

        return response.json()

    def delete_dataset(self, dataset_id):
        """Deletes a dataset"""

        url = f'{self.endpoint_url}/datasets/{dataset_id}'
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 404:
            raise DatasetNotFoundError(dataset_id, self.endpoint_url)

        response.raise_for_status()

    def delete_workspace(self, workspace_id):
        """Deletes a workspace"""

        url = f'{self.endpoint_url}/workspaces/{workspace_id}'
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 404:
            raise WorkspaceNotFoundError(workspace_id, self.endpoint_url)

        response.raise_for_status()
