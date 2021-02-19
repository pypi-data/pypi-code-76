'''_992.py

ReadonlyToothThicknessSpecification
'''


from mastapy.gears.gear_designs.cylindrical import _1009
from mastapy._internal.python_net import python_net_import

_READONLY_TOOTH_THICKNESS_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ReadonlyToothThicknessSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('ReadonlyToothThicknessSpecification',)


class ReadonlyToothThicknessSpecification(_1009.ToothThicknessSpecification):
    '''ReadonlyToothThicknessSpecification

    This is a mastapy class.
    '''

    TYPE = _READONLY_TOOTH_THICKNESS_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ReadonlyToothThicknessSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
