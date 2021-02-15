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

class SmsAddressProvision(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SmsAddressProvision - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'street': 'str',
            'city': 'str',
            'region': 'str',
            'postal_code': 'str',
            'country_code': 'str',
            'auto_correct_address': 'bool',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'street': 'street',
            'city': 'city',
            'region': 'region',
            'postal_code': 'postalCode',
            'country_code': 'countryCode',
            'auto_correct_address': 'autoCorrectAddress',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._street = None
        self._city = None
        self._region = None
        self._postal_code = None
        self._country_code = None
        self._auto_correct_address = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this SmsAddressProvision.
        The globally unique identifier for the object.

        :return: The id of this SmsAddressProvision.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SmsAddressProvision.
        The globally unique identifier for the object.

        :param id: The id of this SmsAddressProvision.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this SmsAddressProvision.
        Name associated with this address

        :return: The name of this SmsAddressProvision.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this SmsAddressProvision.
        Name associated with this address

        :param name: The name of this SmsAddressProvision.
        :type: str
        """
        
        self._name = name

    @property
    def street(self):
        """
        Gets the street of this SmsAddressProvision.
        The number and street address where this address is located.

        :return: The street of this SmsAddressProvision.
        :rtype: str
        """
        return self._street

    @street.setter
    def street(self, street):
        """
        Sets the street of this SmsAddressProvision.
        The number and street address where this address is located.

        :param street: The street of this SmsAddressProvision.
        :type: str
        """
        
        self._street = street

    @property
    def city(self):
        """
        Gets the city of this SmsAddressProvision.
        The city in which this address is in

        :return: The city of this SmsAddressProvision.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """
        Sets the city of this SmsAddressProvision.
        The city in which this address is in

        :param city: The city of this SmsAddressProvision.
        :type: str
        """
        
        self._city = city

    @property
    def region(self):
        """
        Gets the region of this SmsAddressProvision.
        The state or region this address is in

        :return: The region of this SmsAddressProvision.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """
        Sets the region of this SmsAddressProvision.
        The state or region this address is in

        :param region: The region of this SmsAddressProvision.
        :type: str
        """
        
        self._region = region

    @property
    def postal_code(self):
        """
        Gets the postal_code of this SmsAddressProvision.
        The postal code this address is in

        :return: The postal_code of this SmsAddressProvision.
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """
        Sets the postal_code of this SmsAddressProvision.
        The postal code this address is in

        :param postal_code: The postal_code of this SmsAddressProvision.
        :type: str
        """
        
        self._postal_code = postal_code

    @property
    def country_code(self):
        """
        Gets the country_code of this SmsAddressProvision.
        The ISO country code of this address

        :return: The country_code of this SmsAddressProvision.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """
        Sets the country_code of this SmsAddressProvision.
        The ISO country code of this address

        :param country_code: The country_code of this SmsAddressProvision.
        :type: str
        """
        
        self._country_code = country_code

    @property
    def auto_correct_address(self):
        """
        Gets the auto_correct_address of this SmsAddressProvision.
        This is used when the address is created. If the value is not set or true, then the system will, if necessary, auto-correct the address you provide. Set this value to false if the system should not auto-correct the address.

        :return: The auto_correct_address of this SmsAddressProvision.
        :rtype: bool
        """
        return self._auto_correct_address

    @auto_correct_address.setter
    def auto_correct_address(self, auto_correct_address):
        """
        Sets the auto_correct_address of this SmsAddressProvision.
        This is used when the address is created. If the value is not set or true, then the system will, if necessary, auto-correct the address you provide. Set this value to false if the system should not auto-correct the address.

        :param auto_correct_address: The auto_correct_address of this SmsAddressProvision.
        :type: bool
        """
        
        self._auto_correct_address = auto_correct_address

    @property
    def self_uri(self):
        """
        Gets the self_uri of this SmsAddressProvision.
        The URI for this object

        :return: The self_uri of this SmsAddressProvision.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this SmsAddressProvision.
        The URI for this object

        :param self_uri: The self_uri of this SmsAddressProvision.
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

