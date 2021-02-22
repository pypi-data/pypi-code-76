'''_3536.py

BearingCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2089
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3404
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3564
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'BearingCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundStabilityAnalysis',)


class BearingCompoundStabilityAnalysis(_3564.ConnectorCompoundStabilityAnalysis):
    '''BearingCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2089.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3404.BearingStabilityAnalysis]':
        '''List[BearingStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3404.BearingStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3404.BearingStabilityAnalysis]':
        '''List[BearingStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3404.BearingStabilityAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundStabilityAnalysis]':
        '''List[BearingCompoundStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundStabilityAnalysis))
        return value
