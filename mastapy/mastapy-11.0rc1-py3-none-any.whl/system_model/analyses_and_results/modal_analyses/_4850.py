'''_4850.py

ShaftModalAnalysisMode
'''


from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_MODAL_ANALYSIS_MODE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ShaftModalAnalysisMode')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftModalAnalysisMode',)


class ShaftModalAnalysisMode(_0.APIBase):
    '''ShaftModalAnalysisMode

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MODAL_ANALYSIS_MODE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftModalAnalysisMode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
