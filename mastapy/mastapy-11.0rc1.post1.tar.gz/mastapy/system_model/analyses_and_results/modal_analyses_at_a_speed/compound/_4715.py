'''_4715.py

ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4621
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed',)


class ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed(_4621.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed):
    '''ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
