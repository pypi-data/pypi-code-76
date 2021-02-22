'''_5814.py

PlanetCarrierCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2069
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5421
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5806
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'PlanetCarrierCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundGearWhineAnalysis',)


class PlanetCarrierCompoundGearWhineAnalysis(_5806.MountableComponentCompoundGearWhineAnalysis):
    '''PlanetCarrierCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2069.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2069.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5421.PlanetCarrierGearWhineAnalysis]':
        '''List[PlanetCarrierGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5421.PlanetCarrierGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5421.PlanetCarrierGearWhineAnalysis]':
        '''List[PlanetCarrierGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5421.PlanetCarrierGearWhineAnalysis))
        return value
