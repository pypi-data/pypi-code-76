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

class SocialExpression(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SocialExpression - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'id': 'str',
            'social_media_id': 'str',
            'social_media_hub': 'str',
            'social_user_name': 'str',
            'preview_text': 'str',
            'recording_id': 'str',
            'segments': 'list[Segment]',
            'held': 'bool',
            'disconnect_type': 'str',
            'start_hold_time': 'datetime',
            'start_alerting_time': 'datetime',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'provider': 'str',
            'script_id': 'str',
            'peer_id': 'str',
            'wrapup': 'Wrapup',
            'after_call_work': 'AfterCallWork',
            'after_call_work_required': 'bool'
        }

        self.attribute_map = {
            'state': 'state',
            'id': 'id',
            'social_media_id': 'socialMediaId',
            'social_media_hub': 'socialMediaHub',
            'social_user_name': 'socialUserName',
            'preview_text': 'previewText',
            'recording_id': 'recordingId',
            'segments': 'segments',
            'held': 'held',
            'disconnect_type': 'disconnectType',
            'start_hold_time': 'startHoldTime',
            'start_alerting_time': 'startAlertingTime',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'provider': 'provider',
            'script_id': 'scriptId',
            'peer_id': 'peerId',
            'wrapup': 'wrapup',
            'after_call_work': 'afterCallWork',
            'after_call_work_required': 'afterCallWorkRequired'
        }

        self._state = None
        self._id = None
        self._social_media_id = None
        self._social_media_hub = None
        self._social_user_name = None
        self._preview_text = None
        self._recording_id = None
        self._segments = None
        self._held = None
        self._disconnect_type = None
        self._start_hold_time = None
        self._start_alerting_time = None
        self._connected_time = None
        self._disconnected_time = None
        self._provider = None
        self._script_id = None
        self._peer_id = None
        self._wrapup = None
        self._after_call_work = None
        self._after_call_work_required = None

    @property
    def state(self):
        """
        Gets the state of this SocialExpression.
        The connection state of this communication.

        :return: The state of this SocialExpression.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this SocialExpression.
        The connection state of this communication.

        :param state: The state of this SocialExpression.
        :type: str
        """
        allowed_values = ["alerting", "dialing", "contacting", "offering", "connected", "disconnected", "terminated", "none"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def id(self):
        """
        Gets the id of this SocialExpression.
        A globally unique identifier for this communication.

        :return: The id of this SocialExpression.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SocialExpression.
        A globally unique identifier for this communication.

        :param id: The id of this SocialExpression.
        :type: str
        """
        
        self._id = id

    @property
    def social_media_id(self):
        """
        Gets the social_media_id of this SocialExpression.
        A globally unique identifier for the social media.

        :return: The social_media_id of this SocialExpression.
        :rtype: str
        """
        return self._social_media_id

    @social_media_id.setter
    def social_media_id(self, social_media_id):
        """
        Sets the social_media_id of this SocialExpression.
        A globally unique identifier for the social media.

        :param social_media_id: The social_media_id of this SocialExpression.
        :type: str
        """
        
        self._social_media_id = social_media_id

    @property
    def social_media_hub(self):
        """
        Gets the social_media_hub of this SocialExpression.
        The social network of the communication

        :return: The social_media_hub of this SocialExpression.
        :rtype: str
        """
        return self._social_media_hub

    @social_media_hub.setter
    def social_media_hub(self, social_media_hub):
        """
        Sets the social_media_hub of this SocialExpression.
        The social network of the communication

        :param social_media_hub: The social_media_hub of this SocialExpression.
        :type: str
        """
        
        self._social_media_hub = social_media_hub

    @property
    def social_user_name(self):
        """
        Gets the social_user_name of this SocialExpression.
        The user name for the communication.

        :return: The social_user_name of this SocialExpression.
        :rtype: str
        """
        return self._social_user_name

    @social_user_name.setter
    def social_user_name(self, social_user_name):
        """
        Sets the social_user_name of this SocialExpression.
        The user name for the communication.

        :param social_user_name: The social_user_name of this SocialExpression.
        :type: str
        """
        
        self._social_user_name = social_user_name

    @property
    def preview_text(self):
        """
        Gets the preview_text of this SocialExpression.
        The text preview of the communication contents

        :return: The preview_text of this SocialExpression.
        :rtype: str
        """
        return self._preview_text

    @preview_text.setter
    def preview_text(self, preview_text):
        """
        Sets the preview_text of this SocialExpression.
        The text preview of the communication contents

        :param preview_text: The preview_text of this SocialExpression.
        :type: str
        """
        
        self._preview_text = preview_text

    @property
    def recording_id(self):
        """
        Gets the recording_id of this SocialExpression.
        A globally unique identifier for the recording associated with this chat.

        :return: The recording_id of this SocialExpression.
        :rtype: str
        """
        return self._recording_id

    @recording_id.setter
    def recording_id(self, recording_id):
        """
        Sets the recording_id of this SocialExpression.
        A globally unique identifier for the recording associated with this chat.

        :param recording_id: The recording_id of this SocialExpression.
        :type: str
        """
        
        self._recording_id = recording_id

    @property
    def segments(self):
        """
        Gets the segments of this SocialExpression.
        The time line of the participant's chat, divided into activity segments.

        :return: The segments of this SocialExpression.
        :rtype: list[Segment]
        """
        return self._segments

    @segments.setter
    def segments(self, segments):
        """
        Sets the segments of this SocialExpression.
        The time line of the participant's chat, divided into activity segments.

        :param segments: The segments of this SocialExpression.
        :type: list[Segment]
        """
        
        self._segments = segments

    @property
    def held(self):
        """
        Gets the held of this SocialExpression.
        True if this call is held and the person on this side hears silence.

        :return: The held of this SocialExpression.
        :rtype: bool
        """
        return self._held

    @held.setter
    def held(self, held):
        """
        Sets the held of this SocialExpression.
        True if this call is held and the person on this side hears silence.

        :param held: The held of this SocialExpression.
        :type: bool
        """
        
        self._held = held

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this SocialExpression.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :return: The disconnect_type of this SocialExpression.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this SocialExpression.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :param disconnect_type: The disconnect_type of this SocialExpression.
        :type: str
        """
        allowed_values = ["endpoint", "client", "system", "timeout", "transfer", "transfer.conference", "transfer.consult", "transfer.forward", "transfer.noanswer", "transfer.notavailable", "transport.failure", "error", "peer", "other", "spam", "uncallable"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for disconnect_type -> " + disconnect_type)
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def start_hold_time(self):
        """
        Gets the start_hold_time of this SocialExpression.
        The timestamp the chat was placed on hold in the cloud clock if the chat is currently on hold. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The start_hold_time of this SocialExpression.
        :rtype: datetime
        """
        return self._start_hold_time

    @start_hold_time.setter
    def start_hold_time(self, start_hold_time):
        """
        Sets the start_hold_time of this SocialExpression.
        The timestamp the chat was placed on hold in the cloud clock if the chat is currently on hold. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param start_hold_time: The start_hold_time of this SocialExpression.
        :type: datetime
        """
        
        self._start_hold_time = start_hold_time

    @property
    def start_alerting_time(self):
        """
        Gets the start_alerting_time of this SocialExpression.
        The timestamp the communication has when it is first put into an alerting state. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The start_alerting_time of this SocialExpression.
        :rtype: datetime
        """
        return self._start_alerting_time

    @start_alerting_time.setter
    def start_alerting_time(self, start_alerting_time):
        """
        Sets the start_alerting_time of this SocialExpression.
        The timestamp the communication has when it is first put into an alerting state. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param start_alerting_time: The start_alerting_time of this SocialExpression.
        :type: datetime
        """
        
        self._start_alerting_time = start_alerting_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this SocialExpression.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The connected_time of this SocialExpression.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this SocialExpression.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param connected_time: The connected_time of this SocialExpression.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this SocialExpression.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The disconnected_time of this SocialExpression.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this SocialExpression.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param disconnected_time: The disconnected_time of this SocialExpression.
        :type: datetime
        """
        
        self._disconnected_time = disconnected_time

    @property
    def provider(self):
        """
        Gets the provider of this SocialExpression.
        The source provider for the social expression.

        :return: The provider of this SocialExpression.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this SocialExpression.
        The source provider for the social expression.

        :param provider: The provider of this SocialExpression.
        :type: str
        """
        
        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this SocialExpression.
        The UUID of the script to use.

        :return: The script_id of this SocialExpression.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this SocialExpression.
        The UUID of the script to use.

        :param script_id: The script_id of this SocialExpression.
        :type: str
        """
        
        self._script_id = script_id

    @property
    def peer_id(self):
        """
        Gets the peer_id of this SocialExpression.
        The id of the peer communication corresponding to a matching leg for this communication.

        :return: The peer_id of this SocialExpression.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this SocialExpression.
        The id of the peer communication corresponding to a matching leg for this communication.

        :param peer_id: The peer_id of this SocialExpression.
        :type: str
        """
        
        self._peer_id = peer_id

    @property
    def wrapup(self):
        """
        Gets the wrapup of this SocialExpression.
        Call wrap up or disposition data.

        :return: The wrapup of this SocialExpression.
        :rtype: Wrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this SocialExpression.
        Call wrap up or disposition data.

        :param wrapup: The wrapup of this SocialExpression.
        :type: Wrapup
        """
        
        self._wrapup = wrapup

    @property
    def after_call_work(self):
        """
        Gets the after_call_work of this SocialExpression.
        After-call work for the communication.

        :return: The after_call_work of this SocialExpression.
        :rtype: AfterCallWork
        """
        return self._after_call_work

    @after_call_work.setter
    def after_call_work(self, after_call_work):
        """
        Sets the after_call_work of this SocialExpression.
        After-call work for the communication.

        :param after_call_work: The after_call_work of this SocialExpression.
        :type: AfterCallWork
        """
        
        self._after_call_work = after_call_work

    @property
    def after_call_work_required(self):
        """
        Gets the after_call_work_required of this SocialExpression.
        Indicates if after-call work is required for a communication. Only used when the ACW Setting is Agent Requested.

        :return: The after_call_work_required of this SocialExpression.
        :rtype: bool
        """
        return self._after_call_work_required

    @after_call_work_required.setter
    def after_call_work_required(self, after_call_work_required):
        """
        Sets the after_call_work_required of this SocialExpression.
        Indicates if after-call work is required for a communication. Only used when the ACW Setting is Agent Requested.

        :param after_call_work_required: The after_call_work_required of this SocialExpression.
        :type: bool
        """
        
        self._after_call_work_required = after_call_work_required

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

