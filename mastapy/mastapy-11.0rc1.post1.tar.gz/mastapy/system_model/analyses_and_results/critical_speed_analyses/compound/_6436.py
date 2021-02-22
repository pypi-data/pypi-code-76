'''_6436.py

ZerolBevelGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2225
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6434, _6435, _6326
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6307
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'ZerolBevelGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundCriticalSpeedAnalysis',)


class ZerolBevelGearSetCompoundCriticalSpeedAnalysis(_6326.BevelGearSetCompoundCriticalSpeedAnalysis):
    '''ZerolBevelGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2225.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2225.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_critical_speed_analysis(self) -> 'List[_6434.ZerolBevelGearCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearCompoundCriticalSpeedAnalysis]: 'ZerolBevelGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundCriticalSpeedAnalysis, constructor.new(_6434.ZerolBevelGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_critical_speed_analysis(self) -> 'List[_6435.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearMeshCompoundCriticalSpeedAnalysis]: 'ZerolBevelMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6435.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6307.ZerolBevelGearSetCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6307.ZerolBevelGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6307.ZerolBevelGearSetCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6307.ZerolBevelGearSetCriticalSpeedAnalysis))
        return value
