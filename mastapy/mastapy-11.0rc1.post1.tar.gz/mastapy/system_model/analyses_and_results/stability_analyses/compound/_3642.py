'''_3642.py

PlanetCarrierCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2142
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3511
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3634
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'PlanetCarrierCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundStabilityAnalysis',)


class PlanetCarrierCompoundStabilityAnalysis(_3634.MountableComponentCompoundStabilityAnalysis):
    '''PlanetCarrierCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2142.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3511.PlanetCarrierStabilityAnalysis]':
        '''List[PlanetCarrierStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3511.PlanetCarrierStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3511.PlanetCarrierStabilityAnalysis]':
        '''List[PlanetCarrierStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3511.PlanetCarrierStabilityAnalysis))
        return value
