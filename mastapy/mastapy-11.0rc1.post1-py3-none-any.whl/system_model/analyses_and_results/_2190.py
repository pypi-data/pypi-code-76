'''_2190.py

ModalAnalysisforWhineAnalysis
'''


from mastapy.system_model.analyses_and_results import _2175
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSISFOR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ModalAnalysisforWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisforWhineAnalysis',)


class ModalAnalysisforWhineAnalysis(_2175.SingleAnalysis):
    '''ModalAnalysisforWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSISFOR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisforWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
