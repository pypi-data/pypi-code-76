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

class DocumentListing(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DocumentListing - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'entities': 'list[KnowledgeDocument]',
            'next_uri': 'str',
            'self_uri': 'str',
            'previous_uri': 'str'
        }

        self.attribute_map = {
            'entities': 'entities',
            'next_uri': 'nextUri',
            'self_uri': 'selfUri',
            'previous_uri': 'previousUri'
        }

        self._entities = None
        self._next_uri = None
        self._self_uri = None
        self._previous_uri = None

    @property
    def entities(self):
        """
        Gets the entities of this DocumentListing.


        :return: The entities of this DocumentListing.
        :rtype: list[KnowledgeDocument]
        """
        return self._entities

    @entities.setter
    def entities(self, entities):
        """
        Sets the entities of this DocumentListing.


        :param entities: The entities of this DocumentListing.
        :type: list[KnowledgeDocument]
        """
        
        self._entities = entities

    @property
    def next_uri(self):
        """
        Gets the next_uri of this DocumentListing.


        :return: The next_uri of this DocumentListing.
        :rtype: str
        """
        return self._next_uri

    @next_uri.setter
    def next_uri(self, next_uri):
        """
        Sets the next_uri of this DocumentListing.


        :param next_uri: The next_uri of this DocumentListing.
        :type: str
        """
        
        self._next_uri = next_uri

    @property
    def self_uri(self):
        """
        Gets the self_uri of this DocumentListing.


        :return: The self_uri of this DocumentListing.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this DocumentListing.


        :param self_uri: The self_uri of this DocumentListing.
        :type: str
        """
        
        self._self_uri = self_uri

    @property
    def previous_uri(self):
        """
        Gets the previous_uri of this DocumentListing.


        :return: The previous_uri of this DocumentListing.
        :rtype: str
        """
        return self._previous_uri

    @previous_uri.setter
    def previous_uri(self, previous_uri):
        """
        Sets the previous_uri of this DocumentListing.


        :param previous_uri: The previous_uri of this DocumentListing.
        :type: str
        """
        
        self._previous_uri = previous_uri

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

