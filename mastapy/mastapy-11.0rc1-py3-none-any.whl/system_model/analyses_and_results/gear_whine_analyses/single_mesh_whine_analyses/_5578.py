'''_5578.py

StraightBevelDiffGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2144
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6257
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5579, _5577, _5493
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'StraightBevelDiffGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetSingleMeshWhineAnalysis',)


class StraightBevelDiffGearSetSingleMeshWhineAnalysis(_5493.BevelGearSetSingleMeshWhineAnalysis):
    '''StraightBevelDiffGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2144.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2144.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6257.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6257.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_single_mesh_whine_analysis(self) -> 'List[_5579.StraightBevelDiffGearSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearSingleMeshWhineAnalysis]: 'StraightBevelDiffGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsSingleMeshWhineAnalysis, constructor.new(_5579.StraightBevelDiffGearSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_single_mesh_whine_analysis(self) -> 'List[_5577.StraightBevelDiffGearMeshSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearMeshSingleMeshWhineAnalysis]: 'StraightBevelDiffMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesSingleMeshWhineAnalysis, constructor.new(_5577.StraightBevelDiffGearMeshSingleMeshWhineAnalysis))
        return value
