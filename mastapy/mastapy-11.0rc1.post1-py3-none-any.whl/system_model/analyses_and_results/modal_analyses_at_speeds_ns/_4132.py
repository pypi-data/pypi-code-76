'''_4132.py

StabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4104
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _6566
from mastapy._internal.python_net import python_net_import

_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StabilityAnalysis',)


class StabilityAnalysis(_6566.StaticLoadAnalysisCase):
    '''StabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def modal_analyses_at_speeds_options(self) -> '_4104.ModalAnalysesAtSpeedsOptions':
        '''ModalAnalysesAtSpeedsOptions: 'ModalAnalysesAtSpeedsOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4104.ModalAnalysesAtSpeedsOptions)(self.wrapped.ModalAnalysesAtSpeedsOptions) if self.wrapped.ModalAnalysesAtSpeedsOptions else None
