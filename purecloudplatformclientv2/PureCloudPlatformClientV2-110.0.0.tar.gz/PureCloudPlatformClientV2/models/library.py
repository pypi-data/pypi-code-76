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

class Library(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Library - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'version': 'int',
            'created_by': 'User',
            'date_created': 'datetime',
            'response_type': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version': 'version',
            'created_by': 'createdBy',
            'date_created': 'dateCreated',
            'response_type': 'responseType',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._version = None
        self._created_by = None
        self._date_created = None
        self._response_type = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Library.
        The globally unique identifier for the object.

        :return: The id of this Library.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Library.
        The globally unique identifier for the object.

        :param id: The id of this Library.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Library.
        The library name.

        :return: The name of this Library.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Library.
        The library name.

        :param name: The name of this Library.
        :type: str
        """
        
        self._name = name

    @property
    def version(self):
        """
        Gets the version of this Library.
        Current version for this resource.

        :return: The version of this Library.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this Library.
        Current version for this resource.

        :param version: The version of this Library.
        :type: int
        """
        
        self._version = version

    @property
    def created_by(self):
        """
        Gets the created_by of this Library.
        User that created the library.

        :return: The created_by of this Library.
        :rtype: User
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this Library.
        User that created the library.

        :param created_by: The created_by of this Library.
        :type: User
        """
        
        self._created_by = created_by

    @property
    def date_created(self):
        """
        Gets the date_created of this Library.
        The date and time the response was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this Library.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this Library.
        The date and time the response was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this Library.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def response_type(self):
        """
        Gets the response_type of this Library.
        This value is deprecated. Responses representing message templates may be added to any library.

        :return: The response_type of this Library.
        :rtype: str
        """
        return self._response_type

    @response_type.setter
    def response_type(self, response_type):
        """
        Sets the response_type of this Library.
        This value is deprecated. Responses representing message templates may be added to any library.

        :param response_type: The response_type of this Library.
        :type: str
        """
        allowed_values = ["MessagingTemplate", "CampaignSmsTemplate"]
        if response_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for response_type -> " + response_type)
            self._response_type = "outdated_sdk_version"
        else:
            self._response_type = response_type

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Library.
        The URI for this object

        :return: The self_uri of this Library.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Library.
        The URI for this object

        :param self_uri: The self_uri of this Library.
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

