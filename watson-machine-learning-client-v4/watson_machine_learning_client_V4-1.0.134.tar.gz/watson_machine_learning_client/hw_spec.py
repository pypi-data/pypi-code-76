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
from watson_machine_learning_client.utils import SPACES_DETAILS_TYPE, INSTANCE_DETAILS_TYPE, MEMBER_DETAILS_TYPE,HW_SPEC_DETAILS_TYPE, STR_TYPE, STR_TYPE_NAME, docstring_parameter, meta_props_str_conv, str_type_conv, get_file_from_cos
from watson_machine_learning_client.metanames import HwSpecMetaNames
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.wml_client_error import WMLClientError, ApiRequestFailure
import os,json

_DEFAULT_LIST_LENGTH = 50


class HwSpec(WMLResource):
    """
    Store and manage your hardware specs.
    """
    ConfigurationMetaNames = HwSpecMetaNames()
    """MetaNames for Hardware Specification."""

    def __init__(self, client):
        WMLResource.__init__(self, __name__, client)
        self._ICP = client.ICP

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self, hw_spec_uid):
        """
            Get hardware specification details.

            **Parameters**

            .. important::
                **hw_spec_uid** : Unique id of the hardware spec
                ** type**: str

            **Output**

            .. important::
                **returns**: Metadata of the hardware specifications\n
                **return type**: dict\n of hw_spec\n

            **Example**

                 >>> hw_spec_details = client.hardware_specifications.get_details(hw_spec_uid)

        """
        HwSpec._validate_type(hw_spec_uid, u'hw_spec_uid', STR_TYPE, True)
        if not self._ICP:
            response = requests.get(self._href_definitions.get_hw_spec_href(hw_spec_uid), params=self._client._params(),
                                    headers=self._client._get_headers())
        else:
            response = requests.get(self._href_definitions.get_hw_spec_href(hw_spec_uid), params=self._client._params(),
                                      headers=self._client._get_headers(), verify=False)
        if response.status_code == 200:
            return self._get_required_element_from_response(self._handle_response(200, u'get hardware spec details', response))
        else:
            return self._handle_response(200, u'get hardware spec details', response)

    # Creation of new hardware specs is not required at the moment because WML does not support it
    # @docstring_parameter({'str_type': STR_TYPE_NAME})
    # def store(self, meta_props):
    #     """
    #             Create a space.
    #
    #             **Parameters**
    #
    #             .. important::
    #                #. **meta_props**:  meta data of the space configuration. To see available meta names use:\n
    #                                 >>> client.hardware_specifications.ConfigurationMetaNames.get()
    #
    #                   **type**: dict\n
    #
    #             **Output**
    #
    #             .. important::
    #
    #                 **returns**: metadata of the stored space\n
    #                 **return type**: dict\n
    #
    #             **Example**
    #
    #              >>> meta_props = {
    #              >>>    client.hardware_specifications.ConfigurationMetaNames.NAME: "skl_pipeline_heart_problem_prediction",
    #              >>>    client.hardware_specifications.ConfigurationMetaNames.DESCRIPTION: "description scikit-learn_0.20",
    #              >>>    client.hardware_specifications.ConfigurationMetaNames.HARDWARE_CONFIGURATIONS: {},
    #              >>> }
    #
    #     """
    #
    #     # quick support for COS credentials instead of local path
    #     # TODO add error handling and cleaning (remove the file)
    #     HwSpec._validate_type(meta_props, u'meta_props', dict, True)
    #     hw_spec_meta = self.ConfigurationMetaNames._generate_resource_metadata(
    #         meta_props,
    #         with_validation=True,
    #         client=self._client)
    #
    #     hw_spec_meta_json = json.dumps(hw_spec_meta)
    #     href = self._href_definitions.get_hw_specs_href()
    #
    #     if not self._ICP:
    #         creation_response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(), data=hw_spec_meta_json)
    #     else:
    #         creation_response = requests.post(href, params=self._client._params(), headers=self._client._get_headers(), data=hw_spec_meta_json, verify=False)
    #
    #     hw_spec_details = self._handle_response(201, u'creating new hw specs', creation_response)
    #
    #     return hw_spec_details


    def list(self,name=None):
        """
           List hardware specifications.

           **Parameters**

           .. important::
                #. **type**: int\n

           **Output**

           .. important::
                This method only prints the list of all assets in a table format.\n
                **return type**: None\n

           **Example**

            >>> client.hardware_specifications.list()

        """

        # Todo provide api to return
        href = self._href_definitions.get_hw_specs_href()
        # Todo include space_id/project_id once https://github.ibm.com/ax/planning/issues/7493 is fixed
        if not self._ICP:
            response = requests.get(href, headers=self._client._get_headers())
        else:
            response = requests.get(href, headers=self._client._get_headers(), verify=False)
        self._handle_response(200, u'list hw_specs', response)
        asset_details = self._handle_response(200, u'list assets', response)["resources"]
        hw_spec_values = [
            (m[u'metadata'][u'name'], m[u'metadata'][u'asset_id'], m[u'metadata'][u'description']) for
            m in asset_details]
        self._list(hw_spec_values, [u'NAME', u"ID", u'DESCRIPTION'], None, _DEFAULT_LIST_LENGTH)


    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid(hw_spec_details):
        """
                Get UID of hardware specifications asset.

                **Parameters**

                .. important::

                   #. **asset_details**:  Metadata of the hardware specifications \n
                      **type**: dict\n
                      **type**: dict\n

                **Output**

                .. important::

                    **returns**: Unique Id of hardware specifications\n
                    **return type**: str\n

                **Example**

                 >>> asset_uid = client.hardware_specifications.get_uid(hw_spec_details)

        """
        HwSpec._validate_type(hw_spec_details, u'hw_spec_details', object, True)
        HwSpec._validate_type_of_details(hw_spec_details, HW_SPEC_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(hw_spec_details, u'hw_spec_details',
                                                           [u'metadata', u'asset_id'])


    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_href(hw_spec_details):
        """
            Get url of hardware specifications.

           **Parameters**

           .. important::
                #. **hw_spec_details**:  hardware specifications details\n
                   **type**: dict\n

           **Output**

           .. important::
                **returns**: href of hardware specifications\n
                **return type**: str\n

           **Example**

             >>> hw_spec_details = client.hw_spec.get_details(hw_spec_uid)
             >>> hw_spec_href = client.hw_spec.get_href(hw_spec_details)

        """
        HwSpec._validate_type(hw_spec_details, u'hw_spec_details', object, True)
        HwSpec._validate_type_of_details(hw_spec_details, HW_SPEC_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(hw_spec_details, u'hw_spec_details', [u'metadata', u'href'])

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid_by_name(self, hw_spec_name):
        """
                Get Unique Id of hardware specification for the given name.

                **Parameters**

                .. important::

                   #. **hw_spec_name**:  name of the hardware spec \n
                      **type**: str\n

                **Output**

                .. important::

                    **returns**: Unique Id of hardware specification \n
                    **return type**: str\n

                **Example**

                 >>> asset_uid = client.hardware_specifications.get_uid_by_name(hw_spec_name)

        """
        HwSpec._validate_type(hw_spec_name, u'hw_spec_name', STR_TYPE, True)
        parameters = self._client._params()
        parameters.update(name=hw_spec_name)
        if not self._ICP:
            response = requests.get(self._href_definitions.get_hw_specs_href(),
                                    params=parameters,
                                    headers=self._client._get_headers())
        else:
            response = requests.get(self._href_definitions.get_hw_specs_href(),
                                    params=parameters,
                                    headers=self._client._get_headers(), verify=False)
        if response.status_code == 200:
            total_values = self._handle_response(200, u'list assets', response)["total_results"]
            if total_values != 0:
                hw_spec_details = self._handle_response(200, u'list assets', response)["resources"]
                return hw_spec_details[0][u'metadata'][u'asset_id']
            else:
                return "Not Found"

    # @docstring_parameter({'str_type': STR_TYPE_NAME})
    # def delete(self, hw_spec_uid):
    #     """
    #         Delete a hardware specifications.
    #
    #         **Parameters**
    #
    #         .. important::
    #             #. **hw_spec_uid**:  hardware specifications UID\n
    #                **type**: str\n
    #
    #         **Output**
    #
    #         .. important::
    #             **returns**: status ("SUCCESS" or "FAILED")\n
    #             **return type**: str\n
    #
    #         **Example**
    #
    #          >>> client.hw_spec.delete(hw_spec_uid)
    #     """
    #     HwSpec._validate_type(hw_spec_uid, u'hw_spec_uid', STR_TYPE, True)
    #
    #     if not self._ICP:
    #         response = requests.delete(self._href_definitions.get_hw_spec_href(hw_spec_uid), params=self._client._params(),
    #                                 headers=self._client._get_headers())
    #     else:
    #         response = requests.delete(self._href_definitions.get_hw_spec_href(hw_spec_uid), params=self._client._params(),
    #                                   headers=self._client._get_headers(), verify=False)
    #     if response.status_code == 200:
    #         return self._get_required_element_from_response(response.json())
    #     else:
    #         return self._handle_response(204, u'delete hardware specification', response)
    #

    def _get_required_element_from_response(self, response_data):

        WMLResource._validate_type(response_data, u'hw_spec_response', dict)
        try:
            if self._client.default_space_id is not None:
                new_el = {'metadata': {
                                       'name': response_data['metadata']['name'],
                                       'asset_id': response_data['metadata']['asset_id'],
                                       'href': response_data['metadata']['href'],
                                       'asset_type': response_data['metadata']['asset_type'],
                                       'created_at': response_data['metadata']['created_at']
                                       #'updated_at': response_data['metadata']['updated_at']
                                       },
                          'entity': response_data['entity']

                          }
            elif self._client.default_project_id is not None:
                if self._client.WSD:

                    href = "/v2/assets/" + response_data['metadata']['asset_id'] + "?" + "project_id=" + response_data['metadata']['project_id']

                    new_el = {'metadata': {
                                           'name': response_data['metadata']['name'],
                                           'asset_id': response_data['metadata']['asset_id'],
                                           'href': response_data['metadata']['href'],
                                           'asset_type': response_data['metadata']['asset_type'],
                                           'created_at': response_data['metadata']['created_at']
                                           },
                              'entity': response_data['entity']

                              }
                else:
                    new_el = {'metadata': {
                                           'name': response_data['metadata']['name'],
                                           'asset_id': response_data['metadata']['asset_id'],
                                           'href': response_data['metadata']['href'],
                                           'asset_type': response_data['metadata']['asset_type'],
                                           'created_at': response_data['metadata']['created_at']
                                       },
                             'entity': response_data['entity']

                            }
            return new_el
        except Exception as e:
            raise WMLClientError("Failed to read Response from down-stream service: " + response_data.text)
