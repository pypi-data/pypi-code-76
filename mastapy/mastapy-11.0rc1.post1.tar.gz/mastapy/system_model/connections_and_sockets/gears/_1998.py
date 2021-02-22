'''_1998.py

KlingelnbergSpiralBevelGearTeethSocket
'''


from mastapy.system_model.connections_and_sockets.gears import _1993
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_SPIRAL_BEVEL_GEAR_TEETH_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergSpiralBevelGearTeethSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergSpiralBevelGearTeethSocket',)


class KlingelnbergSpiralBevelGearTeethSocket(_1993.KlingelnbergConicalGearTeethSocket):
    '''KlingelnbergSpiralBevelGearTeethSocket

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_SPIRAL_BEVEL_GEAR_TEETH_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergSpiralBevelGearTeethSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
