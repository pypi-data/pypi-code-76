'''_6491.py

CycloidalDiscPlanetaryBearingConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _2014
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6441
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CycloidalDiscPlanetaryBearingConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionLoadCase',)


class CycloidalDiscPlanetaryBearingConnectionLoadCase(_6441.AbstractShaftToMountableComponentConnectionLoadCase):
    '''CycloidalDiscPlanetaryBearingConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
