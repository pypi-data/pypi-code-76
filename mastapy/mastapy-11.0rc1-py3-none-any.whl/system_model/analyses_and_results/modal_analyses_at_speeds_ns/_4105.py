'''_4105.py

ModalAnalysisAtSpeedsDrawStyle
'''


from mastapy.system_model.analyses_and_results.rotor_dynamics import _3274
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_AT_SPEEDS_DRAW_STYLE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ModalAnalysisAtSpeedsDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisAtSpeedsDrawStyle',)


class ModalAnalysisAtSpeedsDrawStyle(_3274.RotorDynamicsDrawStyle):
    '''ModalAnalysisAtSpeedsDrawStyle

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_AT_SPEEDS_DRAW_STYLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisAtSpeedsDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
