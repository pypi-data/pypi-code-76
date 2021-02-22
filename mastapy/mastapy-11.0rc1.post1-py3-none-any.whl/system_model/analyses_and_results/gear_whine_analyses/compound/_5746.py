'''_5746.py

BevelDifferentialGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5744, _5745, _5751
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5330
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'BevelDifferentialGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundGearWhineAnalysis',)


class BevelDifferentialGearSetCompoundGearWhineAnalysis(_5751.BevelGearSetCompoundGearWhineAnalysis):
    '''BevelDifferentialGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundGearWhineAnalysis.TYPE'):
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
    def bevel_differential_gears_compound_gear_whine_analysis(self) -> 'List[_5744.BevelDifferentialGearCompoundGearWhineAnalysis]':
        '''List[BevelDifferentialGearCompoundGearWhineAnalysis]: 'BevelDifferentialGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundGearWhineAnalysis, constructor.new(_5744.BevelDifferentialGearCompoundGearWhineAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_gear_whine_analysis(self) -> 'List[_5745.BevelDifferentialGearMeshCompoundGearWhineAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundGearWhineAnalysis]: 'BevelDifferentialMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundGearWhineAnalysis, constructor.new(_5745.BevelDifferentialGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5330.BevelDifferentialGearSetGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5330.BevelDifferentialGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5330.BevelDifferentialGearSetGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5330.BevelDifferentialGearSetGearWhineAnalysis))
        return value
