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


class ReplaceDocxParagraphRequest(object):
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
        'find_string': 'str',
        'match_case': 'bool',
        'replacement_image': 'DocxImage'
    }

    attribute_map = {
        'input_file_bytes': 'InputFileBytes',
        'input_file_url': 'InputFileUrl',
        'find_string': 'FindString',
        'match_case': 'MatchCase',
        'replacement_image': 'Replacement_Image'
    }

    def __init__(self, input_file_bytes=None, input_file_url=None, find_string=None, match_case=None, replacement_image=None):  # noqa: E501
        """ReplaceDocxParagraphRequest - a model defined in Swagger"""  # noqa: E501

        self._input_file_bytes = None
        self._input_file_url = None
        self._find_string = None
        self._match_case = None
        self._replacement_image = None
        self.discriminator = None

        if input_file_bytes is not None:
            self.input_file_bytes = input_file_bytes
        if input_file_url is not None:
            self.input_file_url = input_file_url
        if find_string is not None:
            self.find_string = find_string
        if match_case is not None:
            self.match_case = match_case
        if replacement_image is not None:
            self.replacement_image = replacement_image

    @property
    def input_file_bytes(self):
        """Gets the input_file_bytes of this ReplaceDocxParagraphRequest.  # noqa: E501

        Optional: Bytes of the input file to operate on  # noqa: E501

        :return: The input_file_bytes of this ReplaceDocxParagraphRequest.  # noqa: E501
        :rtype: str
        """
        return self._input_file_bytes

    @input_file_bytes.setter
    def input_file_bytes(self, input_file_bytes):
        """Sets the input_file_bytes of this ReplaceDocxParagraphRequest.

        Optional: Bytes of the input file to operate on  # noqa: E501

        :param input_file_bytes: The input_file_bytes of this ReplaceDocxParagraphRequest.  # noqa: E501
        :type: str
        """
        if input_file_bytes is not None and not re.search(r'^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', input_file_bytes):  # noqa: E501
            raise ValueError(r"Invalid value for `input_file_bytes`, must be a follow pattern or equal to `/^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$/`")  # noqa: E501

        self._input_file_bytes = input_file_bytes

    @property
    def input_file_url(self):
        """Gets the input_file_url of this ReplaceDocxParagraphRequest.  # noqa: E501

        Optional: URL of a file to operate on as input.  This can be a public URL, or you can also use the begin-editing API to upload a document and pass in the secure URL result from that operation as the URL here (this URL is not public).  # noqa: E501

        :return: The input_file_url of this ReplaceDocxParagraphRequest.  # noqa: E501
        :rtype: str
        """
        return self._input_file_url

    @input_file_url.setter
    def input_file_url(self, input_file_url):
        """Sets the input_file_url of this ReplaceDocxParagraphRequest.

        Optional: URL of a file to operate on as input.  This can be a public URL, or you can also use the begin-editing API to upload a document and pass in the secure URL result from that operation as the URL here (this URL is not public).  # noqa: E501

        :param input_file_url: The input_file_url of this ReplaceDocxParagraphRequest.  # noqa: E501
        :type: str
        """

        self._input_file_url = input_file_url

    @property
    def find_string(self):
        """Gets the find_string of this ReplaceDocxParagraphRequest.  # noqa: E501

        Required: The target string to search for in the paragraphs of the document  # noqa: E501

        :return: The find_string of this ReplaceDocxParagraphRequest.  # noqa: E501
        :rtype: str
        """
        return self._find_string

    @find_string.setter
    def find_string(self, find_string):
        """Sets the find_string of this ReplaceDocxParagraphRequest.

        Required: The target string to search for in the paragraphs of the document  # noqa: E501

        :param find_string: The find_string of this ReplaceDocxParagraphRequest.  # noqa: E501
        :type: str
        """

        self._find_string = find_string

    @property
    def match_case(self):
        """Gets the match_case of this ReplaceDocxParagraphRequest.  # noqa: E501

        Optional: True to match case, false to ignore case when matching  # noqa: E501

        :return: The match_case of this ReplaceDocxParagraphRequest.  # noqa: E501
        :rtype: bool
        """
        return self._match_case

    @match_case.setter
    def match_case(self, match_case):
        """Sets the match_case of this ReplaceDocxParagraphRequest.

        Optional: True to match case, false to ignore case when matching  # noqa: E501

        :param match_case: The match_case of this ReplaceDocxParagraphRequest.  # noqa: E501
        :type: bool
        """

        self._match_case = match_case

    @property
    def replacement_image(self):
        """Gets the replacement_image of this ReplaceDocxParagraphRequest.  # noqa: E501

        Optional: Image to replace the paragraph with; note that most of the fields in this object are optional and do not need to be supplied  # noqa: E501

        :return: The replacement_image of this ReplaceDocxParagraphRequest.  # noqa: E501
        :rtype: DocxImage
        """
        return self._replacement_image

    @replacement_image.setter
    def replacement_image(self, replacement_image):
        """Sets the replacement_image of this ReplaceDocxParagraphRequest.

        Optional: Image to replace the paragraph with; note that most of the fields in this object are optional and do not need to be supplied  # noqa: E501

        :param replacement_image: The replacement_image of this ReplaceDocxParagraphRequest.  # noqa: E501
        :type: DocxImage
        """

        self._replacement_image = replacement_image

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
        if issubclass(ReplaceDocxParagraphRequest, dict):
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
        if not isinstance(other, ReplaceDocxParagraphRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
