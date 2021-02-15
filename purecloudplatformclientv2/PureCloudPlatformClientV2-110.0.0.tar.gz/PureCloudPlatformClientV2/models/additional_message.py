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

class AdditionalMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AdditionalMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'text_body': 'str',
            'media_ids': 'list[str]',
            'sticker_ids': 'list[str]',
            'messaging_template': 'MessagingTemplateRequest'
        }

        self.attribute_map = {
            'text_body': 'textBody',
            'media_ids': 'mediaIds',
            'sticker_ids': 'stickerIds',
            'messaging_template': 'messagingTemplate'
        }

        self._text_body = None
        self._media_ids = None
        self._sticker_ids = None
        self._messaging_template = None

    @property
    def text_body(self):
        """
        Gets the text_body of this AdditionalMessage.
        The body of the text message.

        :return: The text_body of this AdditionalMessage.
        :rtype: str
        """
        return self._text_body

    @text_body.setter
    def text_body(self, text_body):
        """
        Sets the text_body of this AdditionalMessage.
        The body of the text message.

        :param text_body: The text_body of this AdditionalMessage.
        :type: str
        """
        
        self._text_body = text_body

    @property
    def media_ids(self):
        """
        Gets the media_ids of this AdditionalMessage.
        The media ids associated with the text message.

        :return: The media_ids of this AdditionalMessage.
        :rtype: list[str]
        """
        return self._media_ids

    @media_ids.setter
    def media_ids(self, media_ids):
        """
        Sets the media_ids of this AdditionalMessage.
        The media ids associated with the text message.

        :param media_ids: The media_ids of this AdditionalMessage.
        :type: list[str]
        """
        
        self._media_ids = media_ids

    @property
    def sticker_ids(self):
        """
        Gets the sticker_ids of this AdditionalMessage.
        The sticker ids associated with the text message.

        :return: The sticker_ids of this AdditionalMessage.
        :rtype: list[str]
        """
        return self._sticker_ids

    @sticker_ids.setter
    def sticker_ids(self, sticker_ids):
        """
        Sets the sticker_ids of this AdditionalMessage.
        The sticker ids associated with the text message.

        :param sticker_ids: The sticker_ids of this AdditionalMessage.
        :type: list[str]
        """
        
        self._sticker_ids = sticker_ids

    @property
    def messaging_template(self):
        """
        Gets the messaging_template of this AdditionalMessage.
        The messaging template use to send a predefined canned response with the message

        :return: The messaging_template of this AdditionalMessage.
        :rtype: MessagingTemplateRequest
        """
        return self._messaging_template

    @messaging_template.setter
    def messaging_template(self, messaging_template):
        """
        Sets the messaging_template of this AdditionalMessage.
        The messaging template use to send a predefined canned response with the message

        :param messaging_template: The messaging_template of this AdditionalMessage.
        :type: MessagingTemplateRequest
        """
        
        self._messaging_template = messaging_template

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

