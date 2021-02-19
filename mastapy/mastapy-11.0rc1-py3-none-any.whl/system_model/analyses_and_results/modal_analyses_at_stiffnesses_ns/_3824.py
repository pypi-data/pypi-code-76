'''_3824.py

CriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3858
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _6566
from mastapy._internal.python_net import python_net_import

_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'CriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CriticalSpeedAnalysis',)


class CriticalSpeedAnalysis(_6566.StaticLoadAnalysisCase):
    '''CriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def modal_analyses_at_stiffnesses_options(self) -> '_3858.ModalAnalysesAtStiffnessesOptions':
        '''ModalAnalysesAtStiffnessesOptions: 'ModalAnalysesAtStiffnessesOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3858.ModalAnalysesAtStiffnessesOptions)(self.wrapped.ModalAnalysesAtStiffnessesOptions) if self.wrapped.ModalAnalysesAtStiffnessesOptions else None
