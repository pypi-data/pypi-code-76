'''_5612.py

BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5610, _5611, _5617
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5488
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis',)


class BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis(_5617.BevelGearSetCompoundSingleMeshWhineAnalysis):
    '''BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2114.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2114.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_single_mesh_whine_analysis(self) -> 'List[_5610.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearCompoundSingleMeshWhineAnalysis]: 'BevelDifferentialGearsCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundSingleMeshWhineAnalysis, constructor.new(_5610.BevelDifferentialGearCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_single_mesh_whine_analysis(self) -> 'List[_5611.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]: 'BevelDifferentialMeshesCompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundSingleMeshWhineAnalysis, constructor.new(_5611.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5488.BevelDifferentialGearSetSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSetSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5488.BevelDifferentialGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_5488.BevelDifferentialGearSetSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSetSingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_5488.BevelDifferentialGearSetSingleMeshWhineAnalysis))
        return value
