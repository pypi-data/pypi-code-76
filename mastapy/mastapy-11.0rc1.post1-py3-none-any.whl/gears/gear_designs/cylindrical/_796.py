'''_796.py

CylindricalPlanetGearDesign
'''


from typing import List

from mastapy.geometry.twod import _111
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears import _139
from mastapy.gears.gear_designs.cylindrical import _819, _818, _775
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalPlanetGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearDesign',)


class CylindricalPlanetGearDesign(_775.CylindricalGearDesign):
    '''CylindricalPlanetGearDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def internal_external(self) -> '_111.InternalExternalType':
        '''InternalExternalType: 'InternalExternal' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.InternalExternal)
        return constructor.new(_111.InternalExternalType)(value) if value else None

    @internal_external.setter
    def internal_external(self, value: '_111.InternalExternalType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InternalExternal = value

    @property
    def has_factorising_sun(self) -> 'bool':
        '''bool: 'HasFactorisingSun' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasFactorisingSun

    @property
    def has_factorising_annulus(self) -> 'bool':
        '''bool: 'HasFactorisingAnnulus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasFactorisingAnnulus

    @property
    def planetary_details(self) -> '_139.PlanetaryDetail':
        '''PlanetaryDetail: 'PlanetaryDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_139.PlanetaryDetail)(self.wrapped.PlanetaryDetails) if self.wrapped.PlanetaryDetails else None

    @property
    def planetary_sidebands_amplitude_factors(self) -> 'List[_819.NamedPlanetSideBandAmplitudeFactor]':
        '''List[NamedPlanetSideBandAmplitudeFactor]: 'PlanetarySidebandsAmplitudeFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetarySidebandsAmplitudeFactors, constructor.new(_819.NamedPlanetSideBandAmplitudeFactor))
        return value

    @property
    def planet_assembly_indices(self) -> 'List[_818.NamedPlanetAssemblyIndex]':
        '''List[NamedPlanetAssemblyIndex]: 'PlanetAssemblyIndices' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetAssemblyIndices, constructor.new(_818.NamedPlanetAssemblyIndex))
        return value
