'''_2206.py

ModalAnalysesataSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results import _2196
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSESATA_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ModalAnalysesataSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysesataSpeedAnalysis',)


class ModalAnalysesataSpeedAnalysis(_2196.SingleAnalysis):
    '''ModalAnalysesataSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSESATA_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysesataSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
