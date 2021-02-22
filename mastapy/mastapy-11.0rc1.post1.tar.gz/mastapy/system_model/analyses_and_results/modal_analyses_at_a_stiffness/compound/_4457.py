'''_4457.py

ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4363
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness',)


class ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness(_4363.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness):
    '''ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
