'''_3776.py

PlanetaryConnectionPowerFlow
'''


from mastapy.system_model.connections_and_sockets import _1963
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6561
from mastapy.system_model.analyses_and_results.power_flows import _3792
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PlanetaryConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionPowerFlow',)


class PlanetaryConnectionPowerFlow(_3792.ShaftToMountableComponentConnectionPowerFlow):
    '''PlanetaryConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionPowerFlow.TYPE'):
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
