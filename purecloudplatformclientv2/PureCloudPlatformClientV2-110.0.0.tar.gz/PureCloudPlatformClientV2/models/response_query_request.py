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

class ResponseQueryRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ResponseQueryRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'query_phrase': 'str',
            'page_size': 'int',
            'filters': 'list[ResponseFilter]'
        }

        self.attribute_map = {
            'query_phrase': 'queryPhrase',
            'page_size': 'pageSize',
            'filters': 'filters'
        }

        self._query_phrase = None
        self._page_size = None
        self._filters = None

    @property
    def query_phrase(self):
        """
        Gets the query_phrase of this ResponseQueryRequest.
        Query phrase to search response text and name. If not set will match all.

        :return: The query_phrase of this ResponseQueryRequest.
        :rtype: str
        """
        return self._query_phrase

    @query_phrase.setter
    def query_phrase(self, query_phrase):
        """
        Sets the query_phrase of this ResponseQueryRequest.
        Query phrase to search response text and name. If not set will match all.

        :param query_phrase: The query_phrase of this ResponseQueryRequest.
        :type: str
        """
        
        self._query_phrase = query_phrase

    @property
    def page_size(self):
        """
        Gets the page_size of this ResponseQueryRequest.
        The maximum number of hits to return. Default: 25, Maximum: 500.

        :return: The page_size of this ResponseQueryRequest.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """
        Sets the page_size of this ResponseQueryRequest.
        The maximum number of hits to return. Default: 25, Maximum: 500.

        :param page_size: The page_size of this ResponseQueryRequest.
        :type: int
        """
        
        self._page_size = page_size

    @property
    def filters(self):
        """
        Gets the filters of this ResponseQueryRequest.
        Filter the query results.

        :return: The filters of this ResponseQueryRequest.
        :rtype: list[ResponseFilter]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """
        Sets the filters of this ResponseQueryRequest.
        Filter the query results.

        :param filters: The filters of this ResponseQueryRequest.
        :type: list[ResponseFilter]
        """
        
        self._filters = filters

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

