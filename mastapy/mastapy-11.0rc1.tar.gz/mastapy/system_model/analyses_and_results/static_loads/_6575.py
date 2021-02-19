'''_6575.py

RollingRingConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets import _1968
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6540
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RollingRingConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionLoadCase',)


class RollingRingConnectionLoadCase(_6540.InterMountableComponentConnectionLoadCase):
    '''RollingRingConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
