# Copyright 2020 kubeflow.org.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    KFServing

    Python SDK for KFServing  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kfserving.configuration import Configuration


class V1beta1ExplainersConfig(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'aix': 'V1beta1ExplainerConfig',
        'alibi': 'V1beta1ExplainerConfig',
        'art': 'V1beta1ExplainerConfig'
    }

    attribute_map = {
        'aix': 'aix',
        'alibi': 'alibi',
        'art': 'art'
    }

    def __init__(self, aix=None, alibi=None, art=None, local_vars_configuration=None):  # noqa: E501
        """V1beta1ExplainersConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._aix = None
        self._alibi = None
        self._art = None
        self.discriminator = None

        if aix is not None:
            self.aix = aix
        if alibi is not None:
            self.alibi = alibi
        if art is not None:
            self.art = art

    @property
    def aix(self):
        """Gets the aix of this V1beta1ExplainersConfig.  # noqa: E501


        :return: The aix of this V1beta1ExplainersConfig.  # noqa: E501
        :rtype: V1beta1ExplainerConfig
        """
        return self._aix

    @aix.setter
    def aix(self, aix):
        """Sets the aix of this V1beta1ExplainersConfig.


        :param aix: The aix of this V1beta1ExplainersConfig.  # noqa: E501
        :type: V1beta1ExplainerConfig
        """

        self._aix = aix

    @property
    def alibi(self):
        """Gets the alibi of this V1beta1ExplainersConfig.  # noqa: E501


        :return: The alibi of this V1beta1ExplainersConfig.  # noqa: E501
        :rtype: V1beta1ExplainerConfig
        """
        return self._alibi

    @alibi.setter
    def alibi(self, alibi):
        """Sets the alibi of this V1beta1ExplainersConfig.


        :param alibi: The alibi of this V1beta1ExplainersConfig.  # noqa: E501
        :type: V1beta1ExplainerConfig
        """

        self._alibi = alibi

    @property
    def art(self):
        """Gets the art of this V1beta1ExplainersConfig.  # noqa: E501


        :return: The art of this V1beta1ExplainersConfig.  # noqa: E501
        :rtype: V1beta1ExplainerConfig
        """
        return self._art

    @art.setter
    def art(self, art):
        """Sets the art of this V1beta1ExplainersConfig.


        :param art: The art of this V1beta1ExplainersConfig.  # noqa: E501
        :type: V1beta1ExplainerConfig
        """

        self._art = art

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1beta1ExplainersConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1beta1ExplainersConfig):
            return True

        return self.to_dict() != other.to_dict()
