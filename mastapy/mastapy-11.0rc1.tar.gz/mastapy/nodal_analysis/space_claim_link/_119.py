'''_119.py

SpaceClaimDimensionType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPACE_CLAIM_DIMENSION_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis.SpaceClaimLink', 'SpaceClaimDimensionType')


__docformat__ = 'restructuredtext en'
__all__ = ('SpaceClaimDimensionType',)


class SpaceClaimDimensionType(Enum):
    '''SpaceClaimDimensionType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _SPACE_CLAIM_DIMENSION_TYPE

    __hash__ = None

    UNITLESS = 0
    ANGLE = 1
    LENGTH = 2
    COUNT = 3


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


SpaceClaimDimensionType.__setattr__ = __enum_setattr
SpaceClaimDimensionType.__delattr__ = __enum_delattr
