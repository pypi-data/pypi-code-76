'''_3618.py

GuideDxfModelCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3487
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3582
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'GuideDxfModelCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundStabilityAnalysis',)


class GuideDxfModelCompoundStabilityAnalysis(_3582.ComponentCompoundStabilityAnalysis):
    '''GuideDxfModelCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3487.GuideDxfModelStabilityAnalysis]':
        '''List[GuideDxfModelStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3487.GuideDxfModelStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3487.GuideDxfModelStabilityAnalysis]':
        '''List[GuideDxfModelStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3487.GuideDxfModelStabilityAnalysis))
        return value
