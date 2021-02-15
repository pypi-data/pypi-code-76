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

class PhoneChangeTopicPhoneStatus(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PhoneChangeTopicPhoneStatus - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'operational_status': 'str',
            'edge': 'PhoneChangeTopicEdgeReference',
            'provision': 'PhoneChangeTopicProvisionInfo',
            'line_statuses': 'list[PhoneChangeTopicLineStatus]',
            'event_creation_time': 'PhoneChangeTopicOffsetDateTime'
        }

        self.attribute_map = {
            'id': 'id',
            'operational_status': 'operationalStatus',
            'edge': 'edge',
            'provision': 'provision',
            'line_statuses': 'lineStatuses',
            'event_creation_time': 'eventCreationTime'
        }

        self._id = None
        self._operational_status = None
        self._edge = None
        self._provision = None
        self._line_statuses = None
        self._event_creation_time = None

    @property
    def id(self):
        """
        Gets the id of this PhoneChangeTopicPhoneStatus.


        :return: The id of this PhoneChangeTopicPhoneStatus.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PhoneChangeTopicPhoneStatus.


        :param id: The id of this PhoneChangeTopicPhoneStatus.
        :type: str
        """
        
        self._id = id

    @property
    def operational_status(self):
        """
        Gets the operational_status of this PhoneChangeTopicPhoneStatus.


        :return: The operational_status of this PhoneChangeTopicPhoneStatus.
        :rtype: str
        """
        return self._operational_status

    @operational_status.setter
    def operational_status(self, operational_status):
        """
        Sets the operational_status of this PhoneChangeTopicPhoneStatus.


        :param operational_status: The operational_status of this PhoneChangeTopicPhoneStatus.
        :type: str
        """
        allowed_values = ["OPERATIONAL", "DEGRADED", "OFFLINE"]
        if operational_status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for operational_status -> " + operational_status)
            self._operational_status = "outdated_sdk_version"
        else:
            self._operational_status = operational_status

    @property
    def edge(self):
        """
        Gets the edge of this PhoneChangeTopicPhoneStatus.


        :return: The edge of this PhoneChangeTopicPhoneStatus.
        :rtype: PhoneChangeTopicEdgeReference
        """
        return self._edge

    @edge.setter
    def edge(self, edge):
        """
        Sets the edge of this PhoneChangeTopicPhoneStatus.


        :param edge: The edge of this PhoneChangeTopicPhoneStatus.
        :type: PhoneChangeTopicEdgeReference
        """
        
        self._edge = edge

    @property
    def provision(self):
        """
        Gets the provision of this PhoneChangeTopicPhoneStatus.


        :return: The provision of this PhoneChangeTopicPhoneStatus.
        :rtype: PhoneChangeTopicProvisionInfo
        """
        return self._provision

    @provision.setter
    def provision(self, provision):
        """
        Sets the provision of this PhoneChangeTopicPhoneStatus.


        :param provision: The provision of this PhoneChangeTopicPhoneStatus.
        :type: PhoneChangeTopicProvisionInfo
        """
        
        self._provision = provision

    @property
    def line_statuses(self):
        """
        Gets the line_statuses of this PhoneChangeTopicPhoneStatus.


        :return: The line_statuses of this PhoneChangeTopicPhoneStatus.
        :rtype: list[PhoneChangeTopicLineStatus]
        """
        return self._line_statuses

    @line_statuses.setter
    def line_statuses(self, line_statuses):
        """
        Sets the line_statuses of this PhoneChangeTopicPhoneStatus.


        :param line_statuses: The line_statuses of this PhoneChangeTopicPhoneStatus.
        :type: list[PhoneChangeTopicLineStatus]
        """
        
        self._line_statuses = line_statuses

    @property
    def event_creation_time(self):
        """
        Gets the event_creation_time of this PhoneChangeTopicPhoneStatus.


        :return: The event_creation_time of this PhoneChangeTopicPhoneStatus.
        :rtype: PhoneChangeTopicOffsetDateTime
        """
        return self._event_creation_time

    @event_creation_time.setter
    def event_creation_time(self, event_creation_time):
        """
        Sets the event_creation_time of this PhoneChangeTopicPhoneStatus.


        :param event_creation_time: The event_creation_time of this PhoneChangeTopicPhoneStatus.
        :type: PhoneChangeTopicOffsetDateTime
        """
        
        self._event_creation_time = event_creation_time

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

