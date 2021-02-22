import numpy as np
import re
import logging
from typing import Union

logger = logging.getLogger(__name__)


class UnitPrefixDict(dict):
    """Dictionary mapping standard prefixes for SI units on corresponding orders of magnitude.

    Additional functionalities implemented:
    - inverse mapping (order -> prefix)
    - matching closest defined prefix (if the order is too small/too big for the defined prefixes)
    """

    def __init__(self, *args, **kwargs):
        super(UnitPrefixDict, self).__init__(*args, **kwargs)

        # verify the type and values
        for key, value in self.items():
            self._check_item(key, value)

        # define the inverse mapping
        self._inverse = {}
        self._update_inverse()

    def _update_inverse(self):
        """Update the inverse mapping (to be called in __init__ and __setitem__)."""

        self._check_unique_orders()
        self._inverse = {v: k for k, v in self.items()}

    def _check_unique_orders(self):
        """Verify that the set of orders (dictionary values) is unique, so that the inverse mapping can be defined."""

        if len(set(self.values())) < len(self):
            raise ValueError(f"Orders must be unique")

    @property
    def inverse(self):
        return self._inverse

    @staticmethod
    def _check_item(key, value):
        """Verify that the prefixes and orders are of proper type and value."""

        if not isinstance(key, str):
            raise TypeError(f"Prefix should be a string (got '{key}' of type '{type(key)}')")

        if not isinstance(value, int):
            raise TypeError(f"Order should be an integer (got '{value}' of type '{type(value)}')")

        UnitPrefixDict._check_order_value(value)

    @staticmethod
    def _check_order_value(order):
        """Verify that the order is divisible by 3."""

        if divmod(order, 3)[1]:
            raise ValueError(f"Order should be an integer multiple of 3 (got {order})")

    def __setitem__(self, key: str, value: int):
        self._check_item(key, value)
        super(UnitPrefixDict, self).__setitem__(key, value)
        self._update_inverse()

    def get_prefix(self, order: int):
        """Get a prefix corresponding to the given order."""

        order = int(order)

        self._check_order_value(order)

        if order not in self.values():
            logger.warning(f"No prefix defined for value order {order}")
            return

        return self._inverse[order]

    def match_prefix(self, order: int):
        """Look for the closest defined prefix corresponding to the given order."""

        prefix = self.get_prefix(order)

        if prefix is None:
            prefix, order = self.match_prefix(order - 3 if order > max(self.values()) else order + 3)

        return prefix, order


class ScaleManager(object):
    # units prefixes
    PREFIX_DICT = UnitPrefixDict({'': 0, 'k': 3, 'M': 6, 'G': 9, 'T': 12,
                                  'm': -3, 'u': -6, 'n': -9, 'p': -12, 'f': -15})

    @staticmethod
    def rescale_data(data, order_change: int):
        """Rescale data with the given order of magnitude (exponent of 10)."""

        if order_change == 0:
            return data
        return data * ScaleManager.scaling_factor_from_order(order_change)

    @staticmethod
    def scaling_factor_from_order(order):
        return 10 ** (-order)

    @staticmethod
    def split_unit(unit: str):
        """Split unit to prefix and base."""

        # split the unit to a prefix and the core part
        unit_split_match = re.search("(?P<prefix>[a-zA-Z]?)(?P<core>[a-zA-Z]+((/[a-zA-Z]+)?))", unit)
        if not unit_split_match:
            raise ValueError(f"Invalid unit format: {unit}")
        prefix = unit_split_match.group('prefix')  # e.g. 'p' in 'pm/s'

        if prefix in ScaleManager.PREFIX_DICT.keys():
            unit_core = unit_split_match.group('core')  # main part of the unit (e.g. 'm/s' in 'pm/s')
        else:
            # prefix is empty or is in fact a part of the unit (e.g. 'H' in 'Hz')
            prefix = ''
            unit_core = unit

        return prefix, unit_core

    @staticmethod
    def rescale_unit(unit: str, order_change: int):
        """Adjust rescaling order and change the unit prefix accordingly.

        Returns
        -------
        unit_rescaled   :   str
            the rescaled unit
        order           :   int
            adjusted order to be applied for rescaling the corresponding data
        """

        if order_change == 0:
            return unit, order_change

        prefix, unit_core = ScaleManager.split_unit(unit)
        unit_order = ScaleManager.PREFIX_DICT[prefix]  # e.g. -12 for 'p'

        # define order for the new prefix
        order_for_prefix, order_remainder = divmod(order_change + unit_order, 3)
        order_for_prefix = 3 * order_for_prefix

        # order for prefix may be changed if there is no matching prefix -> rescale data differently
        prefix_new, order_for_prefix = ScaleManager.PREFIX_DICT.match_prefix(order_for_prefix)

        # assemble the final unit
        unit_rescaled = f"{prefix_new}{unit_core}" + (f" * 1E{order_remainder}" if order_remainder else "")

        return unit_rescaled, order_for_prefix - unit_order

    @staticmethod
    def order_from_unit(unit):
        prefix, _ = ScaleManager.split_unit(unit)
        return ScaleManager.PREFIX_DICT[prefix]  # e.g. -12 for 'p'

    @staticmethod
    def adjust_scale(data):
        """Propose a scaling factor magnitude (exponent of 10, an integer multiple of 3) to best represent the data."""

        max_val = np.nanmax(np.abs(data)).item() or 1  # 0 is not a valid argument for logarithm (next step)
        order = np.log10(max_val)
        order = np.sign(order) * np.floor(np.abs(order))
        return int(3 * (order // 3))

    @staticmethod
    def rescale(data, unit: str, order_change: int = None):
        """Rescale data and its unit. Rescaling order may be provided or automatically adjusted to the data."""

        # define the order
        if order_change is None:
            order_change = ScaleManager.adjust_scale(data)

        # adjust the order to the available prefixes; rescale the unit
        unit_rescaled, order_change = ScaleManager.rescale_unit(unit, order_change)

        # rescale the data
        return ScaleManager.rescale_data(data, order_change), unit_rescaled

    @staticmethod
    def rescale_to_basic(data, unit: str):
        """Rescale data and its unit to base unit, e.g. 3 kHz -> 3000 Hz, 0.2 mm -> 0.0002 m"""

        order_change = - ScaleManager.order_from_unit(unit)
        return ScaleManager.rescale(data, unit, order_change=order_change)

    @staticmethod
    def display(number: Union[float, complex], unit: str, precision: int = 2):
        """Rescale a number and its unit and return a string representation with given decimal precision."""

        n_rescaled, unit_rescaled = ScaleManager.rescale(number, unit)
        return f'{n_rescaled:.{precision}f} {unit_rescaled}'


