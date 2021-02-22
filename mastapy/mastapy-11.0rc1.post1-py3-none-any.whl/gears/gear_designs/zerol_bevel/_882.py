'''_882.py

ZerolBevelGearMeshDesign
'''


from typing import List

from mastapy.gears.gear_designs.zerol_bevel import _883, _881, _884
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.bevel import _1091
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.ZerolBevel', 'ZerolBevelGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshDesign',)


class ZerolBevelGearMeshDesign(_1091.BevelGearMeshDesign):
    '''ZerolBevelGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def zerol_bevel_gear_set(self) -> '_883.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ZerolBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_883.ZerolBevelGearSetDesign)(self.wrapped.ZerolBevelGearSet) if self.wrapped.ZerolBevelGearSet else None

    @property
    def zerol_bevel_gears(self) -> 'List[_881.ZerolBevelGearDesign]':
        '''List[ZerolBevelGearDesign]: 'ZerolBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGears, constructor.new(_881.ZerolBevelGearDesign))
        return value

    @property
    def zerol_bevel_meshed_gears(self) -> 'List[_884.ZerolBevelMeshedGearDesign]':
        '''List[ZerolBevelMeshedGearDesign]: 'ZerolBevelMeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshedGears, constructor.new(_884.ZerolBevelMeshedGearDesign))
        return value
