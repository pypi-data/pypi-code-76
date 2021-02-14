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


class GetXlsxCellByIdentifierRequest(object):
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
        'input_file_bytes': 'str',
        'input_file_url': 'str',
        'worksheet_to_query': 'XlsxWorksheet',
        'cell_identifier': 'str'
    }

    attribute_map = {
        'input_file_bytes': 'InputFileBytes',
        'input_file_url': 'InputFileUrl',
        'worksheet_to_query': 'WorksheetToQuery',
        'cell_identifier': 'CellIdentifier'
    }

    def __init__(self, input_file_bytes=None, input_file_url=None, worksheet_to_query=None, cell_identifier=None):  # noqa: E501
        """GetXlsxCellByIdentifierRequest - a model defined in Swagger"""  # noqa: E501

        self._input_file_bytes = None
        self._input_file_url = None
        self._worksheet_to_query = None
        self._cell_identifier = None
        self.discriminator = None

        if input_file_bytes is not None:
            self.input_file_bytes = input_file_bytes
        if input_file_url is not None:
            self.input_file_url = input_file_url
        if worksheet_to_query is not None:
            self.worksheet_to_query = worksheet_to_query
        if cell_identifier is not None:
            self.cell_identifier = cell_identifier

    @property
    def input_file_bytes(self):
        """Gets the input_file_bytes of this GetXlsxCellByIdentifierRequest.  # noqa: E501

        Optional: Bytes of the input file to operate on  # noqa: E501

        :return: The input_file_bytes of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :rtype: str
        """
        return self._input_file_bytes

    @input_file_bytes.setter
    def input_file_bytes(self, input_file_bytes):
        """Sets the input_file_bytes of this GetXlsxCellByIdentifierRequest.

        Optional: Bytes of the input file to operate on  # noqa: E501

        :param input_file_bytes: The input_file_bytes of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :type: str
        """
        if input_file_bytes is not None and not re.search(r'^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', input_file_bytes):  # noqa: E501
            raise ValueError(r"Invalid value for `input_file_bytes`, must be a follow pattern or equal to `/^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$/`")  # noqa: E501

        self._input_file_bytes = input_file_bytes

    @property
    def input_file_url(self):
        """Gets the input_file_url of this GetXlsxCellByIdentifierRequest.  # noqa: E501

        Optional: URL of a file to operate on as input.  This can be a public URL, or you can also use the begin-editing API to upload a document and pass in the secure URL result from that operation as the URL here (this URL is not public).  # noqa: E501

        :return: The input_file_url of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :rtype: str
        """
        return self._input_file_url

    @input_file_url.setter
    def input_file_url(self, input_file_url):
        """Sets the input_file_url of this GetXlsxCellByIdentifierRequest.

        Optional: URL of a file to operate on as input.  This can be a public URL, or you can also use the begin-editing API to upload a document and pass in the secure URL result from that operation as the URL here (this URL is not public).  # noqa: E501

        :param input_file_url: The input_file_url of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :type: str
        """

        self._input_file_url = input_file_url

    @property
    def worksheet_to_query(self):
        """Gets the worksheet_to_query of this GetXlsxCellByIdentifierRequest.  # noqa: E501

        Optional; Worksheet (tab) within the spreadsheet to get the rows and cells of; leave blank to default to the first worksheet  # noqa: E501

        :return: The worksheet_to_query of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :rtype: XlsxWorksheet
        """
        return self._worksheet_to_query

    @worksheet_to_query.setter
    def worksheet_to_query(self, worksheet_to_query):
        """Sets the worksheet_to_query of this GetXlsxCellByIdentifierRequest.

        Optional; Worksheet (tab) within the spreadsheet to get the rows and cells of; leave blank to default to the first worksheet  # noqa: E501

        :param worksheet_to_query: The worksheet_to_query of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :type: XlsxWorksheet
        """

        self._worksheet_to_query = worksheet_to_query

    @property
    def cell_identifier(self):
        """Gets the cell_identifier of this GetXlsxCellByIdentifierRequest.  # noqa: E501

        Required; Excel cell identifier, e.g. A1, B22, C33, etc.  # noqa: E501

        :return: The cell_identifier of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :rtype: str
        """
        return self._cell_identifier

    @cell_identifier.setter
    def cell_identifier(self, cell_identifier):
        """Sets the cell_identifier of this GetXlsxCellByIdentifierRequest.

        Required; Excel cell identifier, e.g. A1, B22, C33, etc.  # noqa: E501

        :param cell_identifier: The cell_identifier of this GetXlsxCellByIdentifierRequest.  # noqa: E501
        :type: str
        """

        self._cell_identifier = cell_identifier

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
        if issubclass(GetXlsxCellByIdentifierRequest, dict):
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
        if not isinstance(other, GetXlsxCellByIdentifierRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
