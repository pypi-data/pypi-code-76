# coding: utf-8

"""

    No descripton provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from pprint import pformat
from six import iteritems
import re


class PatchOperationExperiments(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, op=None, path=None, value=None, _from=None):
        """
        PatchOperationExperiments - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'op': 'str',
            'path': 'str',
            'value': 'object',
            '_from': 'str'
        }

        self.attribute_map = {
            'op': 'op',
            'path': 'path',
            'value': 'value',
            '_from': 'from'
        }

        self._op = op
        self._path = path
        self._value = value
        self.__from = _from

    @property
    def op(self):
        """
        Gets the op of this PatchOperationExperiments.
        operation

        :return: The op of this PatchOperationExperiments.
        :rtype: str
        """
        return self._op

    @op.setter
    def op(self, op):
        """
        Sets the op of this PatchOperationExperiments.
        operation

        :param op: The op of this PatchOperationExperiments.
        :type: str
        """
        allowed_values = ["add", "remove", "replace", "move", "copy", "test"]
        if op not in allowed_values:
            raise ValueError(
                "Invalid value for `op` ({0}), must be one of {1}"
                .format(op, allowed_values)
            )

        self._op = op

    @property
    def path(self):
        """
        Gets the path of this PatchOperationExperiments.
        path

        :return: The path of this PatchOperationExperiments.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this PatchOperationExperiments.
        path

        :param path: The path of this PatchOperationExperiments.
        :type: str
        """

        self._path = path

    @property
    def value(self):
        """
        Gets the value of this PatchOperationExperiments.


        :return: The value of this PatchOperationExperiments.
        :rtype: object
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this PatchOperationExperiments.


        :param value: The value of this PatchOperationExperiments.
        :type: object
        """

        self._value = value

    @property
    def _from(self):
        """
        Gets the _from of this PatchOperationExperiments.


        :return: The _from of this PatchOperationExperiments.
        :rtype: str
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """
        Sets the _from of this PatchOperationExperiments.


        :param _from: The _from of this PatchOperationExperiments.
        :type: str
        """

        self.__from = _from

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
