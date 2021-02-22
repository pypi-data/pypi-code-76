'''_1088.py

ConceptGearSetDesign
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.concept import _1086, _1087
from mastapy.gears.gear_designs import _879
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Concept', 'ConceptGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetDesign',)


class ConceptGearSetDesign(_879.GearSetDesign):
    '''ConceptGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def working_normal_pressure_angle_gear_a_concave_flank(self) -> 'float':
        '''float: 'WorkingNormalPressureAngleGearAConcaveFlank' is the original name of this property.'''

        return self.wrapped.WorkingNormalPressureAngleGearAConcaveFlank

    @working_normal_pressure_angle_gear_a_concave_flank.setter
    def working_normal_pressure_angle_gear_a_concave_flank(self, value: 'float'):
        self.wrapped.WorkingNormalPressureAngleGearAConcaveFlank = float(value) if value else 0.0

    @property
    def working_normal_pressure_angle_gear_a_convex_flank(self) -> 'float':
        '''float: 'WorkingNormalPressureAngleGearAConvexFlank' is the original name of this property.'''

        return self.wrapped.WorkingNormalPressureAngleGearAConvexFlank

    @working_normal_pressure_angle_gear_a_convex_flank.setter
    def working_normal_pressure_angle_gear_a_convex_flank(self, value: 'float'):
        self.wrapped.WorkingNormalPressureAngleGearAConvexFlank = float(value) if value else 0.0

    @property
    def gears(self) -> 'List[_1086.ConceptGearDesign]':
        '''List[ConceptGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_1086.ConceptGearDesign))
        return value

    @property
    def concept_gears(self) -> 'List[_1086.ConceptGearDesign]':
        '''List[ConceptGearDesign]: 'ConceptGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGears, constructor.new(_1086.ConceptGearDesign))
        return value

    @property
    def concept_meshes(self) -> 'List[_1087.ConceptGearMeshDesign]':
        '''List[ConceptGearMeshDesign]: 'ConceptMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshes, constructor.new(_1087.ConceptGearMeshDesign))
        return value
