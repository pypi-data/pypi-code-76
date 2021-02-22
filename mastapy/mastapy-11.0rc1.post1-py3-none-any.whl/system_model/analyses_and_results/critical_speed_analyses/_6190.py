'''_6190.py

BevelDifferentialGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2187
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6456
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6188, _6189, _6195
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'BevelDifferentialGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCriticalSpeedAnalysis',)


class BevelDifferentialGearSetCriticalSpeedAnalysis(_6195.BevelGearSetCriticalSpeedAnalysis):
    '''BevelDifferentialGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2187.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6456.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6456.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_critical_speed_analysis(self) -> 'List[_6188.BevelDifferentialGearCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearCriticalSpeedAnalysis]: 'BevelDifferentialGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCriticalSpeedAnalysis, constructor.new(_6188.BevelDifferentialGearCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_meshes_critical_speed_analysis(self) -> 'List[_6189.BevelDifferentialGearMeshCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearMeshCriticalSpeedAnalysis]: 'BevelDifferentialMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCriticalSpeedAnalysis, constructor.new(_6189.BevelDifferentialGearMeshCriticalSpeedAnalysis))
        return value
