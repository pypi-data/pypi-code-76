# encoding: utf8
from pint import Quantity


class ServiceAbstract:
    """
    Base class of services
    """

    @classmethod
    def unit_convert(cls, value, from_unit, to_unit):
        """
        Convert a value from an unit to another unit
        :param value: The value to convert
        :param from_unit: The source unit
        :param to_unit: The destination unit
        :return: The converted value
        :rtype: int|float
        """
        quantity = Quantity(value, from_unit)
        return quantity.to(to_unit).magnitude
