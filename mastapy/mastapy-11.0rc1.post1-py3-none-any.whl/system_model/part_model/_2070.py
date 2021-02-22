'''_2070.py

PlanetCarrierSettings
'''


from mastapy.utility import _1157
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrierSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierSettings',)


class PlanetCarrierSettings(_1157.PerMachineSettings):
    '''PlanetCarrierSettings

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
