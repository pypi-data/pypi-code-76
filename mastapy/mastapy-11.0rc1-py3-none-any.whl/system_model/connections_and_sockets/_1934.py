'''_1934.py

InnerShaftConnectingSocketBase
'''


from mastapy.system_model.connections_and_sockets import _1947
from mastapy._internal.python_net import python_net_import

_INNER_SHAFT_CONNECTING_SOCKET_BASE = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InnerShaftConnectingSocketBase')


__docformat__ = 'restructuredtext en'
__all__ = ('InnerShaftConnectingSocketBase',)


class InnerShaftConnectingSocketBase(_1947.ShaftConnectingSocket):
    '''InnerShaftConnectingSocketBase

    This is a mastapy class.
    '''

    TYPE = _INNER_SHAFT_CONNECTING_SOCKET_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InnerShaftConnectingSocketBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
