'''_1342.py

PropertySpecificationMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_PROPERTY_SPECIFICATION_METHOD = python_net_import('SMT.MastaAPI.Utility.Enums', 'PropertySpecificationMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('PropertySpecificationMethod',)


class PropertySpecificationMethod(Enum):
    '''PropertySpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _PROPERTY_SPECIFICATION_METHOD

    __hash__ = None

    CONSTANT = 0
    ONEDIMENSIONAL_LOOKUP_TABLE = 1
    TWODIMENSIONAL_LOOKUP_TABLE = 2


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


PropertySpecificationMethod.__setattr__ = __enum_setattr
PropertySpecificationMethod.__delattr__ = __enum_delattr
