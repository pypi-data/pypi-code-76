'''_2259.py

CompoundModalAnalysisforWhineAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_MODAL_ANALYSISFOR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundModalAnalysisforWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundModalAnalysisforWhineAnalysis',)


class CompoundModalAnalysisforWhineAnalysis(_2213.CompoundAnalysis):
    '''CompoundModalAnalysisforWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_MODAL_ANALYSISFOR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundModalAnalysisforWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
