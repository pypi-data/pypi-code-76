'''_2049.py

ConcentricPartGroup
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1061
from mastapy.system_model.part_model.part_groups import _2050, _2048
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_PART_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'ConcentricPartGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricPartGroup',)


class ConcentricPartGroup(_2048.ConcentricOrParallelPartGroup):
    '''ConcentricPartGroup

    This is a mastapy class.
    '''

    TYPE = _CONCENTRIC_PART_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConcentricPartGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def total_of_cylindrical_gear_face_widths(self) -> 'float':
        '''float: 'TotalOfCylindricalGearFaceWidths' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalOfCylindricalGearFaceWidths

    @property
    def radial_position(self) -> '_1061.Vector2D':
        '''Vector2D: 'RadialPosition' is the original name of this property.'''

        return constructor.new(_1061.Vector2D)(self.wrapped.RadialPosition) if self.wrapped.RadialPosition else None

    @radial_position.setter
    def radial_position(self, value: '_1061.Vector2D'):
        value = value.wrapped if value else None
        self.wrapped.RadialPosition = value

    @property
    def parallel_groups(self) -> 'List[_2050.ConcentricPartGroupParallelToThis]':
        '''List[ConcentricPartGroupParallelToThis]: 'ParallelGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelGroups, constructor.new(_2050.ConcentricPartGroupParallelToThis))
        return value
