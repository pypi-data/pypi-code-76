'''_4925.py

ComponentCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4979
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ComponentCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundModalAnalysis',)


class ComponentCompoundModalAnalysis(_4979.PartCompoundModalAnalysis):
    '''ComponentCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
