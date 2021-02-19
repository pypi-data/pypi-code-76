"""JUICE CReMA ESA module."""

from .crema import CReMACollection
from .vars import DATA


class JUICE_CReMA(metaclass=CReMACollection):  # pylint: disable=R0903
    """JUICE Consolidated Report on Mission Analysis (CReMA).

    The complete JUICE Operation SPICE Kernel Dataset can be found here:

        https://doi.org/10.5270/esa-ybmj68p

    """

    URL = 'https://www.cosmos.esa.int/web/spice/spice-for-juice'

    CSV = DATA / 'juice_crema.csv'
