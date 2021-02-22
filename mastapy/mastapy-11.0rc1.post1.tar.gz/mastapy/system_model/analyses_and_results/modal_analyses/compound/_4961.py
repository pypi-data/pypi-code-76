'''_4961.py

GuideDxfModelCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4810
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4925
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'GuideDxfModelCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundModalAnalysis',)


class GuideDxfModelCompoundModalAnalysis(_4925.ComponentCompoundModalAnalysis):
    '''GuideDxfModelCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4810.GuideDxfModelModalAnalysis]':
        '''List[GuideDxfModelModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4810.GuideDxfModelModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4810.GuideDxfModelModalAnalysis]':
        '''List[GuideDxfModelModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4810.GuideDxfModelModalAnalysis))
        return value
