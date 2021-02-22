'''_2005.py

ImportedFEType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_TYPE = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEType')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEType',)


class ImportedFEType(Enum):
    '''ImportedFEType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _IMPORTED_FE_TYPE

    __hash__ = None

    FULL_FE_MESH = 0
    EXTERNALLY_REDUCED_FE = 1
    CREATE_SHAFT_MESH = 2


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


ImportedFEType.__setattr__ = __enum_setattr
ImportedFEType.__delattr__ = __enum_delattr
