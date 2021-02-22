'''_4356.py

WormGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2223
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6616
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4355, _4354, _4291
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'WormGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetModalAnalysisAtAStiffness',)


class WormGearSetModalAnalysisAtAStiffness(_4291.GearSetModalAnalysisAtAStiffness):
    '''WormGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2223.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6616.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6616.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4355.WormGearModalAnalysisAtAStiffness]':
        '''List[WormGearModalAnalysisAtAStiffness]: 'WormGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsModalAnalysisAtAStiffness, constructor.new(_4355.WormGearModalAnalysisAtAStiffness))
        return value

    @property
    def worm_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4354.WormGearMeshModalAnalysisAtAStiffness]':
        '''List[WormGearMeshModalAnalysisAtAStiffness]: 'WormMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesModalAnalysisAtAStiffness, constructor.new(_4354.WormGearMeshModalAnalysisAtAStiffness))
        return value
