'''_6321.py

BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2187
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6319, _6320, _6326
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6190
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'BevelDifferentialGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundCriticalSpeedAnalysis',)


class BevelDifferentialGearSetCompoundCriticalSpeedAnalysis(_6326.BevelGearSetCompoundCriticalSpeedAnalysis):
    '''BevelDifferentialGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2187.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2187.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_critical_speed_analysis(self) -> 'List[_6319.BevelDifferentialGearCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundCriticalSpeedAnalysis, constructor.new(_6319.BevelDifferentialGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_critical_speed_analysis(self) -> 'List[_6320.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis]: 'BevelDifferentialMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6320.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6190.BevelDifferentialGearSetCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6190.BevelDifferentialGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6190.BevelDifferentialGearSetCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6190.BevelDifferentialGearSetCriticalSpeedAnalysis))
        return value
