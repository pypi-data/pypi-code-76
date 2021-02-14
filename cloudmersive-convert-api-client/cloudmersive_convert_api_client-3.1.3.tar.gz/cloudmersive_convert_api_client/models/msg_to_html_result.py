# coding: utf-8

"""
    convertapi

    Convert API lets you effortlessly convert file formats and types.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MsgToHtmlResult(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'successful': 'bool',
        'content': 'str',
        'body': 'str',
        '_from': 'str',
        'to': 'str',
        'cc': 'str',
        'received_time': 'str',
        'subject': 'str',
        'attachments': 'list[MsgAttachment]'
    }

    attribute_map = {
        'successful': 'Successful',
        'content': 'Content',
        'body': 'Body',
        '_from': 'From',
        'to': 'To',
        'cc': 'Cc',
        'received_time': 'ReceivedTime',
        'subject': 'Subject',
        'attachments': 'Attachments'
    }

    def __init__(self, successful=None, content=None, body=None, _from=None, to=None, cc=None, received_time=None, subject=None, attachments=None):  # noqa: E501
        """MsgToHtmlResult - a model defined in Swagger"""  # noqa: E501

        self._successful = None
        self._content = None
        self._body = None
        self.__from = None
        self._to = None
        self._cc = None
        self._received_time = None
        self._subject = None
        self._attachments = None
        self.discriminator = None

        if successful is not None:
            self.successful = successful
        if content is not None:
            self.content = content
        if body is not None:
            self.body = body
        if _from is not None:
            self._from = _from
        if to is not None:
            self.to = to
        if cc is not None:
            self.cc = cc
        if received_time is not None:
            self.received_time = received_time
        if subject is not None:
            self.subject = subject
        if attachments is not None:
            self.attachments = attachments

    @property
    def successful(self):
        """Gets the successful of this MsgToHtmlResult.  # noqa: E501

        True if the operation was successful, false otherwise  # noqa: E501

        :return: The successful of this MsgToHtmlResult.  # noqa: E501
        :rtype: bool
        """
        return self._successful

    @successful.setter
    def successful(self, successful):
        """Sets the successful of this MsgToHtmlResult.

        True if the operation was successful, false otherwise  # noqa: E501

        :param successful: The successful of this MsgToHtmlResult.  # noqa: E501
        :type: bool
        """

        self._successful = successful

    @property
    def content(self):
        """Gets the content of this MsgToHtmlResult.  # noqa: E501

        An HTML string version of the MSG file  # noqa: E501

        :return: The content of this MsgToHtmlResult.  # noqa: E501
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this MsgToHtmlResult.

        An HTML string version of the MSG file  # noqa: E501

        :param content: The content of this MsgToHtmlResult.  # noqa: E501
        :type: str
        """

        self._content = content

    @property
    def body(self):
        """Gets the body of this MsgToHtmlResult.  # noqa: E501

        The main body of the MSG file's email as an HTML string  # noqa: E501

        :return: The body of this MsgToHtmlResult.  # noqa: E501
        :rtype: str
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this MsgToHtmlResult.

        The main body of the MSG file's email as an HTML string  # noqa: E501

        :param body: The body of this MsgToHtmlResult.  # noqa: E501
        :type: str
        """

        self._body = body

    @property
    def _from(self):
        """Gets the _from of this MsgToHtmlResult.  # noqa: E501

        The From sender of the MSG file's email  # noqa: E501

        :return: The _from of this MsgToHtmlResult.  # noqa: E501
        :rtype: str
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """Sets the _from of this MsgToHtmlResult.

        The From sender of the MSG file's email  # noqa: E501

        :param _from: The _from of this MsgToHtmlResult.  # noqa: E501
        :type: str
        """

        self.__from = _from

    @property
    def to(self):
        """Gets the to of this MsgToHtmlResult.  # noqa: E501

        The To recipients of the MSG file's email  # noqa: E501

        :return: The to of this MsgToHtmlResult.  # noqa: E501
        :rtype: str
        """
        return self._to

    @to.setter
    def to(self, to):
        """Sets the to of this MsgToHtmlResult.

        The To recipients of the MSG file's email  # noqa: E501

        :param to: The to of this MsgToHtmlResult.  # noqa: E501
        :type: str
        """

        self._to = to

    @property
    def cc(self):
        """Gets the cc of this MsgToHtmlResult.  # noqa: E501

        The CC recipients of the MSG file's email  # noqa: E501

        :return: The cc of this MsgToHtmlResult.  # noqa: E501
        :rtype: str
        """
        return self._cc

    @cc.setter
    def cc(self, cc):
        """Sets the cc of this MsgToHtmlResult.

        The CC recipients of the MSG file's email  # noqa: E501

        :param cc: The cc of this MsgToHtmlResult.  # noqa: E501
        :type: str
        """

        self._cc = cc

    @property
    def received_time(self):
        """Gets the received_time of this MsgToHtmlResult.  # noqa: E501

        The time that the MSG file's email was received  # noqa: E501

        :return: The received_time of this MsgToHtmlResult.  # noqa: E501
        :rtype: str
        """
        return self._received_time

    @received_time.setter
    def received_time(self, received_time):
        """Sets the received_time of this MsgToHtmlResult.

        The time that the MSG file's email was received  # noqa: E501

        :param received_time: The received_time of this MsgToHtmlResult.  # noqa: E501
        :type: str
        """

        self._received_time = received_time

    @property
    def subject(self):
        """Gets the subject of this MsgToHtmlResult.  # noqa: E501

        The subject of the MSG file's email  # noqa: E501

        :return: The subject of this MsgToHtmlResult.  # noqa: E501
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this MsgToHtmlResult.

        The subject of the MSG file's email  # noqa: E501

        :param subject: The subject of this MsgToHtmlResult.  # noqa: E501
        :type: str
        """

        self._subject = subject

    @property
    def attachments(self):
        """Gets the attachments of this MsgToHtmlResult.  # noqa: E501

        List of all attachments for the MSG file  # noqa: E501

        :return: The attachments of this MsgToHtmlResult.  # noqa: E501
        :rtype: list[MsgAttachment]
        """
        return self._attachments

    @attachments.setter
    def attachments(self, attachments):
        """Sets the attachments of this MsgToHtmlResult.

        List of all attachments for the MSG file  # noqa: E501

        :param attachments: The attachments of this MsgToHtmlResult.  # noqa: E501
        :type: list[MsgAttachment]
        """

        self._attachments = attachments

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(MsgToHtmlResult, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MsgToHtmlResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
