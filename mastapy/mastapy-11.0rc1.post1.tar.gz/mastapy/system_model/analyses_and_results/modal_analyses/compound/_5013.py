'''_5013.py

SynchroniserCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2273
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4868
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4998
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SynchroniserCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundModalAnalysis',)


class SynchroniserCompoundModalAnalysis(_4998.SpecialisedAssemblyCompoundModalAnalysis):
    '''SynchroniserCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2273.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2273.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2273.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4868.SynchroniserModalAnalysis]':
        '''List[SynchroniserModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4868.SynchroniserModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4868.SynchroniserModalAnalysis]':
        '''List[SynchroniserModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4868.SynchroniserModalAnalysis))
        return value
