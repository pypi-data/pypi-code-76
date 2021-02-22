'''_1936.py

InnerShaftSocketBase
'''


from mastapy.system_model.connections_and_sockets import _1948
from mastapy._internal.python_net import python_net_import

_INNER_SHAFT_SOCKET_BASE = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InnerShaftSocketBase')


__docformat__ = 'restructuredtext en'
__all__ = ('InnerShaftSocketBase',)


class InnerShaftSocketBase(_1948.ShaftSocket):
    '''InnerShaftSocketBase

    This is a mastapy class.
    '''

    TYPE = _INNER_SHAFT_SOCKET_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InnerShaftSocketBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
