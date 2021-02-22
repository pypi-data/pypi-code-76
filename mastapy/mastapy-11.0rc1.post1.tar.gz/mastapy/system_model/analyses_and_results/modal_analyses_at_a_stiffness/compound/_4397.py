'''_4397.py

CouplingCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4458
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CouplingCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundModalAnalysisAtAStiffness',)


class CouplingCompoundModalAnalysisAtAStiffness(_4458.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness):
    '''CouplingCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
