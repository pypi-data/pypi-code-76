'''_1992.py

RingPinsSocket
'''


from mastapy.system_model.connections_and_sockets import _1930
from mastapy._internal.python_net import python_net_import

_RING_PINS_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsSocket',)


class RingPinsSocket(_1930.CylindricalSocket):
    '''RingPinsSocket

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
