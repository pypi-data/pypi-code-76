'''_6745.py

SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets.couplings import _2026
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6586
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6679
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation',)


class SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation(_6679.CouplingConnectionAdvancedTimeSteppingAnalysisForModulation):
    '''SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2026.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2026.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6586.SpringDamperConnectionLoadCase':
        '''SpringDamperConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6586.SpringDamperConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
