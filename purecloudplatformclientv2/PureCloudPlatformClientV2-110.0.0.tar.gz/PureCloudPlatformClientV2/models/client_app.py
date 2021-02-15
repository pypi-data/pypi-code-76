# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class ClientApp(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ClientApp - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'integration_type': 'IntegrationType',
            'notes': 'str',
            'intended_state': 'str',
            'config': 'ClientAppConfigurationInfo',
            'reported_state': 'IntegrationStatusInfo',
            'attributes': 'dict(str, str)',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'integration_type': 'integrationType',
            'notes': 'notes',
            'intended_state': 'intendedState',
            'config': 'config',
            'reported_state': 'reportedState',
            'attributes': 'attributes',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._integration_type = None
        self._notes = None
        self._intended_state = None
        self._config = None
        self._reported_state = None
        self._attributes = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ClientApp.
        The globally unique identifier for the object.

        :return: The id of this ClientApp.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ClientApp.
        The globally unique identifier for the object.

        :param id: The id of this ClientApp.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ClientApp.
        The name of the integration, used to distinguish this integration from others of the same type.

        :return: The name of this ClientApp.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ClientApp.
        The name of the integration, used to distinguish this integration from others of the same type.

        :param name: The name of this ClientApp.
        :type: str
        """
        
        self._name = name

    @property
    def integration_type(self):
        """
        Gets the integration_type of this ClientApp.
        Type of the integration

        :return: The integration_type of this ClientApp.
        :rtype: IntegrationType
        """
        return self._integration_type

    @integration_type.setter
    def integration_type(self, integration_type):
        """
        Sets the integration_type of this ClientApp.
        Type of the integration

        :param integration_type: The integration_type of this ClientApp.
        :type: IntegrationType
        """
        
        self._integration_type = integration_type

    @property
    def notes(self):
        """
        Gets the notes of this ClientApp.
        Notes about the integration.

        :return: The notes of this ClientApp.
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """
        Sets the notes of this ClientApp.
        Notes about the integration.

        :param notes: The notes of this ClientApp.
        :type: str
        """
        
        self._notes = notes

    @property
    def intended_state(self):
        """
        Gets the intended_state of this ClientApp.
        Configured state of the integration.

        :return: The intended_state of this ClientApp.
        :rtype: str
        """
        return self._intended_state

    @intended_state.setter
    def intended_state(self, intended_state):
        """
        Sets the intended_state of this ClientApp.
        Configured state of the integration.

        :param intended_state: The intended_state of this ClientApp.
        :type: str
        """
        allowed_values = ["ENABLED", "DISABLED", "DELETED"]
        if intended_state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for intended_state -> " + intended_state)
            self._intended_state = "outdated_sdk_version"
        else:
            self._intended_state = intended_state

    @property
    def config(self):
        """
        Gets the config of this ClientApp.
        Configuration information for the integration.

        :return: The config of this ClientApp.
        :rtype: ClientAppConfigurationInfo
        """
        return self._config

    @config.setter
    def config(self, config):
        """
        Sets the config of this ClientApp.
        Configuration information for the integration.

        :param config: The config of this ClientApp.
        :type: ClientAppConfigurationInfo
        """
        
        self._config = config

    @property
    def reported_state(self):
        """
        Gets the reported_state of this ClientApp.
        Last reported status of the integration.

        :return: The reported_state of this ClientApp.
        :rtype: IntegrationStatusInfo
        """
        return self._reported_state

    @reported_state.setter
    def reported_state(self, reported_state):
        """
        Sets the reported_state of this ClientApp.
        Last reported status of the integration.

        :param reported_state: The reported_state of this ClientApp.
        :type: IntegrationStatusInfo
        """
        
        self._reported_state = reported_state

    @property
    def attributes(self):
        """
        Gets the attributes of this ClientApp.
        Read-only attributes for the integration.

        :return: The attributes of this ClientApp.
        :rtype: dict(str, str)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this ClientApp.
        Read-only attributes for the integration.

        :param attributes: The attributes of this ClientApp.
        :type: dict(str, str)
        """
        
        self._attributes = attributes

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ClientApp.
        The URI for this object

        :return: The self_uri of this ClientApp.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ClientApp.
        The URI for this object

        :param self_uri: The self_uri of this ClientApp.
        :type: str
        """
        
        self._self_uri = self_uri

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

