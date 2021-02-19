'''_392.py

CylindricalCutterDatabase
'''


from typing import Generic, TypeVar

from mastapy.utility.databases import _1360
from mastapy.gears.manufacturing.cylindrical.cutters import _513
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_CUTTER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalCutterDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalCutterDatabase',)


T = TypeVar('T', bound='_513.CylindricalGearRealCutterDesign')


class CylindricalCutterDatabase(_1360.NamedDatabase['T'], Generic[T]):
    '''CylindricalCutterDatabase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _CYLINDRICAL_CUTTER_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalCutterDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
