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


class HyperParametersExperimentsIntRange(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, min_value=None, max_value=None, step=None, power=None):
        """
        HyperParametersExperimentsIntRange - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'min_value': 'int',
            'max_value': 'int',
            'step': 'int',
            'power': 'float'
        }

        self.attribute_map = {
            'min_value': 'min_value',
            'max_value': 'max_value',
            'step': 'step',
            'power': 'power'
        }

        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._power = power

    @property
    def min_value(self):
        """
        Gets the min_value of this HyperParametersExperimentsIntRange.


        :return: The min_value of this HyperParametersExperimentsIntRange.
        :rtype: int
        """
        return self._min_value

    @min_value.setter
    def min_value(self, min_value):
        """
        Sets the min_value of this HyperParametersExperimentsIntRange.


        :param min_value: The min_value of this HyperParametersExperimentsIntRange.
        :type: int
        """

        self._min_value = min_value

    @property
    def max_value(self):
        """
        Gets the max_value of this HyperParametersExperimentsIntRange.


        :return: The max_value of this HyperParametersExperimentsIntRange.
        :rtype: int
        """
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        """
        Sets the max_value of this HyperParametersExperimentsIntRange.


        :param max_value: The max_value of this HyperParametersExperimentsIntRange.
        :type: int
        """

        self._max_value = max_value

    @property
    def step(self):
        """
        Gets the step of this HyperParametersExperimentsIntRange.


        :return: The step of this HyperParametersExperimentsIntRange.
        :rtype: int
        """
        return self._step

    @step.setter
    def step(self, step):
        """
        Sets the step of this HyperParametersExperimentsIntRange.


        :param step: The step of this HyperParametersExperimentsIntRange.
        :type: int
        """

        self._step = step

    @property
    def power(self):
        """
        Gets the power of this HyperParametersExperimentsIntRange.


        :return: The power of this HyperParametersExperimentsIntRange.
        :rtype: float
        """
        return self._power

    @power.setter
    def power(self, power):
        """
        Sets the power of this HyperParametersExperimentsIntRange.


        :param power: The power of this HyperParametersExperimentsIntRange.
        :type: float
        """

        self._power = power

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
