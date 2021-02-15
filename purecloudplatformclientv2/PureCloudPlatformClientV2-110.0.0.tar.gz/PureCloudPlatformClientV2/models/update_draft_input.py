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

class UpdateDraftInput(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        UpdateDraftInput - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'category': 'str',
            'name': 'str',
            'config': 'ActionConfig',
            'contract': 'ActionContractInput',
            'secure': 'bool',
            'version': 'int'
        }

        self.attribute_map = {
            'category': 'category',
            'name': 'name',
            'config': 'config',
            'contract': 'contract',
            'secure': 'secure',
            'version': 'version'
        }

        self._category = None
        self._name = None
        self._config = None
        self._contract = None
        self._secure = None
        self._version = None

    @property
    def category(self):
        """
        Gets the category of this UpdateDraftInput.
        Category of action, Can be up to 256 characters long

        :return: The category of this UpdateDraftInput.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this UpdateDraftInput.
        Category of action, Can be up to 256 characters long

        :param category: The category of this UpdateDraftInput.
        :type: str
        """
        
        self._category = category

    @property
    def name(self):
        """
        Gets the name of this UpdateDraftInput.
        Name of action, Can be up to 256 characters long

        :return: The name of this UpdateDraftInput.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UpdateDraftInput.
        Name of action, Can be up to 256 characters long

        :param name: The name of this UpdateDraftInput.
        :type: str
        """
        
        self._name = name

    @property
    def config(self):
        """
        Gets the config of this UpdateDraftInput.
        Configuration to support request and response processing

        :return: The config of this UpdateDraftInput.
        :rtype: ActionConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """
        Sets the config of this UpdateDraftInput.
        Configuration to support request and response processing

        :param config: The config of this UpdateDraftInput.
        :type: ActionConfig
        """
        
        self._config = config

    @property
    def contract(self):
        """
        Gets the contract of this UpdateDraftInput.
        Action contract

        :return: The contract of this UpdateDraftInput.
        :rtype: ActionContractInput
        """
        return self._contract

    @contract.setter
    def contract(self, contract):
        """
        Sets the contract of this UpdateDraftInput.
        Action contract

        :param contract: The contract of this UpdateDraftInput.
        :type: ActionContractInput
        """
        
        self._contract = contract

    @property
    def secure(self):
        """
        Gets the secure of this UpdateDraftInput.
        Indication of whether or not the action is designed to accept sensitive data

        :return: The secure of this UpdateDraftInput.
        :rtype: bool
        """
        return self._secure

    @secure.setter
    def secure(self, secure):
        """
        Sets the secure of this UpdateDraftInput.
        Indication of whether or not the action is designed to accept sensitive data

        :param secure: The secure of this UpdateDraftInput.
        :type: bool
        """
        
        self._secure = secure

    @property
    def version(self):
        """
        Gets the version of this UpdateDraftInput.
        Version of current Draft

        :return: The version of this UpdateDraftInput.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this UpdateDraftInput.
        Version of current Draft

        :param version: The version of this UpdateDraftInput.
        :type: int
        """
        
        self._version = version

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

