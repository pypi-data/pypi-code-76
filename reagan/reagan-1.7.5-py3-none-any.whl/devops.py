#!/usr/bin/python
from reagan.subclass import Subclass
import pandas as pd
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class DevOpsAPI(Subclass):
    def __init__(self):
        super().__init__()
        self.organization = self.get_parameter("devops").get_parameter('organization')
        self.personal_access_token = self.get_parameter("devops").get_parameter('personal_access_token')
        self._connect(self.organization, self.personal_access_token)

    def _connect(self, organization, personal_access_token):

        # Create a connection to the org
        credentials = BasicAuthentication('', personal_access_token)
        connection = Connection(base_url=f'https://dev.azure.com/{organization}', creds=credentials)

        # Get a client (the "core" client provides access to projects, teams, etc)
        self.core_client = connection.clients.get_core_client()

    def to_df(self, obj):
        response = eval(f'self.core_client.get_{obj}()')
        r = response.value
        return pd.DataFrame(list(map(lambda x: x.as_dict(), r)))

if __name__ == "__main__":
    dva = DevOpsAPI()
    df = dva.to_df(obj = 'projects')

# from azure.devops.connection import Connection
# from msrest.authentication import BasicAuthentication
# import pprint





# # Fill in with your personal access token and org URL
# personal_access_token = '3kckmnwaxml32fplorsnva5m54mo42zuhdghlp5p5fovwfeiadaa'
# organization_url = 'https://dev.azure.com/GMDataOps'

# # Create a connection to the org
# credentials = BasicAuthentication('', personal_access_token)
# connection = Connection(base_url=organization_url, creds=credentials)

# # Get a client (the "core" client provides access to projects, teams, etc)
# core_client = connection.clients.get_core_client()

# # Get the first page of projects
# get_projects_response = core_client.get_projects()
# # index = 0
# # while get_projects_response is not None:
# #     for project in get_projects_response.value:
# #         pprint.pprint("[" + str(index) + "] " + project.name)
# #         index += 1
# #     if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
# #         # Get the next page of projects
# #         get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
# #     else:
# #         # All projects have been retrieved
# #         get_projects_response = None