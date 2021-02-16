# coding: utf-8
# -----------------------------------------------------------------------------------
# <copyright company="Aspose" file="FileFormatsResponse.py">
#   Copyright (c) 2021 GroupDocs.Assembly for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------
import pprint
import re  # noqa: F401

import six


class FileFormatsResponse(object):
    """Response with file formats.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'file_formats': 'FormatCollection',
        'code': 'int',
        'status': 'str'
    }

    attribute_map = {
        'file_formats': 'FileFormats',
        'code': 'Code',
        'status': 'Status'
    }

    def __init__(self, file_formats=None, code=None, status=None):  # noqa: E501
        """FileFormatsResponse - a model defined in Swagger"""  # noqa: E501

        self._file_formats = None
        self._code = None
        self._status = None
        self.discriminator = None

        if file_formats is not None:
            self.file_formats = file_formats
        if code is not None:
            self.code = code
        if status is not None:
            self.status = status

    @property
    def file_formats(self):
        """Gets the file_formats of this FileFormatsResponse.  # noqa: E501

        Gets or sets file formats.  # noqa: E501

        :return: The file_formats of this FileFormatsResponse.  # noqa: E501
        :rtype: FormatCollection
        """
        return self._file_formats

    @file_formats.setter
    def file_formats(self, file_formats):
        """Sets the file_formats of this FileFormatsResponse.

        Gets or sets file formats.  # noqa: E501

        :param file_formats: The file_formats of this FileFormatsResponse.  # noqa: E501
        :type: FormatCollection
        """
        self._file_formats = file_formats
    @property
    def code(self):
        """Gets the code of this FileFormatsResponse.  # noqa: E501

        Gets response status code.  # noqa: E501

        :return: The code of this FileFormatsResponse.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this FileFormatsResponse.

        Gets response status code.  # noqa: E501

        :param code: The code of this FileFormatsResponse.  # noqa: E501
        :type: int
        """
        self._code = code
    @property
    def status(self):
        """Gets the status of this FileFormatsResponse.  # noqa: E501

        Gets or sets response status.  # noqa: E501

        :return: The status of this FileFormatsResponse.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this FileFormatsResponse.

        Gets or sets response status.  # noqa: E501

        :param status: The status of this FileFormatsResponse.  # noqa: E501
        :type: str
        """
        self._status = status
    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            alias = attr
            if self.attribute_map[alias]:
                alias = self.attribute_map[alias]
            value = getattr(self, attr)
            if isinstance(value, list):
                result[alias] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[alias] = value.to_dict()
            elif isinstance(value, dict):
                result[alias] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[alias] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FileFormatsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
