'''_4979.py

PartCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'PartCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundModalAnalysis',)


class PartCompoundModalAnalysis(_7176.PartCompoundAnalysis):
    '''PartCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
