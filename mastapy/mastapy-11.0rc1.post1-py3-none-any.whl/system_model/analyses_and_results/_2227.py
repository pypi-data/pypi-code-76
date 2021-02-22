'''_2227.py

ModalAnalysesatStiffnessesAnalysis
'''


from mastapy.system_model.analyses_and_results import _2214
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSESAT_STIFFNESSES_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ModalAnalysesatStiffnessesAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysesatStiffnessesAnalysis',)


class ModalAnalysesatStiffnessesAnalysis(_2214.SingleAnalysis):
    '''ModalAnalysesatStiffnessesAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSESAT_STIFFNESSES_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysesatStiffnessesAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
