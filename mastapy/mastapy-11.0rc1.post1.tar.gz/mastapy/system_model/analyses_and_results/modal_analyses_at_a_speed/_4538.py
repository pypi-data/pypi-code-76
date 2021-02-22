'''_4538.py

CylindricalGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2197, _2213
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6496, _6562
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4537, _4536, _4549
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'CylindricalGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetModalAnalysisAtASpeed',)


class CylindricalGearSetModalAnalysisAtASpeed(_4549.GearSetModalAnalysisAtASpeed):
    '''CylindricalGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2197.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2197.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6496.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6496.CylindricalGearSetLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_modal_analysis_at_a_speed(self) -> 'List[_4537.CylindricalGearModalAnalysisAtASpeed]':
        '''List[CylindricalGearModalAnalysisAtASpeed]: 'CylindricalGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsModalAnalysisAtASpeed, constructor.new(_4537.CylindricalGearModalAnalysisAtASpeed))
        return value

    @property
    def cylindrical_meshes_modal_analysis_at_a_speed(self) -> 'List[_4536.CylindricalGearMeshModalAnalysisAtASpeed]':
        '''List[CylindricalGearMeshModalAnalysisAtASpeed]: 'CylindricalMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesModalAnalysisAtASpeed, constructor.new(_4536.CylindricalGearMeshModalAnalysisAtASpeed))
        return value
