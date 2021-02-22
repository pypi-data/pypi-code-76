'''_607.py

ContactResultType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CONTACT_RESULT_TYPE = python_net_import('SMT.MastaAPI.Gears.LTCA', 'ContactResultType')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactResultType',)


class ContactResultType(Enum):
    '''ContactResultType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CONTACT_RESULT_TYPE

    __hash__ = None

    MAX_PRESSURE = 0
    FORCE_PER_UNIT_LENGTH = 1
    HERTZIAN_CONTACT_HALF_WIDTH = 2
    MAX_SHEAR_STRESS = 3
    DEPTH_OF_MAX_SHEAR_STRESS = 4
    TOTAL_DEFLECTION_FOR_MESH = 5
    SLIDING_VELOCITY = 6
    PRESSURE_VELOCITY_PV = 7
    MINIMUM_FILM_THICKNESS_ISOTR_1514412014 = 8
    SPECIFIC_FILM_THICKNESS_ISOTR_1514412014 = 9
    MICROPITTING_SAFETY_FACTOR_ISOTR_1514412014 = 10
    MICROPITTING_FLASH_TEMPERATURE_ISOTR_1514412014 = 11
    MICROPITTING_CONTACT_TEMPERATURE_ISOTR_1514412014 = 12
    COEFFICIENT_OF_FRICTION_BENEDICT_AND_KELLEY = 13
    SLIDING_POWER_LOSS = 14
    SCUFFING_FLASH_TEMPERATURE_ISOTR_1398912000 = 15
    SCUFFING_CONTACT_TEMPERATURE_ISOTR_1398912000 = 16
    SCUFFING_SAFETY_FACTOR_ISOTR_1398912000 = 17
    SCUFFING_FLASH_TEMPERATURE_AGMA_925A03 = 18
    SCUFFING_CONTACT_TEMPERATURE_AGMA_925A03 = 19
    SCUFFING_SAFETY_FACTOR_AGMA_925A03 = 20
    SCUFFING_FLASH_TEMPERATURE_DIN_399041987 = 21
    SCUFFING_CONTACT_TEMPERATURE_DIN_399041987 = 22
    SCUFFING_SAFETY_FACTOR_DIN_399041987 = 23
    GAP_BETWEEN_LOADED_FLANKS_TRANSVERSE = 24
    GAP_BETWEEN_UNLOADED_FLANKS_TRANSVERSE = 25


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


ContactResultType.__setattr__ = __enum_setattr
ContactResultType.__delattr__ = __enum_delattr
