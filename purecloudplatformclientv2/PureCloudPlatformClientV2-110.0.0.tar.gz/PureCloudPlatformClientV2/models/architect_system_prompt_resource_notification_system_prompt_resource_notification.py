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

class ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'prompt_id': 'str',
            'id': 'str',
            'language': 'str',
            'media_uri': 'str',
            'upload_status': 'str',
            'duration_seconds': 'float'
        }

        self.attribute_map = {
            'prompt_id': 'promptId',
            'id': 'id',
            'language': 'language',
            'media_uri': 'mediaUri',
            'upload_status': 'uploadStatus',
            'duration_seconds': 'durationSeconds'
        }

        self._prompt_id = None
        self._id = None
        self._language = None
        self._media_uri = None
        self._upload_status = None
        self._duration_seconds = None

    @property
    def prompt_id(self):
        """
        Gets the prompt_id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :return: The prompt_id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :rtype: str
        """
        return self._prompt_id

    @prompt_id.setter
    def prompt_id(self, prompt_id):
        """
        Sets the prompt_id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :param prompt_id: The prompt_id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :type: str
        """
        
        self._prompt_id = prompt_id

    @property
    def id(self):
        """
        Gets the id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :return: The id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :param id: The id of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :type: str
        """
        
        self._id = id

    @property
    def language(self):
        """
        Gets the language of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :return: The language of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """
        Sets the language of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :param language: The language of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :type: str
        """
        
        self._language = language

    @property
    def media_uri(self):
        """
        Gets the media_uri of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :return: The media_uri of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :rtype: str
        """
        return self._media_uri

    @media_uri.setter
    def media_uri(self, media_uri):
        """
        Sets the media_uri of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :param media_uri: The media_uri of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :type: str
        """
        
        self._media_uri = media_uri

    @property
    def upload_status(self):
        """
        Gets the upload_status of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :return: The upload_status of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :rtype: str
        """
        return self._upload_status

    @upload_status.setter
    def upload_status(self, upload_status):
        """
        Sets the upload_status of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :param upload_status: The upload_status of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :type: str
        """
        
        self._upload_status = upload_status

    @property
    def duration_seconds(self):
        """
        Gets the duration_seconds of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :return: The duration_seconds of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :rtype: float
        """
        return self._duration_seconds

    @duration_seconds.setter
    def duration_seconds(self, duration_seconds):
        """
        Sets the duration_seconds of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.


        :param duration_seconds: The duration_seconds of this ArchitectSystemPromptResourceNotificationSystemPromptResourceNotification.
        :type: float
        """
        
        self._duration_seconds = duration_seconds

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

