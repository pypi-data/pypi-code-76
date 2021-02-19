'''_1905.py

BevelGearTeethSocket
'''


from mastapy.system_model.connections_and_sockets.gears import _1901
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_TEETH_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearTeethSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearTeethSocket',)


class BevelGearTeethSocket(_1901.AGMAGleasonConicalGearTeethSocket):
    '''BevelGearTeethSocket

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_TEETH_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearTeethSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
