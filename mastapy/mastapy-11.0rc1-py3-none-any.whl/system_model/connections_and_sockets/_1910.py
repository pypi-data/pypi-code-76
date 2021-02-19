'''_1910.py

ShaftConnectingSocket
'''


from mastapy.system_model.connections_and_sockets import _1896
from mastapy._internal.python_net import python_net_import

_SHAFT_CONNECTING_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftConnectingSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftConnectingSocket',)


class ShaftConnectingSocket(_1896.CylindricalSocket):
    '''ShaftConnectingSocket

    This is a mastapy class.
    '''

    TYPE = _SHAFT_CONNECTING_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftConnectingSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
