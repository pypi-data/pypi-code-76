'''_1903.py

OuterShaftSocket
'''


from mastapy.system_model.connections_and_sockets import _1911
from mastapy._internal.python_net import python_net_import

_OUTER_SHAFT_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'OuterShaftSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterShaftSocket',)


class OuterShaftSocket(_1911.ShaftSocket):
    '''OuterShaftSocket

    This is a mastapy class.
    '''

    TYPE = _OUTER_SHAFT_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OuterShaftSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
