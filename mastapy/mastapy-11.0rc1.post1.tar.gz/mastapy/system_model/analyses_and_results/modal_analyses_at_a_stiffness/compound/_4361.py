'''_4361.py

AbstractShaftCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4362
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'AbstractShaftCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftCompoundModalAnalysisAtAStiffness',)


class AbstractShaftCompoundModalAnalysisAtAStiffness(_4362.AbstractShaftOrHousingCompoundModalAnalysisAtAStiffness):
    '''AbstractShaftCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
