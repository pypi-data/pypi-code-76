'''_966.py

CylindricalPlanetaryGearSetDesign
'''


from mastapy._internal import constructor
from mastapy.math_utility import _1275
from mastapy.gears.gear_designs.cylindrical import _955
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANETARY_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalPlanetaryGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetaryGearSetDesign',)


class CylindricalPlanetaryGearSetDesign(_955.CylindricalGearSetDesign):
    '''CylindricalPlanetaryGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANETARY_GEAR_SET_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetaryGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def equally_spaced_planets_are_assemblable(self) -> 'bool':
        '''bool: 'EquallySpacedPlanetsAreAssemblable' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquallySpacedPlanetsAreAssemblable

    @property
    def least_mesh_angle(self) -> 'float':
        '''float: 'LeastMeshAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LeastMeshAngle

    @property
    def planetary_sideband_fourier_series_for_rotating_planet_carrier(self) -> '_1275.FourierSeries':
        '''FourierSeries: 'PlanetarySidebandFourierSeriesForRotatingPlanetCarrier' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1275.FourierSeries)(self.wrapped.PlanetarySidebandFourierSeriesForRotatingPlanetCarrier) if self.wrapped.PlanetarySidebandFourierSeriesForRotatingPlanetCarrier else None
