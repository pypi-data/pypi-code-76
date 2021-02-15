# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.2591
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class ModelReturn(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'effective_at': 'datetime',
        'return_value': 'float',
        'market_value': 'float',
        'period': 'str'
    }

    attribute_map = {
        'effective_at': 'effectiveAt',
        'return_value': 'returnValue',
        'market_value': 'marketValue',
        'period': 'period'
    }

    required_map = {
        'effective_at': 'required',
        'return_value': 'required',
        'market_value': 'required',
        'period': 'optional'
    }

    def __init__(self, effective_at=None, return_value=None, market_value=None, period=None):  # noqa: E501
        """
        ModelReturn - a model defined in OpenAPI

        :param effective_at:  The effectiveAt for the return. (required)
        :type effective_at: datetime
        :param return_value:  The return number. (required)
        :type return_value: float
        :param market_value:  The market value. (required)
        :type market_value: float
        :param period:  Show the returns on a Daily or Monthly period.
        :type period: str

        """  # noqa: E501

        self._effective_at = None
        self._return_value = None
        self._market_value = None
        self._period = None
        self.discriminator = None

        self.effective_at = effective_at
        self.return_value = return_value
        self.market_value = market_value
        self.period = period

    @property
    def effective_at(self):
        """Gets the effective_at of this ModelReturn.  # noqa: E501

        The effectiveAt for the return.  # noqa: E501

        :return: The effective_at of this ModelReturn.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_at

    @effective_at.setter
    def effective_at(self, effective_at):
        """Sets the effective_at of this ModelReturn.

        The effectiveAt for the return.  # noqa: E501

        :param effective_at: The effective_at of this ModelReturn.  # noqa: E501
        :type: datetime
        """
        if effective_at is None:
            raise ValueError("Invalid value for `effective_at`, must not be `None`")  # noqa: E501

        self._effective_at = effective_at

    @property
    def return_value(self):
        """Gets the return_value of this ModelReturn.  # noqa: E501

        The return number.  # noqa: E501

        :return: The return_value of this ModelReturn.  # noqa: E501
        :rtype: float
        """
        return self._return_value

    @return_value.setter
    def return_value(self, return_value):
        """Sets the return_value of this ModelReturn.

        The return number.  # noqa: E501

        :param return_value: The return_value of this ModelReturn.  # noqa: E501
        :type: float
        """
        if return_value is None:
            raise ValueError("Invalid value for `return_value`, must not be `None`")  # noqa: E501

        self._return_value = return_value

    @property
    def market_value(self):
        """Gets the market_value of this ModelReturn.  # noqa: E501

        The market value.  # noqa: E501

        :return: The market_value of this ModelReturn.  # noqa: E501
        :rtype: float
        """
        return self._market_value

    @market_value.setter
    def market_value(self, market_value):
        """Sets the market_value of this ModelReturn.

        The market value.  # noqa: E501

        :param market_value: The market_value of this ModelReturn.  # noqa: E501
        :type: float
        """
        if market_value is None:
            raise ValueError("Invalid value for `market_value`, must not be `None`")  # noqa: E501

        self._market_value = market_value

    @property
    def period(self):
        """Gets the period of this ModelReturn.  # noqa: E501

        Show the returns on a Daily or Monthly period.  # noqa: E501

        :return: The period of this ModelReturn.  # noqa: E501
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period):
        """Sets the period of this ModelReturn.

        Show the returns on a Daily or Monthly period.  # noqa: E501

        :param period: The period of this ModelReturn.  # noqa: E501
        :type: str
        """

        self._period = period

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ModelReturn):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
