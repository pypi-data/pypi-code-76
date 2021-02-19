'''_368.py

BevelGearIsoMaterialDatabase
'''


from mastapy.gears.materials import _366, _367
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_ISO_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'BevelGearIsoMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearIsoMaterialDatabase',)


class BevelGearIsoMaterialDatabase(_366.BevelGearAbstractMaterialDatabase['_367.BevelGearISOMaterial']):
    '''BevelGearIsoMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_ISO_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearIsoMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
