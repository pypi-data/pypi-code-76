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

class ResponseConfig(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ResponseConfig - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'translation_map': 'dict(str, str)',
            'translation_map_defaults': 'dict(str, str)',
            'success_template': 'str',
            'success_template_uri': 'str'
        }

        self.attribute_map = {
            'translation_map': 'translationMap',
            'translation_map_defaults': 'translationMapDefaults',
            'success_template': 'successTemplate',
            'success_template_uri': 'successTemplateUri'
        }

        self._translation_map = None
        self._translation_map_defaults = None
        self._success_template = None
        self._success_template_uri = None

    @property
    def translation_map(self):
        """
        Gets the translation_map of this ResponseConfig.
        Map 'attribute name' and 'JSON path' pairs used to extract data from REST response.

        :return: The translation_map of this ResponseConfig.
        :rtype: dict(str, str)
        """
        return self._translation_map

    @translation_map.setter
    def translation_map(self, translation_map):
        """
        Sets the translation_map of this ResponseConfig.
        Map 'attribute name' and 'JSON path' pairs used to extract data from REST response.

        :param translation_map: The translation_map of this ResponseConfig.
        :type: dict(str, str)
        """
        
        self._translation_map = translation_map

    @property
    def translation_map_defaults(self):
        """
        Gets the translation_map_defaults of this ResponseConfig.
        Map 'attribute name' and 'default value' pairs used as fallback values if JSON path extraction fails for specified key.

        :return: The translation_map_defaults of this ResponseConfig.
        :rtype: dict(str, str)
        """
        return self._translation_map_defaults

    @translation_map_defaults.setter
    def translation_map_defaults(self, translation_map_defaults):
        """
        Sets the translation_map_defaults of this ResponseConfig.
        Map 'attribute name' and 'default value' pairs used as fallback values if JSON path extraction fails for specified key.

        :param translation_map_defaults: The translation_map_defaults of this ResponseConfig.
        :type: dict(str, str)
        """
        
        self._translation_map_defaults = translation_map_defaults

    @property
    def success_template(self):
        """
        Gets the success_template of this ResponseConfig.
        Velocity template to build response to return from Action.

        :return: The success_template of this ResponseConfig.
        :rtype: str
        """
        return self._success_template

    @success_template.setter
    def success_template(self, success_template):
        """
        Sets the success_template of this ResponseConfig.
        Velocity template to build response to return from Action.

        :param success_template: The success_template of this ResponseConfig.
        :type: str
        """
        
        self._success_template = success_template

    @property
    def success_template_uri(self):
        """
        Gets the success_template_uri of this ResponseConfig.
        URI to retrieve success template.

        :return: The success_template_uri of this ResponseConfig.
        :rtype: str
        """
        return self._success_template_uri

    @success_template_uri.setter
    def success_template_uri(self, success_template_uri):
        """
        Sets the success_template_uri of this ResponseConfig.
        URI to retrieve success template.

        :param success_template_uri: The success_template_uri of this ResponseConfig.
        :type: str
        """
        
        self._success_template_uri = success_template_uri

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

