################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
import requests
from watson_machine_learning_client.utils import SPACES_DETAILS_TYPE, INSTANCE_DETAILS_TYPE, MEMBER_DETAILS_TYPE,DATA_ASSETS_DETAILS_TYPE, STR_TYPE, STR_TYPE_NAME, docstring_parameter, meta_props_str_conv, str_type_conv, get_file_from_cos
from watson_machine_learning_client.metanames import ConnectionMetaNames
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.wml_client_error import WMLClientError, ApiRequestFailure
import os

_DEFAULT_LIST_LENGTH = 0


class Connections(WMLResource):
    """
    Store and manage your Connections.

    """
    ConfigurationMetaNames = ConnectionMetaNames()
    """MetaNames for Connection creation."""

    def __init__(self, client):
        WMLResource.__init__(self, __name__, client)
        self._ICP = client.ICP

    def _get_required_element_from_response(self, response_data):

        WMLResource._validate_type(response_data, u'connection_response', dict)
        try:
            if self._client.default_space_id is not None:
                new_el = {'metadata': {'id': response_data['metadata']['asset_id'],
                                       'space_id': response_data['metadata']['space_id'],
                                       'asset_type': response_data['metadata']['asset_type'],
                                       'create_time': response_data['metadata']['create_time'],
                                       'last_access_time': response_data['metadata']['usage'].get('last_access_time')
                                       },
                          'entity': {
                              'datasource_type': response_data['entity']['datasource_type'],
                              'description': response_data['entity']['description'],
                              'name': response_data['entity']['name'],
                              'origin_country': response_data['entity']['origin_country'],
                              'owner_id': response_data['entity']['owner_id'],
                              'properties': response_data['entity']['properties']
                                }
                          }
            elif self._client.default_project_id is not None:
                if self._client.WSD:
                    # TODO :  There is no owner id in connection api response of WSD1.0, this might need a check in WSD2.0
                    # kaganesa: add the below line in 2.0
                    #  'owner_id': response_data['entity']['owner_id'],
                    new_el = {'metadata': {'id': response_data['metadata']['asset_id'],
                                           'project_id': response_data['metadata']['project_id'],
                                           'asset_type': response_data['metadata']['asset_type'],
                                           'create_time': response_data['metadata']['create_time'],
                                           'last_access_time': response_data['metadata']['usage'].get('last_access_time')
                                           },
                              'entity': {
                                  'datasource_type': response_data['entity']['datasource_type'],
                                  'description': response_data['entity']['description'],
                                  'name': response_data['entity']['name'],
                                  'origin_country': response_data['entity']['origin_country'],
                                 # 'owner_id': response_data['entity']['owner_id'],
                                  'properties': response_data['entity']['properties']
                               }
                              }


                else:
                    new_el = {'metadata': {'id': response_data['metadata']['asset_id'],
                                           'project_id': response_data['metadata']['project_id'],
                                           'asset_type': response_data['metadata']['asset_type'],
                                           'create_time': response_data['metadata']['create_time'],
                                           'last_access_time': response_data['metadata']['usage'].get('last_access_time')
                                           },
                              'entity': {
                                  'datasource_type': response_data['entity']['datasource_type'],
                                  'description': response_data['entity']['description'],
                                  'name': response_data['entity']['name'],
                                  'origin_country': response_data['entity']['origin_country'],
                                  'owner_id': response_data['entity']['owner_id'],
                                  'properties': response_data['entity']['properties']
                                  }
                              }

            return new_el
        except Exception as e:
            raise WMLClientError("Failed to read Response from down-stream service: " + response_data)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self, connection_id):
        """
            Get connection details for the given unique Connection id.

            **Parameters**

            .. important::
                #. **connection_id**: Unique id of Connection\n
                   **type**: str\n

            **Output**

            .. important::
                **returns**: Metadata of the stored Connection\n
                **return type**: dict\n

            **Example**

             >>> connection_details = client.connections.get_details(connection_id)

        """
        self._client._check_if_either_is_set()
        Connections._validate_type(connection_id, u'connection_id', STR_TYPE, True)

        if self._client.WSD:
            header_param = self._client._get_headers(wsdconnection_api_req=True)
        else:
            header_param = self._client._get_headers()

        if not self._client.ICP_30 and not self._client.ICP and not self._client.WSD:
            response = requests.get(self._href_definitions.get_connection_by_id_href(connection_id), params=self._client._params(),
                                    headers=header_param)
        else:
            response = requests.get(self._href_definitions.get_connection_by_id_href(connection_id), params=self._client._params(),
                                    headers=header_param, verify=False)
        if response.status_code == 200:
            return self._get_required_element_from_response(self._handle_response(200, u'get connection details', response))
        else:
            return self._handle_response(200, u'get connection details', response)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def create(self, meta_props):
        """
                Creates a connection.

                **Parameters**

                .. important::
                   #. **meta_props**:  meta data of the connection configuration. To see available meta names use:\n
                            >>> client.connections.ConfigurationMetaNames.get()

                      **type**: dict\n
                **Output**

                .. important::

                    **returns**: metadata of the stored connection\n
                    **return type**: dict\n

                **Example**
                     >>> connections_details = client.connections.create({
                     >>> client.connections.ConnectionsMetaNames.NAME: "dashdb connection",
                     >>> client.connections.ConnectionsMetaNames.DESCRIPTION: "connection description",
                     >>> client.connections.ConnectionsMetaNames.DATASOURCE_TYPE: "",
                     >>> client.connections.ConfigurationMetaNames.PROPERTIES: ""
                     >>> })

        """
        WMLResource._chk_and_block_create_update_for_python36(self)

        connection_meta = self.ConfigurationMetaNames._generate_resource_metadata(
            meta_props,
            with_validation=True,
            client=self._client
        )
        connection_meta.update({'origin_country': 'US'})
        #Step1  : Create an asset
        print("Creating connections...")

        if self._client.WSD:
            header_param = self._client._get_headers(wsdconnection_api_req=True)
        else:
            header_param = self._client._get_headers()

        if not self._client.ICP_30 and not self._client.ICP and not self._client.WSD:
            creation_response = requests.post(
                    self._href_definitions.get_connections_href(),
                    headers=header_param,
                    params = self._client._params(),
                    json=connection_meta
            )
        else:
            creation_response = requests.post(
                self._href_definitions.get_connections_href(),
                headers=header_param,
                json=connection_meta,
                params=self._client._params(),
                verify=False
            )

        connection_details = self._handle_response(201, u'creating new connection', creation_response)
        if creation_response.status_code == 201:
            connection_id = connection_details["metadata"]["asset_id"]
            print("SUCCESS")
            return self._get_required_element_from_response(connection_details)
        else:
            raise WMLClientError("Failed while creating a Connections. Try again.")

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, connection_id):
        """
            Delete a stored Connection.

            **Parameters**

            .. important::
                #. **connection_id**: Unique id of the connection to be deleted.\n
                   **type**: str\n

            **Output**

            .. important::
                **returns**: status ("SUCCESS" or "FAILED")\n
                **return type**: str\n

            **Example**

             >>> client.connections.delete(connection_id)

        """
        ##For CP4D, check if either spce or project ID is set
        self._client._check_if_either_is_set()

        pipeline_uid = str_type_conv(connection_id)
        Connections._validate_type(connection_id, u'connection_id', STR_TYPE, True)
        if self._client.WSD:
            header_param = self._client._get_headers(wsdconnection_api_req=True)
        else:
            header_param = self._client._get_headers()

        connection_endpoint = self._href_definitions.get_connection_by_id_href(connection_id)
        if not self._ICP and not self._client.ICP_30 and not self._client.WSD:
            response_delete = requests.delete(connection_endpoint, params=self._client._params(),
                                              headers=header_param)
        else:
            response_delete = requests.delete(connection_endpoint, params=self._client._params(),
                                              headers=header_param, verify=False)

        return self._handle_response(204, u'connection deletion', response_delete, False)

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid(connection_details):
        """
                Get Unique Id of stored connection.

                **Parameters**

                .. important::

                   #. **connection_details**:  Metadata of the stored connection\n
                      **type**: dict\n

                **Output**

                .. important::

                    **returns**: Unique Id of stored connection\n
                    **return type**: str\n

                **Example**


                 >>> connection_uid = client.connection.get_uid(connection_details)

        """
        Connections._validate_type(connection_details, u'connection_details', object, True)

        return WMLResource._get_required_element_from_dict(connection_details, u'connection_details',
                                                           [u'metadata', u'id'])

    def list_datasource_types(self):
        """
           List stored datasource types assets.


           **Output**

           .. important::
                This method only prints the list of datasources type in a table format.\n
                **return type**: None\n

           **Example**

            >>> client.connections.list_datasource_types()

        """

        if self._client.WSD:
            header_param = self._client._get_headers(wsdconnection_api_req=True)
        else:
            header_param = self._client._get_headers()

        if not self._client.ICP_30 and not self._client.ICP and not self._client.WSD:
            response = requests.get(self._href_definitions.get_connection_data_types_href(),
                                    headers=header_param)
        else:
            response = requests.get(self._href_definitions.get_connection_data_types_href(),
                                    headers=header_param, verify=False)

        datasource_details = self._handle_response(200, u'list datasource types', response)['resources']
        space_values = [
            (m[u'entity'][u'name'], m[u'metadata'][u'asset_id'], m[u'entity'][u'type'], m['entity']['status']) for
            m in datasource_details]

        self._list(space_values, [u'NAME', u'DATASOURCE_ID', u'TYPE', u'STATUS'], None, None)

    def list(self):
        """
           List all stored connections.

           **Output**

           .. important::
                This method only prints the list of all connections in a table format.\n
                **return type**: None\n

           **Example**

            >>> client.connections.list()

        """
        if self._client.WSD:
            header_param = self._client._get_headers(wsdconnection_api_req=True)
        else:
            header_param = self._client._get_headers()

        if not self._client.ICP_30 and not self._client.ICP and not self._client.WSD:
            response = requests.get(self._href_definitions.get_connections_href(),
                                    params=self._client._params(),
                                    headers=header_param)
        else:
            response = requests.get(self._href_definitions.get_connections_href(),
                                    params=self._client._params(),
                                    headers=header_param, verify=False)

        self._handle_response(200, u'list datasource type', response)

        datasource_details = self._handle_response(200, u'list datasource types', response)['resources']
        space_values = [
            (m[u'entity'][u'name'], m[u'metadata'][u'asset_id'],m['metadata']['create_time'], m[u'entity'][u'datasource_type']) for
            m in datasource_details]

        self._list(space_values, [u'NAME', u'ID', u'CREATED',  u'DATASOURCE_TYPE_ID', ], None, None)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_datasource_type_uid_by_name(self, name):
        """
           Get stored datasource types id for the given datasource type name.

           **Parameters**

           .. important::
                #. **name**:  name of datasource type\n
                   **type**: int\n

           **Output**

           .. important::
                This method only prints the id of given datasource type name.\n
                **return type**: Str\n

           **Example**

            >>> client.connections.get_datasource_type_uid_by_name('cloudobjectstorage')

        """
        Connections._validate_type(name, u'name', str, True)

        if self._client.WSD:
            header_param = self._client._get_headers(wsdconnection_api_req=True)
        else:
            header_param = self._client._get_headers()

        if not self._client.ICP_30 and not self._client.ICP and not self._client.WSD:
            response = requests.get(self._href_definitions.get_connection_data_types_href(),
                                    headers=header_param)
        else:
            response = requests.get(self._href_definitions.get_connection_data_types_href(),
                                    headers=header_param, verify=False)
        datasource_id = 'None'
        datasource_details = self._handle_response(200, u'list datasource types', response)['resources']
        for i, ds_resource in enumerate(datasource_details):
            if ds_resource['entity']['name'] == name:
                datasource_id = ds_resource['metadata']['asset_id']
        return datasource_id

