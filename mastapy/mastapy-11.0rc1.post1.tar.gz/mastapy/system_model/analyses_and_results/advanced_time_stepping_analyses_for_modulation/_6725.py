'''_6725.py

PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets import _1963
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6561
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6739
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation',)


class PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation(_6739.ShaftToMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation):
    '''PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6561.PlanetaryConnectionLoadCase':
        '''PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6561.PlanetaryConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
