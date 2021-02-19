'''_1871.py

RollingRingConnection
'''


from mastapy.system_model.connections_and_sockets import _1864
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnection',)


class RollingRingConnection(_1864.InterMountableComponentConnection):
    '''RollingRingConnection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
