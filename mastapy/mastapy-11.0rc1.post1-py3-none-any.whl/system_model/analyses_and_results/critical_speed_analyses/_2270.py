'''_2270.py

CriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6185
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _7147
from mastapy._internal.python_net import python_net_import

_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CriticalSpeedAnalysis',)


class CriticalSpeedAnalysis(_7147.StaticLoadAnalysisCase):
    '''CriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def critical_speed_analysis_options(self) -> '_6185.CriticalSpeedAnalysisOptions':
        '''CriticalSpeedAnalysisOptions: 'CriticalSpeedAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6185.CriticalSpeedAnalysisOptions)(self.wrapped.CriticalSpeedAnalysisOptions) if self.wrapped.CriticalSpeedAnalysisOptions else None
