'''_2256.py

CompoundModalAnalysesatSpeedsAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_MODAL_ANALYSESAT_SPEEDS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundModalAnalysesatSpeedsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundModalAnalysesatSpeedsAnalysis',)


class CompoundModalAnalysesatSpeedsAnalysis(_2213.CompoundAnalysis):
    '''CompoundModalAnalysesatSpeedsAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_MODAL_ANALYSESAT_SPEEDS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundModalAnalysesatSpeedsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
