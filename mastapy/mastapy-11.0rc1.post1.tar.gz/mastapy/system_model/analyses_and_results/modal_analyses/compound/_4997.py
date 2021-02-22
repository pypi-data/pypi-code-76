'''_4997.py

ShaftToMountableComponentConnectionCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4903
from mastapy._internal.python_net import python_net_import

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ShaftToMountableComponentConnectionCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftToMountableComponentConnectionCompoundModalAnalysis',)


class ShaftToMountableComponentConnectionCompoundModalAnalysis(_4903.AbstractShaftToMountableComponentConnectionCompoundModalAnalysis):
    '''ShaftToMountableComponentConnectionCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftToMountableComponentConnectionCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
