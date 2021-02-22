'''_546.py

KlingelnbergConicalGearMaterialDatabase
'''


from mastapy.gears.materials import _541, _547
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CONICAL_GEAR_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'KlingelnbergConicalGearMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergConicalGearMaterialDatabase',)


class KlingelnbergConicalGearMaterialDatabase(_541.GearMaterialDatabase['_547.KlingelnbergCycloPalloidConicalGearMaterial']):
    '''KlingelnbergConicalGearMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CONICAL_GEAR_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergConicalGearMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
