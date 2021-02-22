'''_3652.py

ShaftCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2154
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3522
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3558
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ShaftCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundStabilityAnalysis',)


class ShaftCompoundStabilityAnalysis(_3558.AbstractShaftCompoundStabilityAnalysis):
    '''ShaftCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2154.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3522.ShaftStabilityAnalysis]':
        '''List[ShaftStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3522.ShaftStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3522.ShaftStabilityAnalysis]':
        '''List[ShaftStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3522.ShaftStabilityAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundStabilityAnalysis]':
        '''List[ShaftCompoundStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundStabilityAnalysis))
        return value
