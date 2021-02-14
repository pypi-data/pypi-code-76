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


class XlsxSpreadsheetColumn(object):
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
        'path': 'str',
        'heading_cell': 'XlsxSpreadsheetCell'
    }

    attribute_map = {
        'path': 'Path',
        'heading_cell': 'HeadingCell'
    }

    def __init__(self, path=None, heading_cell=None):  # noqa: E501
        """XlsxSpreadsheetColumn - a model defined in Swagger"""  # noqa: E501

        self._path = None
        self._heading_cell = None
        self.discriminator = None

        if path is not None:
            self.path = path
        if heading_cell is not None:
            self.heading_cell = heading_cell

    @property
    def path(self):
        """Gets the path of this XlsxSpreadsheetColumn.  # noqa: E501

        The Path of the location of this object; leave blank for new rows  # noqa: E501

        :return: The path of this XlsxSpreadsheetColumn.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this XlsxSpreadsheetColumn.

        The Path of the location of this object; leave blank for new rows  # noqa: E501

        :param path: The path of this XlsxSpreadsheetColumn.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def heading_cell(self):
        """Gets the heading_cell of this XlsxSpreadsheetColumn.  # noqa: E501

        Heading cell for this column  # noqa: E501

        :return: The heading_cell of this XlsxSpreadsheetColumn.  # noqa: E501
        :rtype: XlsxSpreadsheetCell
        """
        return self._heading_cell

    @heading_cell.setter
    def heading_cell(self, heading_cell):
        """Sets the heading_cell of this XlsxSpreadsheetColumn.

        Heading cell for this column  # noqa: E501

        :param heading_cell: The heading_cell of this XlsxSpreadsheetColumn.  # noqa: E501
        :type: XlsxSpreadsheetCell
        """

        self._heading_cell = heading_cell

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
        if issubclass(XlsxSpreadsheetColumn, dict):
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
        if not isinstance(other, XlsxSpreadsheetColumn):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
