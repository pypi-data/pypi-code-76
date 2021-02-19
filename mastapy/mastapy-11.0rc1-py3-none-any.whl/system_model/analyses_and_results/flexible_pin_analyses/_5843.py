'''_5843.py

FlexiblePinAnalysisStopStartAnalysis
'''


from mastapy.system_model.analyses_and_results.system_deflections import _2353
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5837
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_STOP_START_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisStopStartAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisStopStartAnalysis',)


class FlexiblePinAnalysisStopStartAnalysis(_5837.FlexiblePinAnalysis):
    '''FlexiblePinAnalysisStopStartAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ANALYSIS_STOP_START_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisStopStartAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def shaft_nominal_load_case(self) -> '_2353.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'ShaftNominalLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2353.ShaftSystemDeflection)(self.wrapped.ShaftNominalLoadCase) if self.wrapped.ShaftNominalLoadCase else None

    @property
    def shaft_extreme_load_case(self) -> '_2353.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'ShaftExtremeLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2353.ShaftSystemDeflection)(self.wrapped.ShaftExtremeLoadCase) if self.wrapped.ShaftExtremeLoadCase else None
