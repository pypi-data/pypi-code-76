'''_738.py

SpiralBevelMeshedGearDesign
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.bevel import _920
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.SpiralBevel', 'SpiralBevelMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelMeshedGearDesign',)


class SpiralBevelMeshedGearDesign(_920.BevelMeshedGearDesign):
    '''SpiralBevelMeshedGearDesign

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_MESHED_GEAR_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def tip_thickness_at_mean_section(self) -> 'float':
        '''float: 'TipThicknessAtMeanSection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipThicknessAtMeanSection
