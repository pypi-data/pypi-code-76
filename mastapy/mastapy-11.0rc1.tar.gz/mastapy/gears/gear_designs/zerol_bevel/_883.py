'''_883.py

ZerolBevelGearSetDesign
'''


from typing import List

from mastapy.gears import _312
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.zerol_bevel import _881, _882
from mastapy.gears.gear_designs.bevel import _1092
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.ZerolBevel', 'ZerolBevelGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetDesign',)


class ZerolBevelGearSetDesign(_1092.BevelGearSetDesign):
    '''ZerolBevelGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def tooth_taper_zerol(self) -> '_312.ZerolBevelGleasonToothTaperOption':
        '''ZerolBevelGleasonToothTaperOption: 'ToothTaperZerol' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ToothTaperZerol)
        return constructor.new(_312.ZerolBevelGleasonToothTaperOption)(value) if value else None

    @tooth_taper_zerol.setter
    def tooth_taper_zerol(self, value: '_312.ZerolBevelGleasonToothTaperOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToothTaperZerol = value

    @property
    def minimum_number_of_teeth_for_recommended_tooth_proportions(self) -> 'int':
        '''int: 'MinimumNumberOfTeethForRecommendedToothProportions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumNumberOfTeethForRecommendedToothProportions

    @property
    def gears(self) -> 'List[_881.ZerolBevelGearDesign]':
        '''List[ZerolBevelGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_881.ZerolBevelGearDesign))
        return value

    @property
    def zerol_bevel_gears(self) -> 'List[_881.ZerolBevelGearDesign]':
        '''List[ZerolBevelGearDesign]: 'ZerolBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGears, constructor.new(_881.ZerolBevelGearDesign))
        return value

    @property
    def zerol_bevel_meshes(self) -> 'List[_882.ZerolBevelGearMeshDesign]':
        '''List[ZerolBevelGearMeshDesign]: 'ZerolBevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshes, constructor.new(_882.ZerolBevelGearMeshDesign))
        return value
