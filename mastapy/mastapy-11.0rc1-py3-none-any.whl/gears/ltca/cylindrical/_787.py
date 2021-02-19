'''_787.py

CylindricalGearBendingStiffnessNode
'''


from mastapy.gears.ltca import _774
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_BENDING_STIFFNESS_NODE = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearBendingStiffnessNode')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearBendingStiffnessNode',)


class CylindricalGearBendingStiffnessNode(_774.GearBendingStiffnessNode):
    '''CylindricalGearBendingStiffnessNode

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_BENDING_STIFFNESS_NODE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearBendingStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
