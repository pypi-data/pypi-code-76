'''_3643.py

PointLoadCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2144
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3512
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3679
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'PointLoadCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundStabilityAnalysis',)


class PointLoadCompoundStabilityAnalysis(_3679.VirtualComponentCompoundStabilityAnalysis):
    '''PointLoadCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2144.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2144.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3512.PointLoadStabilityAnalysis]':
        '''List[PointLoadStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3512.PointLoadStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3512.PointLoadStabilityAnalysis]':
        '''List[PointLoadStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3512.PointLoadStabilityAnalysis))
        return value
