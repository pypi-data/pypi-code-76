'''_5549.py

ModalAnalysisForWhine
'''


from mastapy.system_model.analyses_and_results.modal_analyses import _4841, _4838
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_FOR_WHINE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ModalAnalysisForWhine')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisForWhine',)


class ModalAnalysisForWhine(_4838.ModalAnalysis):
    '''ModalAnalysisForWhine

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_FOR_WHINE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisForWhine.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_settings(self) -> '_4841.ModalAnalysisOptions':
        '''ModalAnalysisOptions: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4841.ModalAnalysisOptions)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None
