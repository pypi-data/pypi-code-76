'''_2401.py

CycloidalDiscPlanetaryBearingConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2014
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6491
from mastapy.system_model.analyses_and_results.power_flows import _3737
from mastapy.system_model.analyses_and_results.system_deflections import _2357
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CycloidalDiscPlanetaryBearingConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionSystemDeflection',)


class CycloidalDiscPlanetaryBearingConnectionSystemDeflection(_2357.AbstractShaftToMountableComponentConnectionSystemDeflection):
    '''CycloidalDiscPlanetaryBearingConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6491.CycloidalDiscPlanetaryBearingConnectionLoadCase':
        '''CycloidalDiscPlanetaryBearingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6491.CycloidalDiscPlanetaryBearingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3737.CycloidalDiscPlanetaryBearingConnectionPowerFlow':
        '''CycloidalDiscPlanetaryBearingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3737.CycloidalDiscPlanetaryBearingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
