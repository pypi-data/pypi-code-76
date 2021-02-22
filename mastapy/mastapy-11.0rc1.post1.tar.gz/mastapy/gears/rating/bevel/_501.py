'''_501.py

BevelGearMeshRating
'''


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.bevel.standards import _507, _505
from mastapy.gears.rating.iso_10300 import _385, _383
from mastapy.gears.rating.conical import _492
from mastapy.gears.rating.agma_gleason_conical import _512
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Bevel', 'BevelGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMeshRating',)


class BevelGearMeshRating(_512.AGMAGleasonConicalGearMeshRating):
    '''BevelGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def size_factor_bending(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorBending) if self.wrapped.SizeFactorBending else None

    @property
    def size_factor_contact(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SizeFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SizeFactorContact) if self.wrapped.SizeFactorContact else None

    @property
    def gleason_bevel_mesh_single_flank_rating(self) -> '_507.GleasonSpiralBevelMeshSingleFlankRating':
        '''GleasonSpiralBevelMeshSingleFlankRating: 'GleasonBevelMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_507.GleasonSpiralBevelMeshSingleFlankRating)(self.wrapped.GleasonBevelMeshSingleFlankRating) if self.wrapped.GleasonBevelMeshSingleFlankRating else None

    @property
    def agma_bevel_mesh_single_flank_rating(self) -> '_505.AGMASpiralBevelMeshSingleFlankRating':
        '''AGMASpiralBevelMeshSingleFlankRating: 'AGMABevelMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_505.AGMASpiralBevelMeshSingleFlankRating)(self.wrapped.AGMABevelMeshSingleFlankRating) if self.wrapped.AGMABevelMeshSingleFlankRating else None

    @property
    def iso10300_bevel_mesh_single_flank_rating_method_b1(self) -> '_385.ISO10300MeshSingleFlankRatingMethodB1':
        '''ISO10300MeshSingleFlankRatingMethodB1: 'ISO10300BevelMeshSingleFlankRatingMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_385.ISO10300MeshSingleFlankRatingMethodB1)(self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB1) if self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB1 else None

    @property
    def iso10300_bevel_mesh_single_flank_rating_method_b2(self) -> '_383.Iso10300MeshSingleFlankRatingBevelMethodB2':
        '''Iso10300MeshSingleFlankRatingBevelMethodB2: 'ISO10300BevelMeshSingleFlankRatingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_383.Iso10300MeshSingleFlankRatingBevelMethodB2)(self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB2) if self.wrapped.ISO10300BevelMeshSingleFlankRatingMethodB2 else None

    @property
    def meshed_gears(self) -> 'List[_492.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_492.ConicalMeshedGearRating))
        return value

    @property
    def gears_in_mesh(self) -> 'List[_492.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'GearsInMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsInMesh, constructor.new(_492.ConicalMeshedGearRating))
        return value
