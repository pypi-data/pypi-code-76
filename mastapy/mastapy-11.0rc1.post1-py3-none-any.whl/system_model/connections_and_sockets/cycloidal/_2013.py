'''_2013.py

CycloidalDiscOuterSocket
'''


from mastapy.system_model.connections_and_sockets import _1952
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_OUTER_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscOuterSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscOuterSocket',)


class CycloidalDiscOuterSocket(_1952.CylindricalSocket):
    '''CycloidalDiscOuterSocket

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_OUTER_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscOuterSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
