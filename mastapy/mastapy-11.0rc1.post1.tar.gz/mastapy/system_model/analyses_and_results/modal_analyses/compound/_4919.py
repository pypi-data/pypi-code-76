'''_4919.py

BoltCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2116
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4767
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4925
from mastapy._internal.python_net import python_net_import

_BOLT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BoltCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltCompoundModalAnalysis',)


class BoltCompoundModalAnalysis(_4925.ComponentCompoundModalAnalysis):
    '''BoltCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2116.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4767.BoltModalAnalysis]':
        '''List[BoltModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4767.BoltModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4767.BoltModalAnalysis]':
        '''List[BoltModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4767.BoltModalAnalysis))
        return value
