'''_1902.py

OuterShaftConnectingSocket
'''


from mastapy.system_model.connections_and_sockets import _1910
from mastapy._internal.python_net import python_net_import

_OUTER_SHAFT_CONNECTING_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'OuterShaftConnectingSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterShaftConnectingSocket',)


class OuterShaftConnectingSocket(_1910.ShaftConnectingSocket):
    '''OuterShaftConnectingSocket

    This is a mastapy class.
    '''

    TYPE = _OUTER_SHAFT_CONNECTING_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OuterShaftConnectingSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
