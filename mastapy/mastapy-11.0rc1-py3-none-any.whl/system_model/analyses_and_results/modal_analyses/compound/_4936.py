'''_4936.py

ConnectorCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4977
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ConnectorCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundModalAnalysis',)


class ConnectorCompoundModalAnalysis(_4977.MountableComponentCompoundModalAnalysis):
    '''ConnectorCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
