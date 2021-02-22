'''_2226.py

ModalAnalysesatSpeedsAnalysis
'''


from mastapy.system_model.analyses_and_results import _2214
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSESAT_SPEEDS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ModalAnalysesatSpeedsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysesatSpeedsAnalysis',)


class ModalAnalysesatSpeedsAnalysis(_2214.SingleAnalysis):
    '''ModalAnalysesatSpeedsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSESAT_SPEEDS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysesatSpeedsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
