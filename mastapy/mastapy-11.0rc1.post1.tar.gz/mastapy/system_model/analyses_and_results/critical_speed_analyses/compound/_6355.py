'''_6355.py

CylindricalGearCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2196, _2198
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6226
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6366
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CylindricalGearCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundCriticalSpeedAnalysis',)


class CylindricalGearCompoundCriticalSpeedAnalysis(_6366.GearCompoundCriticalSpeedAnalysis):
    '''CylindricalGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2196.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6226.CylindricalGearCriticalSpeedAnalysis]':
        '''List[CylindricalGearCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6226.CylindricalGearCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6226.CylindricalGearCriticalSpeedAnalysis]':
        '''List[CylindricalGearCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6226.CylindricalGearCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundCriticalSpeedAnalysis]':
        '''List[CylindricalGearCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearCompoundCriticalSpeedAnalysis))
        return value
