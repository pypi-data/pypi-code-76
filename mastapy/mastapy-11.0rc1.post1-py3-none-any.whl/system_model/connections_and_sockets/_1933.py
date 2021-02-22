'''_1933.py

InnerShaftConnectingSocket
'''


from mastapy.system_model.connections_and_sockets import _1934
from mastapy._internal.python_net import python_net_import

_INNER_SHAFT_CONNECTING_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InnerShaftConnectingSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('InnerShaftConnectingSocket',)


class InnerShaftConnectingSocket(_1934.InnerShaftConnectingSocketBase):
    '''InnerShaftConnectingSocket

    This is a mastapy class.
    '''

    TYPE = _INNER_SHAFT_CONNECTING_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InnerShaftConnectingSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
