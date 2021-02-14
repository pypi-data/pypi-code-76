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


class V1beta1TransformerConfig(object):
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
        'default_image_version': 'str',
        'image': 'str'
    }

    attribute_map = {
        'default_image_version': 'defaultImageVersion',
        'image': 'image'
    }

    def __init__(self, default_image_version=None, image=None, local_vars_configuration=None):  # noqa: E501
        """V1beta1TransformerConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._default_image_version = None
        self._image = None
        self.discriminator = None

        self.default_image_version = default_image_version
        self.image = image

    @property
    def default_image_version(self):
        """Gets the default_image_version of this V1beta1TransformerConfig.  # noqa: E501

        default transformer docker image version  # noqa: E501

        :return: The default_image_version of this V1beta1TransformerConfig.  # noqa: E501
        :rtype: str
        """
        return self._default_image_version

    @default_image_version.setter
    def default_image_version(self, default_image_version):
        """Sets the default_image_version of this V1beta1TransformerConfig.

        default transformer docker image version  # noqa: E501

        :param default_image_version: The default_image_version of this V1beta1TransformerConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and default_image_version is None:  # noqa: E501
            raise ValueError("Invalid value for `default_image_version`, must not be `None`")  # noqa: E501

        self._default_image_version = default_image_version

    @property
    def image(self):
        """Gets the image of this V1beta1TransformerConfig.  # noqa: E501

        transformer docker image name  # noqa: E501

        :return: The image of this V1beta1TransformerConfig.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this V1beta1TransformerConfig.

        transformer docker image name  # noqa: E501

        :param image: The image of this V1beta1TransformerConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and image is None:  # noqa: E501
            raise ValueError("Invalid value for `image`, must not be `None`")  # noqa: E501

        self._image = image

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
        if not isinstance(other, V1beta1TransformerConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1beta1TransformerConfig):
            return True

        return self.to_dict() != other.to_dict()
