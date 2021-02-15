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

class FixedLegAllOf(object):
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
        'start_date': 'datetime',
        'maturity_date': 'datetime',
        'leg_definition': 'LegDefinition',
        'notional': 'float',
        'overrides': 'FixedLegAllOfOverrides',
        'instrument_type': 'str'
    }

    attribute_map = {
        'start_date': 'startDate',
        'maturity_date': 'maturityDate',
        'leg_definition': 'legDefinition',
        'notional': 'notional',
        'overrides': 'overrides',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'start_date': 'required',
        'maturity_date': 'required',
        'leg_definition': 'required',
        'notional': 'required',
        'overrides': 'optional',
        'instrument_type': 'required'
    }

    def __init__(self, start_date=None, maturity_date=None, leg_definition=None, notional=None, overrides=None, instrument_type=None):  # noqa: E501
        """
        FixedLegAllOf - a model defined in OpenAPI

        :param start_date:  The start date of the instrument. This is normally synonymous with the trade-date. (required)
        :type start_date: datetime
        :param maturity_date:  The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date (required)
        :type maturity_date: datetime
        :param leg_definition:  (required)
        :type leg_definition: lusid.LegDefinition
        :param notional:  (required)
        :type notional: float
        :param overrides: 
        :type overrides: lusid.FixedLegAllOfOverrides
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashflowLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap (required)
        :type instrument_type: str

        """  # noqa: E501

        self._start_date = None
        self._maturity_date = None
        self._leg_definition = None
        self._notional = None
        self._overrides = None
        self._instrument_type = None
        self.discriminator = None

        self.start_date = start_date
        self.maturity_date = maturity_date
        self.leg_definition = leg_definition
        self.notional = notional
        self.overrides = overrides
        self.instrument_type = instrument_type

    @property
    def start_date(self):
        """Gets the start_date of this FixedLegAllOf.  # noqa: E501

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :return: The start_date of this FixedLegAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this FixedLegAllOf.

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :param start_date: The start_date of this FixedLegAllOf.  # noqa: E501
        :type: datetime
        """
        if start_date is None:
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def maturity_date(self):
        """Gets the maturity_date of this FixedLegAllOf.  # noqa: E501

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date  # noqa: E501

        :return: The maturity_date of this FixedLegAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._maturity_date

    @maturity_date.setter
    def maturity_date(self, maturity_date):
        """Sets the maturity_date of this FixedLegAllOf.

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date  # noqa: E501

        :param maturity_date: The maturity_date of this FixedLegAllOf.  # noqa: E501
        :type: datetime
        """
        if maturity_date is None:
            raise ValueError("Invalid value for `maturity_date`, must not be `None`")  # noqa: E501

        self._maturity_date = maturity_date

    @property
    def leg_definition(self):
        """Gets the leg_definition of this FixedLegAllOf.  # noqa: E501


        :return: The leg_definition of this FixedLegAllOf.  # noqa: E501
        :rtype: LegDefinition
        """
        return self._leg_definition

    @leg_definition.setter
    def leg_definition(self, leg_definition):
        """Sets the leg_definition of this FixedLegAllOf.


        :param leg_definition: The leg_definition of this FixedLegAllOf.  # noqa: E501
        :type: LegDefinition
        """
        if leg_definition is None:
            raise ValueError("Invalid value for `leg_definition`, must not be `None`")  # noqa: E501

        self._leg_definition = leg_definition

    @property
    def notional(self):
        """Gets the notional of this FixedLegAllOf.  # noqa: E501


        :return: The notional of this FixedLegAllOf.  # noqa: E501
        :rtype: float
        """
        return self._notional

    @notional.setter
    def notional(self, notional):
        """Sets the notional of this FixedLegAllOf.


        :param notional: The notional of this FixedLegAllOf.  # noqa: E501
        :type: float
        """
        if notional is None:
            raise ValueError("Invalid value for `notional`, must not be `None`")  # noqa: E501

        self._notional = notional

    @property
    def overrides(self):
        """Gets the overrides of this FixedLegAllOf.  # noqa: E501


        :return: The overrides of this FixedLegAllOf.  # noqa: E501
        :rtype: FixedLegAllOfOverrides
        """
        return self._overrides

    @overrides.setter
    def overrides(self, overrides):
        """Sets the overrides of this FixedLegAllOf.


        :param overrides: The overrides of this FixedLegAllOf.  # noqa: E501
        :type: FixedLegAllOfOverrides
        """

        self._overrides = overrides

    @property
    def instrument_type(self):
        """Gets the instrument_type of this FixedLegAllOf.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashflowLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap  # noqa: E501

        :return: The instrument_type of this FixedLegAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this FixedLegAllOf.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashflowLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap  # noqa: E501

        :param instrument_type: The instrument_type of this FixedLegAllOf.  # noqa: E501
        :type: str
        """
        if instrument_type is None:
            raise ValueError("Invalid value for `instrument_type`, must not be `None`")  # noqa: E501
        allowed_values = ["QuotedSecurity", "InterestRateSwap", "FxForward", "Future", "ExoticInstrument", "FxOption", "CreditDefaultSwap", "InterestRateSwaption", "Bond", "EquityOption", "FixedLeg", "FloatingLeg", "BespokeCashflowLeg", "Unknown", "TermDeposit", "ContractForDifference", "EquitySwap"]  # noqa: E501
        if instrument_type not in allowed_values:
            raise ValueError(
                "Invalid value for `instrument_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_type, allowed_values)
            )

        self._instrument_type = instrument_type

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
        if not isinstance(other, FixedLegAllOf):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
