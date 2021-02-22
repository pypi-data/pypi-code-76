'''_3859.py

ModalAnalysisAtStiffnessesDrawStyle
'''


from mastapy.system_model.analyses_and_results.rotor_dynamics import _3274
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_AT_STIFFNESSES_DRAW_STYLE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ModalAnalysisAtStiffnessesDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisAtStiffnessesDrawStyle',)


class ModalAnalysisAtStiffnessesDrawStyle(_3274.RotorDynamicsDrawStyle):
    '''ModalAnalysisAtStiffnessesDrawStyle

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_AT_STIFFNESSES_DRAW_STYLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisAtStiffnessesDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
