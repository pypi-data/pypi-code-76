'''_2077.py

BevelDifferentialGearSet
'''


from typing import List

from mastapy.gears.gear_designs.bevel import _917
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.zerol_bevel import _718
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _727
from mastapy.gears.gear_designs.straight_bevel import _731
from mastapy.gears.gear_designs.spiral_bevel import _735
from mastapy.system_model.part_model.gears import _2080, _2081
from mastapy.system_model.connections_and_sockets.gears import _1883
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSet',)


class BevelDifferentialGearSet(_2081.BevelGearSet):
    '''BevelDifferentialGearSet

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_gear_set_design(self) -> '_917.BevelGearSetDesign':
        '''BevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.BevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_718.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _718.ZerolBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_727.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _727.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_731.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _731.StraightBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_735.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _735.SpiralBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConicalGearSetDesign.__class__)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def bevel_gear_set_design(self) -> '_917.BevelGearSetDesign':
        '''BevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.BevelGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearSetDesign.__class__)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_718.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _718.ZerolBevelGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearSetDesign.__class__)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_727.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _727.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearSetDesign.__class__)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_731.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _731.StraightBevelGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearSetDesign.__class__)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_735.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _735.SpiralBevelGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearSetDesign.__class__)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gears(self) -> 'List[_2080.BevelGear]':
        '''List[BevelGear]: 'BevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelGears, constructor.new(_2080.BevelGear))
        return value

    @property
    def bevel_meshes(self) -> 'List[_1883.BevelGearMesh]':
        '''List[BevelGearMesh]: 'BevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelMeshes, constructor.new(_1883.BevelGearMesh))
        return value
