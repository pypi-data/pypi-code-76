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

class CoachingAppointmentResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CoachingAppointmentResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'date_start': 'datetime',
            'length_in_minutes': 'int',
            'status': 'str',
            'facilitator': 'UserReference',
            'attendees': 'list[UserReference]',
            'created_by': 'UserReference',
            'date_created': 'datetime',
            'modified_by': 'UserReference',
            'date_modified': 'datetime',
            'conversations': 'list[ConversationReference]',
            'documents': 'list[DocumentReference]',
            'is_overdue': 'bool',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'date_start': 'dateStart',
            'length_in_minutes': 'lengthInMinutes',
            'status': 'status',
            'facilitator': 'facilitator',
            'attendees': 'attendees',
            'created_by': 'createdBy',
            'date_created': 'dateCreated',
            'modified_by': 'modifiedBy',
            'date_modified': 'dateModified',
            'conversations': 'conversations',
            'documents': 'documents',
            'is_overdue': 'isOverdue',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._date_start = None
        self._length_in_minutes = None
        self._status = None
        self._facilitator = None
        self._attendees = None
        self._created_by = None
        self._date_created = None
        self._modified_by = None
        self._date_modified = None
        self._conversations = None
        self._documents = None
        self._is_overdue = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this CoachingAppointmentResponse.
        The globally unique identifier for the object.

        :return: The id of this CoachingAppointmentResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CoachingAppointmentResponse.
        The globally unique identifier for the object.

        :param id: The id of this CoachingAppointmentResponse.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this CoachingAppointmentResponse.
        The name of coaching appointment

        :return: The name of this CoachingAppointmentResponse.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CoachingAppointmentResponse.
        The name of coaching appointment

        :param name: The name of this CoachingAppointmentResponse.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this CoachingAppointmentResponse.
        The description of coaching appointment

        :return: The description of this CoachingAppointmentResponse.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CoachingAppointmentResponse.
        The description of coaching appointment

        :param description: The description of this CoachingAppointmentResponse.
        :type: str
        """
        
        self._description = description

    @property
    def date_start(self):
        """
        Gets the date_start of this CoachingAppointmentResponse.
        The date/time the coaching appointment starts. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_start of this CoachingAppointmentResponse.
        :rtype: datetime
        """
        return self._date_start

    @date_start.setter
    def date_start(self, date_start):
        """
        Sets the date_start of this CoachingAppointmentResponse.
        The date/time the coaching appointment starts. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_start: The date_start of this CoachingAppointmentResponse.
        :type: datetime
        """
        
        self._date_start = date_start

    @property
    def length_in_minutes(self):
        """
        Gets the length_in_minutes of this CoachingAppointmentResponse.
        The duration of coaching appointment in minutes

        :return: The length_in_minutes of this CoachingAppointmentResponse.
        :rtype: int
        """
        return self._length_in_minutes

    @length_in_minutes.setter
    def length_in_minutes(self, length_in_minutes):
        """
        Sets the length_in_minutes of this CoachingAppointmentResponse.
        The duration of coaching appointment in minutes

        :param length_in_minutes: The length_in_minutes of this CoachingAppointmentResponse.
        :type: int
        """
        
        self._length_in_minutes = length_in_minutes

    @property
    def status(self):
        """
        Gets the status of this CoachingAppointmentResponse.
        The status of coaching appointment

        :return: The status of this CoachingAppointmentResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this CoachingAppointmentResponse.
        The status of coaching appointment

        :param status: The status of this CoachingAppointmentResponse.
        :type: str
        """
        allowed_values = ["Scheduled", "InProgress", "Completed", "InvalidSchedule"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def facilitator(self):
        """
        Gets the facilitator of this CoachingAppointmentResponse.
        The facilitator of coaching appointment

        :return: The facilitator of this CoachingAppointmentResponse.
        :rtype: UserReference
        """
        return self._facilitator

    @facilitator.setter
    def facilitator(self, facilitator):
        """
        Sets the facilitator of this CoachingAppointmentResponse.
        The facilitator of coaching appointment

        :param facilitator: The facilitator of this CoachingAppointmentResponse.
        :type: UserReference
        """
        
        self._facilitator = facilitator

    @property
    def attendees(self):
        """
        Gets the attendees of this CoachingAppointmentResponse.
        The list of attendees attending the coaching

        :return: The attendees of this CoachingAppointmentResponse.
        :rtype: list[UserReference]
        """
        return self._attendees

    @attendees.setter
    def attendees(self, attendees):
        """
        Sets the attendees of this CoachingAppointmentResponse.
        The list of attendees attending the coaching

        :param attendees: The attendees of this CoachingAppointmentResponse.
        :type: list[UserReference]
        """
        
        self._attendees = attendees

    @property
    def created_by(self):
        """
        Gets the created_by of this CoachingAppointmentResponse.
        The user who created the coaching appointment

        :return: The created_by of this CoachingAppointmentResponse.
        :rtype: UserReference
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this CoachingAppointmentResponse.
        The user who created the coaching appointment

        :param created_by: The created_by of this CoachingAppointmentResponse.
        :type: UserReference
        """
        
        self._created_by = created_by

    @property
    def date_created(self):
        """
        Gets the date_created of this CoachingAppointmentResponse.
        The date/time the coaching appointment was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this CoachingAppointmentResponse.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this CoachingAppointmentResponse.
        The date/time the coaching appointment was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this CoachingAppointmentResponse.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def modified_by(self):
        """
        Gets the modified_by of this CoachingAppointmentResponse.
        The last user to modify the coaching appointment

        :return: The modified_by of this CoachingAppointmentResponse.
        :rtype: UserReference
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this CoachingAppointmentResponse.
        The last user to modify the coaching appointment

        :param modified_by: The modified_by of this CoachingAppointmentResponse.
        :type: UserReference
        """
        
        self._modified_by = modified_by

    @property
    def date_modified(self):
        """
        Gets the date_modified of this CoachingAppointmentResponse.
        The date/time the coaching appointment was last modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_modified of this CoachingAppointmentResponse.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this CoachingAppointmentResponse.
        The date/time the coaching appointment was last modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_modified: The date_modified of this CoachingAppointmentResponse.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def conversations(self):
        """
        Gets the conversations of this CoachingAppointmentResponse.
        The list of conversations associated with coaching appointment.

        :return: The conversations of this CoachingAppointmentResponse.
        :rtype: list[ConversationReference]
        """
        return self._conversations

    @conversations.setter
    def conversations(self, conversations):
        """
        Sets the conversations of this CoachingAppointmentResponse.
        The list of conversations associated with coaching appointment.

        :param conversations: The conversations of this CoachingAppointmentResponse.
        :type: list[ConversationReference]
        """
        
        self._conversations = conversations

    @property
    def documents(self):
        """
        Gets the documents of this CoachingAppointmentResponse.
        The list of documents associated with coaching appointment.

        :return: The documents of this CoachingAppointmentResponse.
        :rtype: list[DocumentReference]
        """
        return self._documents

    @documents.setter
    def documents(self, documents):
        """
        Sets the documents of this CoachingAppointmentResponse.
        The list of documents associated with coaching appointment.

        :param documents: The documents of this CoachingAppointmentResponse.
        :type: list[DocumentReference]
        """
        
        self._documents = documents

    @property
    def is_overdue(self):
        """
        Gets the is_overdue of this CoachingAppointmentResponse.
        Whether the appointment is overdue.

        :return: The is_overdue of this CoachingAppointmentResponse.
        :rtype: bool
        """
        return self._is_overdue

    @is_overdue.setter
    def is_overdue(self, is_overdue):
        """
        Sets the is_overdue of this CoachingAppointmentResponse.
        Whether the appointment is overdue.

        :param is_overdue: The is_overdue of this CoachingAppointmentResponse.
        :type: bool
        """
        
        self._is_overdue = is_overdue

    @property
    def self_uri(self):
        """
        Gets the self_uri of this CoachingAppointmentResponse.
        The URI for this object

        :return: The self_uri of this CoachingAppointmentResponse.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this CoachingAppointmentResponse.
        The URI for this object

        :param self_uri: The self_uri of this CoachingAppointmentResponse.
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

