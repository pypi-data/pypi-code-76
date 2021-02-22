'''_2207.py

ModalAnalysesataStiffnessAnalysis
'''


from mastapy.system_model.analyses_and_results import _2196
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSESATA_STIFFNESS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ModalAnalysesataStiffnessAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysesataStiffnessAnalysis',)


class ModalAnalysesataStiffnessAnalysis(_2196.SingleAnalysis):
    '''ModalAnalysesataStiffnessAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSESATA_STIFFNESS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysesataStiffnessAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
