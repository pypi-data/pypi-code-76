'''_5581.py

StraightBevelGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2146
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6260
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5582, _5580, _5493
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'StraightBevelGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetSingleMeshWhineAnalysis',)


class StraightBevelGearSetSingleMeshWhineAnalysis(_5493.BevelGearSetSingleMeshWhineAnalysis):
    '''StraightBevelGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2146.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2146.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6260.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6260.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_single_mesh_whine_analysis(self) -> 'List[_5582.StraightBevelGearSingleMeshWhineAnalysis]':
        '''List[StraightBevelGearSingleMeshWhineAnalysis]: 'StraightBevelGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsSingleMeshWhineAnalysis, constructor.new(_5582.StraightBevelGearSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_meshes_single_mesh_whine_analysis(self) -> 'List[_5580.StraightBevelGearMeshSingleMeshWhineAnalysis]':
        '''List[StraightBevelGearMeshSingleMeshWhineAnalysis]: 'StraightBevelMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesSingleMeshWhineAnalysis, constructor.new(_5580.StraightBevelGearMeshSingleMeshWhineAnalysis))
        return value
