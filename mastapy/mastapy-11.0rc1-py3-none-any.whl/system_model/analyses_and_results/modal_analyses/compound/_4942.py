'''_4942.py

CVTPulleyCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4988
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CVTPulleyCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundModalAnalysis',)


class CVTPulleyCompoundModalAnalysis(_4988.PulleyCompoundModalAnalysis):
    '''CVTPulleyCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
