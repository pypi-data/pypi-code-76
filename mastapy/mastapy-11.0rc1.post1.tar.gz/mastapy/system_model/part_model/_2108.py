'''_2108.py

Assembly
'''


from typing import List, TypeVar, Optional

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2138, _2118, _2114, _2117,
    _2126, _2145, _2144, _2139,
    _2141, _2109, _2110, _2111,
    _2116, _2121, _2122, _2125,
    _2127, _2128, _2135, _2136,
    _2137, _2142, _2147, _2149,
    _2150, _2151
)
from mastapy.system_model.part_model.gears import (
    _2219, _2206, _2215, _2203,
    _2197, _2195, _2223, _2208,
    _2184, _2185, _2186, _2187,
    _2188, _2189, _2190, _2191,
    _2192, _2193, _2194, _2196,
    _2198, _2199, _2200, _2201,
    _2205, _2207, _2209, _2210,
    _2211, _2212, _2213, _2214,
    _2216, _2217, _2218, _2220,
    _2221, _2222, _2224, _2225
)
from mastapy.system_model.part_model.couplings import (
    _2269, _2247, _2249, _2250,
    _2252, _2253, _2254, _2255,
    _2257, _2258, _2259, _2260,
    _2261, _2267, _2268, _2271,
    _2272, _2273, _2275, _2276,
    _2277, _2278, _2279, _2281
)
from mastapy.system_model.part_model.shaft_model import _2154
from mastapy.system_model.part_model.cycloidal import _2239, _2240, _2241
from mastapy.gears import _293
from mastapy._internal.python_net import python_net_import
from mastapy.gears.gear_designs.creation_options import _1059, _1056
from mastapy.gears.gear_designs.bevel import _1089
from mastapy.system_model.part_model.creation_options import (
    _2243, _2242, _2245, _2246,
    _2244
)
from mastapy.bearings import _1576, _1601
from mastapy.nodal_analysis import _71

_ARRAY = python_net_import('System', 'Array')
_STRING = python_net_import('System', 'String')
_DOUBLE = python_net_import('System', 'Double')
_INT_32 = python_net_import('System', 'Int32')
_HAND = python_net_import('SMT.MastaAPI.Gears', 'Hand')
_CYLINDRICAL_GEAR_LINEAR_TRAIN_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'CylindricalGearLinearTrainCreationOptions')
_CYCLOIDAL_ASSEMBLY_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'CycloidalAssemblyCreationOptions')
_BELT_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'BeltCreationOptions')
_PLANET_CARRIER_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'PlanetCarrierCreationOptions')
_SHAFT_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'ShaftCreationOptions')
_SPIRAL_BEVEL_GEAR_SET_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.CreationOptions', 'SpiralBevelGearSetCreationOptions')
_CYLINDRICAL_GEAR_PAIR_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.CreationOptions', 'CylindricalGearPairCreationOptions')
_AGMA_GLEASON_CONICAL_GEAR_GEOMETRY_METHODS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'AGMAGleasonConicalGearGeometryMethods')
_ROLLING_BEARING_TYPE = python_net_import('SMT.MastaAPI.Bearings', 'RollingBearingType')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')


__docformat__ = 'restructuredtext en'
__all__ = ('Assembly',)


class Assembly(_2109.AbstractAssembly):
    '''Assembly

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Assembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_width_of_widest_cylindrical_gear(self) -> 'float':
        '''float: 'FaceWidthOfWidestCylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceWidthOfWidestCylindricalGear

    @property
    def mass_of_gears(self) -> 'float':
        '''float: 'MassOfGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfGears

    @property
    def mass_of_bearings(self) -> 'float':
        '''float: 'MassOfBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfBearings

    @property
    def mass_of_shafts(self) -> 'float':
        '''float: 'MassOfShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfShafts

    @property
    def mass_of_fe_part_shafts(self) -> 'float':
        '''float: 'MassOfFEPartShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfFEPartShafts

    @property
    def mass_of_fe_part_housings(self) -> 'float':
        '''float: 'MassOfFEPartHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfFEPartHousings

    @property
    def mass_of_other_parts(self) -> 'float':
        '''float: 'MassOfOtherParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfOtherParts

    @property
    def smallest_number_of_teeth(self) -> 'int':
        '''int: 'SmallestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestNumberOfTeeth

    @property
    def largest_number_of_teeth(self) -> 'int':
        '''int: 'LargestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LargestNumberOfTeeth

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseAndAxialContactRatioRatingForNVH

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatioRatingForNVH

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialContactRatioRatingForNVH

    @property
    def minimum_tip_thickness(self) -> 'float':
        '''float: 'MinimumTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTipThickness

    @property
    def oil_level_specification(self) -> '_2138.OilLevelSpecification':
        '''OilLevelSpecification: 'OilLevelSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.OilLevelSpecification)(self.wrapped.OilLevelSpecification) if self.wrapped.OilLevelSpecification else None

    @property
    def components_with_unknown_scalar_mass(self) -> 'List[_2118.Component]':
        '''List[Component]: 'ComponentsWithUnknownScalarMass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentsWithUnknownScalarMass, constructor.new(_2118.Component))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2219.StraightBevelGearSet]':
        '''List[StraightBevelGearSet]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2219.StraightBevelGearSet))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2206.HypoidGearSet]':
        '''List[HypoidGearSet]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2206.HypoidGearSet))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2215.SpiralBevelGearSet]':
        '''List[SpiralBevelGearSet]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2215.SpiralBevelGearSet))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2269.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2269.ShaftHubConnection))
        return value

    @property
    def gear_sets(self) -> 'List[_2203.GearSet]':
        '''List[GearSet]: 'GearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSets, constructor.new(_2203.GearSet))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2197.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2197.CylindricalGearSet))
        return value

    @property
    def conical_gear_sets(self) -> 'List[_2195.ConicalGearSet]':
        '''List[ConicalGearSet]: 'ConicalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGearSets, constructor.new(_2195.ConicalGearSet))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2223.WormGearSet]':
        '''List[WormGearSet]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2223.WormGearSet))
        return value

    @property
    def klingelnberg_cyclo_palloid_gear_sets(self) -> 'List[_2208.KlingelnbergCycloPalloidConicalGearSet]':
        '''List[KlingelnbergCycloPalloidConicalGearSet]: 'KlingelnbergCycloPalloidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidGearSets, constructor.new(_2208.KlingelnbergCycloPalloidConicalGearSet))
        return value

    @property
    def shafts(self) -> 'List[_2154.Shaft]':
        '''List[Shaft]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2154.Shaft))
        return value

    @property
    def bearings(self) -> 'List[_2114.Bearing]':
        '''List[Bearing]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2114.Bearing))
        return value

    @property
    def bolted_joints(self) -> 'List[_2117.BoltedJoint]':
        '''List[BoltedJoint]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2117.BoltedJoint))
        return value

    @property
    def fe_parts(self) -> 'List[_2126.FEPart]':
        '''List[FEPart]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_2126.FEPart))
        return value

    @property
    def component_details(self) -> 'List[_2118.Component]':
        '''List[Component]: 'ComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDetails, constructor.new(_2118.Component))
        return value

    @property
    def power_loads(self) -> 'List[_2145.PowerLoad]':
        '''List[PowerLoad]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2145.PowerLoad))
        return value

    @property
    def point_loads(self) -> 'List[_2144.PointLoad]':
        '''List[PointLoad]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2144.PointLoad))
        return value

    @property
    def oil_seals(self) -> 'List[_2139.OilSeal]':
        '''List[OilSeal]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2139.OilSeal))
        return value

    def get_part_named(self, name: 'str') -> '_2141.Part':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Part
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2141.Part.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_assembly(self, name: 'str') -> 'Assembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[Assembly.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_abstract_assembly(self, name: 'str') -> '_2109.AbstractAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2109.AbstractAssembly.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_abstract_shaft(self, name: 'str') -> '_2110.AbstractShaft':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractShaft
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2110.AbstractShaft.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_abstract_shaft_or_housing(self, name: 'str') -> '_2111.AbstractShaftOrHousing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractShaftOrHousing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2111.AbstractShaftOrHousing.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bearing(self, name: 'str') -> '_2114.Bearing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2114.Bearing.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bolt(self, name: 'str') -> '_2116.Bolt':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bolt
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2116.Bolt.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bolted_joint(self, name: 'str') -> '_2117.BoltedJoint':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2117.BoltedJoint.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_component(self, name: 'str') -> '_2118.Component':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2118.Component.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_connector(self, name: 'str') -> '_2121.Connector':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Connector
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2121.Connector.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_datum(self, name: 'str') -> '_2122.Datum':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2122.Datum.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_external_cad_model(self, name: 'str') -> '_2125.ExternalCADModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.ExternalCADModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2125.ExternalCADModel.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_fe_part(self, name: 'str') -> '_2126.FEPart':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.FEPart
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2126.FEPart.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_flexible_pin_assembly(self, name: 'str') -> '_2127.FlexiblePinAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.FlexiblePinAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2127.FlexiblePinAssembly.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_guide_dxf_model(self, name: 'str') -> '_2128.GuideDxfModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.GuideDxfModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2128.GuideDxfModel.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_mass_disc(self, name: 'str') -> '_2135.MassDisc':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2135.MassDisc.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_measurement_component(self, name: 'str') -> '_2136.MeasurementComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2136.MeasurementComponent.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_mountable_component(self, name: 'str') -> '_2137.MountableComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MountableComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2137.MountableComponent.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_oil_seal(self, name: 'str') -> '_2139.OilSeal':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2139.OilSeal.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_planet_carrier(self, name: 'str') -> '_2142.PlanetCarrier':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2142.PlanetCarrier.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_point_load(self, name: 'str') -> '_2144.PointLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2144.PointLoad.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_power_load(self, name: 'str') -> '_2145.PowerLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2145.PowerLoad.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_root_assembly(self, name: 'str') -> '_2147.RootAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.RootAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2147.RootAssembly.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_specialised_assembly(self, name: 'str') -> '_2149.SpecialisedAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.SpecialisedAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2149.SpecialisedAssembly.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_unbalanced_mass(self, name: 'str') -> '_2150.UnbalancedMass':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2150.UnbalancedMass.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_virtual_component(self, name: 'str') -> '_2151.VirtualComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.VirtualComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2151.VirtualComponent.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_shaft(self, name: 'str') -> '_2154.Shaft':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2154.Shaft.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear(self, name: 'str') -> '_2184.AGMAGleasonConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2184.AGMAGleasonConicalGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear_set(self, name: 'str') -> '_2185.AGMAGleasonConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2185.AGMAGleasonConicalGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear(self, name: 'str') -> '_2186.BevelDifferentialGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2186.BevelDifferentialGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear_set(self, name: 'str') -> '_2187.BevelDifferentialGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2187.BevelDifferentialGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_planet_gear(self, name: 'str') -> '_2188.BevelDifferentialPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2188.BevelDifferentialPlanetGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_sun_gear(self, name: 'str') -> '_2189.BevelDifferentialSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2189.BevelDifferentialSunGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear(self, name: 'str') -> '_2190.BevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2190.BevelGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear_set(self, name: 'str') -> '_2191.BevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2191.BevelGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear(self, name: 'str') -> '_2192.ConceptGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2192.ConceptGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear_set(self, name: 'str') -> '_2193.ConceptGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2193.ConceptGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear(self, name: 'str') -> '_2194.ConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2194.ConicalGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear_set(self, name: 'str') -> '_2195.ConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2195.ConicalGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear(self, name: 'str') -> '_2196.CylindricalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2196.CylindricalGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear_set(self, name: 'str') -> '_2197.CylindricalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2197.CylindricalGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_planet_gear(self, name: 'str') -> '_2198.CylindricalPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2198.CylindricalPlanetGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_face_gear(self, name: 'str') -> '_2199.FaceGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2199.FaceGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_face_gear_set(self, name: 'str') -> '_2200.FaceGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2200.FaceGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_gear(self, name: 'str') -> '_2201.Gear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.Gear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2201.Gear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_gear_set(self, name: 'str') -> '_2203.GearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.GearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2203.GearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear(self, name: 'str') -> '_2205.HypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2205.HypoidGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear_set(self, name: 'str') -> '_2206.HypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2206.HypoidGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear(self, name: 'str') -> '_2207.KlingelnbergCycloPalloidConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2207.KlingelnbergCycloPalloidConicalGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, name: 'str') -> '_2208.KlingelnbergCycloPalloidConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2208.KlingelnbergCycloPalloidConicalGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, name: 'str') -> '_2209.KlingelnbergCycloPalloidHypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2209.KlingelnbergCycloPalloidHypoidGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: 'str') -> '_2210.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2210.KlingelnbergCycloPalloidHypoidGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, name: 'str') -> '_2211.KlingelnbergCycloPalloidSpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2211.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: 'str') -> '_2212.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2212.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_planetary_gear_set(self, name: 'str') -> '_2213.PlanetaryGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2213.PlanetaryGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear(self, name: 'str') -> '_2214.SpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2214.SpiralBevelGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear_set(self, name: 'str') -> '_2215.SpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2215.SpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear(self, name: 'str') -> '_2216.StraightBevelDiffGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2216.StraightBevelDiffGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear_set(self, name: 'str') -> '_2217.StraightBevelDiffGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2217.StraightBevelDiffGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear(self, name: 'str') -> '_2218.StraightBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2218.StraightBevelGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear_set(self, name: 'str') -> '_2219.StraightBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2219.StraightBevelGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_planet_gear(self, name: 'str') -> '_2220.StraightBevelPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2220.StraightBevelPlanetGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_sun_gear(self, name: 'str') -> '_2221.StraightBevelSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2221.StraightBevelSunGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear(self, name: 'str') -> '_2222.WormGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2222.WormGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear_set(self, name: 'str') -> '_2223.WormGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2223.WormGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear(self, name: 'str') -> '_2224.ZerolBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2224.ZerolBevelGear.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear_set(self, name: 'str') -> '_2225.ZerolBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2225.ZerolBevelGearSet.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_cycloidal_assembly(self, name: 'str') -> '_2239.CycloidalAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.cycloidal.CycloidalAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2239.CycloidalAssembly.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_cycloidal_disc(self, name: 'str') -> '_2240.CycloidalDisc':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.cycloidal.CycloidalDisc
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2240.CycloidalDisc.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_ring_pins(self, name: 'str') -> '_2241.RingPins':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.cycloidal.RingPins
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2241.RingPins.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_belt_drive(self, name: 'str') -> '_2247.BeltDrive':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2247.BeltDrive.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_clutch(self, name: 'str') -> '_2249.Clutch':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2249.Clutch.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_clutch_half(self, name: 'str') -> '_2250.ClutchHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ClutchHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2250.ClutchHalf.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling(self, name: 'str') -> '_2252.ConceptCoupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2252.ConceptCoupling.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling_half(self, name: 'str') -> '_2253.ConceptCouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2253.ConceptCouplingHalf.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_coupling(self, name: 'str') -> '_2254.Coupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Coupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2254.Coupling.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_coupling_half(self, name: 'str') -> '_2255.CouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2255.CouplingHalf.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_cvt(self, name: 'str') -> '_2257.CVT':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2257.CVT.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_cvt_pulley(self, name: 'str') -> '_2258.CVTPulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVTPulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2258.CVTPulley.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_part_to_part_shear_coupling(self, name: 'str') -> '_2259.PartToPartShearCoupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.PartToPartShearCoupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2259.PartToPartShearCoupling.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_part_to_part_shear_coupling_half(self, name: 'str') -> '_2260.PartToPartShearCouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2260.PartToPartShearCouplingHalf.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_pulley(self, name: 'str') -> '_2261.Pulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Pulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2261.Pulley.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring(self, name: 'str') -> '_2267.RollingRing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2267.RollingRing.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring_assembly(self, name: 'str') -> '_2268.RollingRingAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRingAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2268.RollingRingAssembly.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_shaft_hub_connection(self, name: 'str') -> '_2269.ShaftHubConnection':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2269.ShaftHubConnection.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper(self, name: 'str') -> '_2271.SpringDamper':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2271.SpringDamper.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper_half(self, name: 'str') -> '_2272.SpringDamperHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamperHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2272.SpringDamperHalf.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser(self, name: 'str') -> '_2273.Synchroniser':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2273.Synchroniser.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_half(self, name: 'str') -> '_2275.SynchroniserHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2275.SynchroniserHalf.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_part(self, name: 'str') -> '_2276.SynchroniserPart':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserPart
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2276.SynchroniserPart.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_sleeve(self, name: 'str') -> '_2277.SynchroniserSleeve':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserSleeve
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2277.SynchroniserSleeve.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter(self, name: 'str') -> '_2278.TorqueConverter':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2278.TorqueConverter.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_pump(self, name: 'str') -> '_2279.TorqueConverterPump':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterPump
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2279.TorqueConverterPump.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_turbine(self, name: 'str') -> '_2281.TorqueConverterTurbine':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterTurbine
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2281.TorqueConverterTurbine.TYPE](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_part(self, part_type: 'Assembly.PartType', name: 'str') -> '_2141.Part':
        ''' 'AddPart' is the original name of this method.

        Args:
            part_type (mastapy.system_model.part_model.Assembly.PartType)
            name (str)

        Returns:
            mastapy.system_model.part_model.Part
        '''

        part_type = conversion.mp_to_pn_enum(part_type)
        name = str(name)
        method_result = self.wrapped.AddPart(part_type, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def all_parts(self) -> 'List[_2141.Part]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Part]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2141.Part.TYPE](), constructor.new(_2141.Part))

    def all_parts_of_type_assembly(self) -> 'List[Assembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Assembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[Assembly.TYPE](), constructor.new(Assembly))

    def all_parts_of_type_abstract_assembly(self) -> 'List[_2109.AbstractAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2109.AbstractAssembly.TYPE](), constructor.new(_2109.AbstractAssembly))

    def all_parts_of_type_abstract_shaft(self) -> 'List[_2110.AbstractShaft]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractShaft]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2110.AbstractShaft.TYPE](), constructor.new(_2110.AbstractShaft))

    def all_parts_of_type_abstract_shaft_or_housing(self) -> 'List[_2111.AbstractShaftOrHousing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractShaftOrHousing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2111.AbstractShaftOrHousing.TYPE](), constructor.new(_2111.AbstractShaftOrHousing))

    def all_parts_of_type_bearing(self) -> 'List[_2114.Bearing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bearing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2114.Bearing.TYPE](), constructor.new(_2114.Bearing))

    def all_parts_of_type_bolt(self) -> 'List[_2116.Bolt]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bolt]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2116.Bolt.TYPE](), constructor.new(_2116.Bolt))

    def all_parts_of_type_bolted_joint(self) -> 'List[_2117.BoltedJoint]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.BoltedJoint]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2117.BoltedJoint.TYPE](), constructor.new(_2117.BoltedJoint))

    def all_parts_of_type_component(self) -> 'List[_2118.Component]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Component]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2118.Component.TYPE](), constructor.new(_2118.Component))

    def all_parts_of_type_connector(self) -> 'List[_2121.Connector]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Connector]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2121.Connector.TYPE](), constructor.new(_2121.Connector))

    def all_parts_of_type_datum(self) -> 'List[_2122.Datum]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Datum]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2122.Datum.TYPE](), constructor.new(_2122.Datum))

    def all_parts_of_type_external_cad_model(self) -> 'List[_2125.ExternalCADModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ExternalCADModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2125.ExternalCADModel.TYPE](), constructor.new(_2125.ExternalCADModel))

    def all_parts_of_type_fe_part(self) -> 'List[_2126.FEPart]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.FEPart]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2126.FEPart.TYPE](), constructor.new(_2126.FEPart))

    def all_parts_of_type_flexible_pin_assembly(self) -> 'List[_2127.FlexiblePinAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.FlexiblePinAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2127.FlexiblePinAssembly.TYPE](), constructor.new(_2127.FlexiblePinAssembly))

    def all_parts_of_type_guide_dxf_model(self) -> 'List[_2128.GuideDxfModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.GuideDxfModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2128.GuideDxfModel.TYPE](), constructor.new(_2128.GuideDxfModel))

    def all_parts_of_type_mass_disc(self) -> 'List[_2135.MassDisc]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MassDisc]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2135.MassDisc.TYPE](), constructor.new(_2135.MassDisc))

    def all_parts_of_type_measurement_component(self) -> 'List[_2136.MeasurementComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MeasurementComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2136.MeasurementComponent.TYPE](), constructor.new(_2136.MeasurementComponent))

    def all_parts_of_type_mountable_component(self) -> 'List[_2137.MountableComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MountableComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2137.MountableComponent.TYPE](), constructor.new(_2137.MountableComponent))

    def all_parts_of_type_oil_seal(self) -> 'List[_2139.OilSeal]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.OilSeal]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2139.OilSeal.TYPE](), constructor.new(_2139.OilSeal))

    def all_parts_of_type_planet_carrier(self) -> 'List[_2142.PlanetCarrier]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PlanetCarrier]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2142.PlanetCarrier.TYPE](), constructor.new(_2142.PlanetCarrier))

    def all_parts_of_type_point_load(self) -> 'List[_2144.PointLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PointLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2144.PointLoad.TYPE](), constructor.new(_2144.PointLoad))

    def all_parts_of_type_power_load(self) -> 'List[_2145.PowerLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PowerLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2145.PowerLoad.TYPE](), constructor.new(_2145.PowerLoad))

    def all_parts_of_type_root_assembly(self) -> 'List[_2147.RootAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.RootAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2147.RootAssembly.TYPE](), constructor.new(_2147.RootAssembly))

    def all_parts_of_type_specialised_assembly(self) -> 'List[_2149.SpecialisedAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.SpecialisedAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2149.SpecialisedAssembly.TYPE](), constructor.new(_2149.SpecialisedAssembly))

    def all_parts_of_type_unbalanced_mass(self) -> 'List[_2150.UnbalancedMass]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.UnbalancedMass]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2150.UnbalancedMass.TYPE](), constructor.new(_2150.UnbalancedMass))

    def all_parts_of_type_virtual_component(self) -> 'List[_2151.VirtualComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.VirtualComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2151.VirtualComponent.TYPE](), constructor.new(_2151.VirtualComponent))

    def all_parts_of_type_shaft(self) -> 'List[_2154.Shaft]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.shaft_model.Shaft]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2154.Shaft.TYPE](), constructor.new(_2154.Shaft))

    def all_parts_of_type_agma_gleason_conical_gear(self) -> 'List[_2184.AGMAGleasonConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2184.AGMAGleasonConicalGear.TYPE](), constructor.new(_2184.AGMAGleasonConicalGear))

    def all_parts_of_type_agma_gleason_conical_gear_set(self) -> 'List[_2185.AGMAGleasonConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2185.AGMAGleasonConicalGearSet.TYPE](), constructor.new(_2185.AGMAGleasonConicalGearSet))

    def all_parts_of_type_bevel_differential_gear(self) -> 'List[_2186.BevelDifferentialGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2186.BevelDifferentialGear.TYPE](), constructor.new(_2186.BevelDifferentialGear))

    def all_parts_of_type_bevel_differential_gear_set(self) -> 'List[_2187.BevelDifferentialGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2187.BevelDifferentialGearSet.TYPE](), constructor.new(_2187.BevelDifferentialGearSet))

    def all_parts_of_type_bevel_differential_planet_gear(self) -> 'List[_2188.BevelDifferentialPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2188.BevelDifferentialPlanetGear.TYPE](), constructor.new(_2188.BevelDifferentialPlanetGear))

    def all_parts_of_type_bevel_differential_sun_gear(self) -> 'List[_2189.BevelDifferentialSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2189.BevelDifferentialSunGear.TYPE](), constructor.new(_2189.BevelDifferentialSunGear))

    def all_parts_of_type_bevel_gear(self) -> 'List[_2190.BevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2190.BevelGear.TYPE](), constructor.new(_2190.BevelGear))

    def all_parts_of_type_bevel_gear_set(self) -> 'List[_2191.BevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2191.BevelGearSet.TYPE](), constructor.new(_2191.BevelGearSet))

    def all_parts_of_type_concept_gear(self) -> 'List[_2192.ConceptGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2192.ConceptGear.TYPE](), constructor.new(_2192.ConceptGear))

    def all_parts_of_type_concept_gear_set(self) -> 'List[_2193.ConceptGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2193.ConceptGearSet.TYPE](), constructor.new(_2193.ConceptGearSet))

    def all_parts_of_type_conical_gear(self) -> 'List[_2194.ConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2194.ConicalGear.TYPE](), constructor.new(_2194.ConicalGear))

    def all_parts_of_type_conical_gear_set(self) -> 'List[_2195.ConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2195.ConicalGearSet.TYPE](), constructor.new(_2195.ConicalGearSet))

    def all_parts_of_type_cylindrical_gear(self) -> 'List[_2196.CylindricalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2196.CylindricalGear.TYPE](), constructor.new(_2196.CylindricalGear))

    def all_parts_of_type_cylindrical_gear_set(self) -> 'List[_2197.CylindricalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2197.CylindricalGearSet.TYPE](), constructor.new(_2197.CylindricalGearSet))

    def all_parts_of_type_cylindrical_planet_gear(self) -> 'List[_2198.CylindricalPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2198.CylindricalPlanetGear.TYPE](), constructor.new(_2198.CylindricalPlanetGear))

    def all_parts_of_type_face_gear(self) -> 'List[_2199.FaceGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2199.FaceGear.TYPE](), constructor.new(_2199.FaceGear))

    def all_parts_of_type_face_gear_set(self) -> 'List[_2200.FaceGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2200.FaceGearSet.TYPE](), constructor.new(_2200.FaceGearSet))

    def all_parts_of_type_gear(self) -> 'List[_2201.Gear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.Gear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2201.Gear.TYPE](), constructor.new(_2201.Gear))

    def all_parts_of_type_gear_set(self) -> 'List[_2203.GearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.GearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2203.GearSet.TYPE](), constructor.new(_2203.GearSet))

    def all_parts_of_type_hypoid_gear(self) -> 'List[_2205.HypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2205.HypoidGear.TYPE](), constructor.new(_2205.HypoidGear))

    def all_parts_of_type_hypoid_gear_set(self) -> 'List[_2206.HypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2206.HypoidGearSet.TYPE](), constructor.new(_2206.HypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> 'List[_2207.KlingelnbergCycloPalloidConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2207.KlingelnbergCycloPalloidConicalGear.TYPE](), constructor.new(_2207.KlingelnbergCycloPalloidConicalGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> 'List[_2208.KlingelnbergCycloPalloidConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2208.KlingelnbergCycloPalloidConicalGearSet.TYPE](), constructor.new(_2208.KlingelnbergCycloPalloidConicalGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> 'List[_2209.KlingelnbergCycloPalloidHypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2209.KlingelnbergCycloPalloidHypoidGear.TYPE](), constructor.new(_2209.KlingelnbergCycloPalloidHypoidGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> 'List[_2210.KlingelnbergCycloPalloidHypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2210.KlingelnbergCycloPalloidHypoidGearSet.TYPE](), constructor.new(_2210.KlingelnbergCycloPalloidHypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> 'List[_2211.KlingelnbergCycloPalloidSpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2211.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](), constructor.new(_2211.KlingelnbergCycloPalloidSpiralBevelGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> 'List[_2212.KlingelnbergCycloPalloidSpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2212.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](), constructor.new(_2212.KlingelnbergCycloPalloidSpiralBevelGearSet))

    def all_parts_of_type_planetary_gear_set(self) -> 'List[_2213.PlanetaryGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.PlanetaryGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2213.PlanetaryGearSet.TYPE](), constructor.new(_2213.PlanetaryGearSet))

    def all_parts_of_type_spiral_bevel_gear(self) -> 'List[_2214.SpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2214.SpiralBevelGear.TYPE](), constructor.new(_2214.SpiralBevelGear))

    def all_parts_of_type_spiral_bevel_gear_set(self) -> 'List[_2215.SpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2215.SpiralBevelGearSet.TYPE](), constructor.new(_2215.SpiralBevelGearSet))

    def all_parts_of_type_straight_bevel_diff_gear(self) -> 'List[_2216.StraightBevelDiffGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2216.StraightBevelDiffGear.TYPE](), constructor.new(_2216.StraightBevelDiffGear))

    def all_parts_of_type_straight_bevel_diff_gear_set(self) -> 'List[_2217.StraightBevelDiffGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2217.StraightBevelDiffGearSet.TYPE](), constructor.new(_2217.StraightBevelDiffGearSet))

    def all_parts_of_type_straight_bevel_gear(self) -> 'List[_2218.StraightBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2218.StraightBevelGear.TYPE](), constructor.new(_2218.StraightBevelGear))

    def all_parts_of_type_straight_bevel_gear_set(self) -> 'List[_2219.StraightBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2219.StraightBevelGearSet.TYPE](), constructor.new(_2219.StraightBevelGearSet))

    def all_parts_of_type_straight_bevel_planet_gear(self) -> 'List[_2220.StraightBevelPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2220.StraightBevelPlanetGear.TYPE](), constructor.new(_2220.StraightBevelPlanetGear))

    def all_parts_of_type_straight_bevel_sun_gear(self) -> 'List[_2221.StraightBevelSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2221.StraightBevelSunGear.TYPE](), constructor.new(_2221.StraightBevelSunGear))

    def all_parts_of_type_worm_gear(self) -> 'List[_2222.WormGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2222.WormGear.TYPE](), constructor.new(_2222.WormGear))

    def all_parts_of_type_worm_gear_set(self) -> 'List[_2223.WormGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2223.WormGearSet.TYPE](), constructor.new(_2223.WormGearSet))

    def all_parts_of_type_zerol_bevel_gear(self) -> 'List[_2224.ZerolBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2224.ZerolBevelGear.TYPE](), constructor.new(_2224.ZerolBevelGear))

    def all_parts_of_type_zerol_bevel_gear_set(self) -> 'List[_2225.ZerolBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2225.ZerolBevelGearSet.TYPE](), constructor.new(_2225.ZerolBevelGearSet))

    def all_parts_of_type_cycloidal_assembly(self) -> 'List[_2239.CycloidalAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.cycloidal.CycloidalAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2239.CycloidalAssembly.TYPE](), constructor.new(_2239.CycloidalAssembly))

    def all_parts_of_type_cycloidal_disc(self) -> 'List[_2240.CycloidalDisc]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.cycloidal.CycloidalDisc]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2240.CycloidalDisc.TYPE](), constructor.new(_2240.CycloidalDisc))

    def all_parts_of_type_ring_pins(self) -> 'List[_2241.RingPins]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.cycloidal.RingPins]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2241.RingPins.TYPE](), constructor.new(_2241.RingPins))

    def all_parts_of_type_belt_drive(self) -> 'List[_2247.BeltDrive]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.BeltDrive]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2247.BeltDrive.TYPE](), constructor.new(_2247.BeltDrive))

    def all_parts_of_type_clutch(self) -> 'List[_2249.Clutch]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Clutch]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2249.Clutch.TYPE](), constructor.new(_2249.Clutch))

    def all_parts_of_type_clutch_half(self) -> 'List[_2250.ClutchHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ClutchHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2250.ClutchHalf.TYPE](), constructor.new(_2250.ClutchHalf))

    def all_parts_of_type_concept_coupling(self) -> 'List[_2252.ConceptCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2252.ConceptCoupling.TYPE](), constructor.new(_2252.ConceptCoupling))

    def all_parts_of_type_concept_coupling_half(self) -> 'List[_2253.ConceptCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2253.ConceptCouplingHalf.TYPE](), constructor.new(_2253.ConceptCouplingHalf))

    def all_parts_of_type_coupling(self) -> 'List[_2254.Coupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Coupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2254.Coupling.TYPE](), constructor.new(_2254.Coupling))

    def all_parts_of_type_coupling_half(self) -> 'List[_2255.CouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2255.CouplingHalf.TYPE](), constructor.new(_2255.CouplingHalf))

    def all_parts_of_type_cvt(self) -> 'List[_2257.CVT]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVT]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2257.CVT.TYPE](), constructor.new(_2257.CVT))

    def all_parts_of_type_cvt_pulley(self) -> 'List[_2258.CVTPulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVTPulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2258.CVTPulley.TYPE](), constructor.new(_2258.CVTPulley))

    def all_parts_of_type_part_to_part_shear_coupling(self) -> 'List[_2259.PartToPartShearCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2259.PartToPartShearCoupling.TYPE](), constructor.new(_2259.PartToPartShearCoupling))

    def all_parts_of_type_part_to_part_shear_coupling_half(self) -> 'List[_2260.PartToPartShearCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2260.PartToPartShearCouplingHalf.TYPE](), constructor.new(_2260.PartToPartShearCouplingHalf))

    def all_parts_of_type_pulley(self) -> 'List[_2261.Pulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Pulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2261.Pulley.TYPE](), constructor.new(_2261.Pulley))

    def all_parts_of_type_rolling_ring(self) -> 'List[_2267.RollingRing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2267.RollingRing.TYPE](), constructor.new(_2267.RollingRing))

    def all_parts_of_type_rolling_ring_assembly(self) -> 'List[_2268.RollingRingAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRingAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2268.RollingRingAssembly.TYPE](), constructor.new(_2268.RollingRingAssembly))

    def all_parts_of_type_shaft_hub_connection(self) -> 'List[_2269.ShaftHubConnection]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ShaftHubConnection]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2269.ShaftHubConnection.TYPE](), constructor.new(_2269.ShaftHubConnection))

    def all_parts_of_type_spring_damper(self) -> 'List[_2271.SpringDamper]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamper]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2271.SpringDamper.TYPE](), constructor.new(_2271.SpringDamper))

    def all_parts_of_type_spring_damper_half(self) -> 'List[_2272.SpringDamperHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamperHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2272.SpringDamperHalf.TYPE](), constructor.new(_2272.SpringDamperHalf))

    def all_parts_of_type_synchroniser(self) -> 'List[_2273.Synchroniser]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Synchroniser]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2273.Synchroniser.TYPE](), constructor.new(_2273.Synchroniser))

    def all_parts_of_type_synchroniser_half(self) -> 'List[_2275.SynchroniserHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2275.SynchroniserHalf.TYPE](), constructor.new(_2275.SynchroniserHalf))

    def all_parts_of_type_synchroniser_part(self) -> 'List[_2276.SynchroniserPart]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserPart]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2276.SynchroniserPart.TYPE](), constructor.new(_2276.SynchroniserPart))

    def all_parts_of_type_synchroniser_sleeve(self) -> 'List[_2277.SynchroniserSleeve]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserSleeve]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2277.SynchroniserSleeve.TYPE](), constructor.new(_2277.SynchroniserSleeve))

    def all_parts_of_type_torque_converter(self) -> 'List[_2278.TorqueConverter]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverter]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2278.TorqueConverter.TYPE](), constructor.new(_2278.TorqueConverter))

    def all_parts_of_type_torque_converter_pump(self) -> 'List[_2279.TorqueConverterPump]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterPump]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2279.TorqueConverterPump.TYPE](), constructor.new(_2279.TorqueConverterPump))

    def all_parts_of_type_torque_converter_turbine(self) -> 'List[_2281.TorqueConverterTurbine]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterTurbine]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2281.TorqueConverterTurbine.TYPE](), constructor.new(_2281.TorqueConverterTurbine))

    def add_cylindrical_gear_set_extended(self, name: 'str', normal_pressure_angle: 'float', helix_angle: 'float', normal_module: 'float', pinion_hand: '_293.Hand', centre_distances: 'List[float]') -> '_2197.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            normal_pressure_angle (float)
            helix_angle (float)
            normal_module (float)
            pinion_hand (mastapy.gears.Hand)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        normal_pressure_angle = float(normal_pressure_angle)
        helix_angle = float(helix_angle)
        normal_module = float(normal_module)
        pinion_hand = conversion.mp_to_pn_enum(pinion_hand)
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet.Overloads[_STRING, _DOUBLE, _DOUBLE, _DOUBLE, _HAND, _ARRAY[_DOUBLE]](name if name else None, normal_pressure_angle if normal_pressure_angle else 0.0, helix_angle if helix_angle else 0.0, normal_module if normal_module else 0.0, pinion_hand, centre_distances)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_spiral_bevel_gear_set_with_options(self, spiral_bevel_gear_set_creation_options: Optional['_1059.SpiralBevelGearSetCreationOptions'] = None) -> '_2215.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            spiral_bevel_gear_set_creation_options (mastapy.gears.gear_designs.creation_options.SpiralBevelGearSetCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        method_result = self.wrapped.AddSpiralBevelGearSet.Overloads[_SPIRAL_BEVEL_GEAR_SET_CREATION_OPTIONS](spiral_bevel_gear_set_creation_options.wrapped if spiral_bevel_gear_set_creation_options else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_spiral_bevel_gear_set_detailed(self, name: Optional['str'] = 'Spiral Bevel Gear Set', outer_transverse_module: Optional['float'] = 0.00635, pressure_angle: Optional['float'] = 0.02, mean_spiral_angle: Optional['float'] = 0.523599, wheel_number_of_teeth: Optional['int'] = 43, pinion_number_of_teeth: Optional['int'] = 14, wheel_face_width: Optional['float'] = 0.02, pinion_face_width: Optional['float'] = 0.02, pinion_face_width_offset: Optional['float'] = 0.0, shaft_angle: Optional['float'] = 1.5708) -> '_2215.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)
            outer_transverse_module (float, optional)
            pressure_angle (float, optional)
            mean_spiral_angle (float, optional)
            wheel_number_of_teeth (int, optional)
            pinion_number_of_teeth (int, optional)
            wheel_face_width (float, optional)
            pinion_face_width (float, optional)
            pinion_face_width_offset (float, optional)
            shaft_angle (float, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        outer_transverse_module = float(outer_transverse_module)
        pressure_angle = float(pressure_angle)
        mean_spiral_angle = float(mean_spiral_angle)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_face_width = float(wheel_face_width)
        pinion_face_width = float(pinion_face_width)
        pinion_face_width_offset = float(pinion_face_width_offset)
        shaft_angle = float(shaft_angle)
        method_result = self.wrapped.AddSpiralBevelGearSet.Overloads[_STRING, _DOUBLE, _DOUBLE, _DOUBLE, _INT_32, _INT_32, _DOUBLE, _DOUBLE, _DOUBLE, _DOUBLE](name if name else None, outer_transverse_module if outer_transverse_module else 0.0, pressure_angle if pressure_angle else 0.0, mean_spiral_angle if mean_spiral_angle else 0.0, wheel_number_of_teeth if wheel_number_of_teeth else 0, pinion_number_of_teeth if pinion_number_of_teeth else 0, wheel_face_width if wheel_face_width else 0.0, pinion_face_width if pinion_face_width else 0.0, pinion_face_width_offset if pinion_face_width_offset else 0.0, shaft_angle if shaft_angle else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_hypoid_gear_set_detailed(self, name: Optional['str'] = 'Hypoid Gear Set', pinion_number_of_teeth: Optional['int'] = 7, wheel_number_of_teeth: Optional['int'] = 41, outer_transverse_module: Optional['float'] = 0.0109756, wheel_face_width: Optional['float'] = 0.072, offset: Optional['float'] = 0.045, average_pressure_angle: Optional['float'] = 0.3926991, design_method: Optional['_1089.AGMAGleasonConicalGearGeometryMethods'] = _1089.AGMAGleasonConicalGearGeometryMethods.GLEASON) -> '_2206.HypoidGearSet':
        ''' 'AddHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)
            pinion_number_of_teeth (int, optional)
            wheel_number_of_teeth (int, optional)
            outer_transverse_module (float, optional)
            wheel_face_width (float, optional)
            offset (float, optional)
            average_pressure_angle (float, optional)
            design_method (mastapy.gears.gear_designs.bevel.AGMAGleasonConicalGearGeometryMethods, optional)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        pinion_number_of_teeth = int(pinion_number_of_teeth)
        wheel_number_of_teeth = int(wheel_number_of_teeth)
        outer_transverse_module = float(outer_transverse_module)
        wheel_face_width = float(wheel_face_width)
        offset = float(offset)
        average_pressure_angle = float(average_pressure_angle)
        design_method = conversion.mp_to_pn_enum(design_method)
        method_result = self.wrapped.AddHypoidGearSet.Overloads[_STRING, _INT_32, _INT_32, _DOUBLE, _DOUBLE, _DOUBLE, _DOUBLE, _AGMA_GLEASON_CONICAL_GEAR_GEOMETRY_METHODS](name if name else None, pinion_number_of_teeth if pinion_number_of_teeth else 0, wheel_number_of_teeth if wheel_number_of_teeth else 0, outer_transverse_module if outer_transverse_module else 0.0, wheel_face_width if wheel_face_width else 0.0, offset if offset else 0.0, average_pressure_angle if average_pressure_angle else 0.0, design_method)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_bearing(self, name: 'str') -> '_2114.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.AddBearing.Overloads[_STRING](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_cycloidal_assembly_with_options(self, cycloidal_assembly_creation_options: Optional['_2243.CycloidalAssemblyCreationOptions'] = None) -> '_2239.CycloidalAssembly':
        ''' 'AddCycloidalAssembly' is the original name of this method.

        Args:
            cycloidal_assembly_creation_options (mastapy.system_model.part_model.creation_options.CycloidalAssemblyCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.cycloidal.CycloidalAssembly
        '''

        method_result = self.wrapped.AddCycloidalAssembly.Overloads[_CYCLOIDAL_ASSEMBLY_CREATION_OPTIONS](cycloidal_assembly_creation_options.wrapped if cycloidal_assembly_creation_options else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_cycloidal_assembly(self, number_of_discs: Optional['int'] = 1, number_of_pins: Optional['int'] = 10, name: Optional['str'] = 'Cycloidal Assembly') -> '_2239.CycloidalAssembly':
        ''' 'AddCycloidalAssembly' is the original name of this method.

        Args:
            number_of_discs (int, optional)
            number_of_pins (int, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.cycloidal.CycloidalAssembly
        '''

        number_of_discs = int(number_of_discs)
        number_of_pins = int(number_of_pins)
        name = str(name)
        method_result = self.wrapped.AddCycloidalAssembly.Overloads[_INT_32, _INT_32, _STRING](number_of_discs if number_of_discs else 0, number_of_pins if number_of_pins else 0, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_axial_clearance_bearing(self, name: 'str', contact_diameter: 'float') -> '_2114.Bearing':
        ''' 'AddAxialClearanceBearing' is the original name of this method.

        Args:
            name (str)
            contact_diameter (float)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        contact_diameter = float(contact_diameter)
        method_result = self.wrapped.AddAxialClearanceBearing(name if name else None, contact_diameter if contact_diameter else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_shaft_hub_connection(self, name: 'str') -> '_2269.ShaftHubConnection':
        ''' 'AddShaftHubConnection' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.AddShaftHubConnection(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_rolling_bearing_from_catalogue(self, catalogue: '_1576.BearingCatalog', designation: 'str', name: 'str') -> '_2114.Bearing':
        ''' 'AddRollingBearingFromCatalogue' is the original name of this method.

        Args:
            catalogue (mastapy.bearings.BearingCatalog)
            designation (str)
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        catalogue = conversion.mp_to_pn_enum(catalogue)
        designation = str(designation)
        name = str(name)
        method_result = self.wrapped.AddRollingBearingFromCatalogue(catalogue, designation if designation else None, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_bearing_with_name_and_rolling_bearing_type(self, name: 'str', type_: '_1601.RollingBearingType') -> '_2114.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        method_result = self.wrapped.AddBearing.Overloads[_STRING, _ROLLING_BEARING_TYPE](name if name else None, type_)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_bearing_with_name_rolling_bearing_type_and_designation(self, name: 'str', type_: '_1601.RollingBearingType', designation: 'str') -> '_2114.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)
            designation (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        designation = str(designation)
        method_result = self.wrapped.AddBearing.Overloads[_STRING, _ROLLING_BEARING_TYPE, _STRING](name if name else None, type_, designation if designation else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def import_fe_mesh_from_file(self, file_name: 'str', stiffness_matrix: '_71.NodalMatrix') -> '_2126.FEPart':
        ''' 'ImportFEMeshFromFile' is the original name of this method.

        Args:
            file_name (str)
            stiffness_matrix (mastapy.nodal_analysis.NodalMatrix)

        Returns:
            mastapy.system_model.part_model.FEPart
        '''

        file_name = str(file_name)
        method_result = self.wrapped.ImportFEMeshFromFile(file_name if file_name else None, stiffness_matrix.wrapped if stiffness_matrix else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_assembly(self, name: Optional['str'] = 'Assembly') -> 'Assembly':
        ''' 'AddAssembly' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.AddAssembly(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_oil_seal(self, name: Optional['str'] = 'Oil Seal') -> '_2139.OilSeal':
        ''' 'AddOilSeal' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.AddOilSeal(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_power_load(self, name: Optional['str'] = 'Power Load') -> '_2145.PowerLoad':
        ''' 'AddPowerLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPowerLoad(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_point_load(self, name: Optional['str'] = 'Point Load') -> '_2144.PointLoad':
        ''' 'AddPointLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPointLoad(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_datum(self, name: Optional['str'] = 'Datum') -> '_2122.Datum':
        ''' 'AddDatum' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.AddDatum(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_imported_fe_component(self, name: Optional['str'] = 'Imported FE') -> '_2126.FEPart':
        ''' 'AddImportedFEComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.FEPart
        '''

        name = str(name)
        method_result = self.wrapped.AddImportedFEComponent(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_measurement_component(self, name: Optional['str'] = 'Measurement Component') -> '_2136.MeasurementComponent':
        ''' 'AddMeasurementComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.AddMeasurementComponent(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_mass_disc(self, name: Optional['str'] = 'Mass Disc') -> '_2135.MassDisc':
        ''' 'AddMassDisc' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.AddMassDisc(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_unbalanced_mass(self, name: Optional['str'] = 'Unbalanced Mass') -> '_2150.UnbalancedMass':
        ''' 'AddUnbalancedMass' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.AddUnbalancedMass(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_straight_bevel_differential_gear_set(self, name: Optional['str'] = 'Straight Bevel Differential Gear Set') -> '_2217.StraightBevelDiffGearSet':
        ''' 'AddStraightBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelDifferentialGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_spiral_bevel_differential_gear_set(self, name: Optional['str'] = 'Spiral Bevel Differential Gear Set') -> '_2187.BevelDifferentialGearSet':
        ''' 'AddSpiralBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelDifferentialGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_zerol_bevel_differential_gear_set(self, name: Optional['str'] = 'Zerol Bevel Differential Gear Set') -> '_2187.BevelDifferentialGearSet':
        ''' 'AddZerolBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelDifferentialGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_planetary_gear_set(self, name: Optional['str'] = 'Planetary Gear Set') -> '_2213.PlanetaryGearSet':
        ''' 'AddPlanetaryGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddPlanetaryGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_spiral_bevel_gear_set(self, name: Optional['str'] = 'Spiral Bevel Gear Set') -> '_2215.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelGearSet.Overloads[_STRING](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Spiral Bevel Gear Set') -> '_2212.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'AddKlingelnbergCycloPalloidSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidSpiralBevelGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Hypoid Gear Set') -> '_2210.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'AddKlingelnbergCycloPalloidHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidHypoidGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_straight_bevel_gear_set(self, name: Optional['str'] = 'Straight Bevel Gear Set') -> '_2219.StraightBevelGearSet':
        ''' 'AddStraightBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_hypoid_gear_set(self, name: Optional['str'] = 'Hypoid Gear Set') -> '_2206.HypoidGearSet':
        ''' 'AddHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddHypoidGearSet.Overloads[_STRING](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_worm_gear_set(self, name: Optional['str'] = 'Worm Gear Set') -> '_2223.WormGearSet':
        ''' 'AddWormGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddWormGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_zerol_bevel_gear_set(self, name: Optional['str'] = 'Zerol Bevel Gear Set') -> '_2225.ZerolBevelGearSet':
        ''' 'AddZerolBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelGearSet(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_clutch(self, name: Optional['str'] = 'Clutch') -> '_2249.Clutch':
        ''' 'AddClutch' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.AddClutch(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_synchroniser(self, name: Optional['str'] = 'Synchroniser') -> '_2273.Synchroniser':
        ''' 'AddSynchroniser' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.AddSynchroniser(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_rolling_ring(self, name: Optional['str'] = 'Rolling Ring') -> '_2267.RollingRing':
        ''' 'AddRollingRing' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.AddRollingRing(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_concept_coupling(self, name: Optional['str'] = 'Concept Coupling') -> '_2252.ConceptCoupling':
        ''' 'AddConceptCoupling' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.AddConceptCoupling(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_cvt(self, name: Optional['str'] = 'CVT') -> '_2257.CVT':
        ''' 'AddCVT' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.AddCVT(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_spring_damper(self, name: Optional['str'] = 'Spring Damper') -> '_2271.SpringDamper':
        ''' 'AddSpringDamper' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.AddSpringDamper(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_torque_converter(self, name: Optional['str'] = 'Torque Converter') -> '_2278.TorqueConverter':
        ''' 'AddTorqueConverter' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.AddTorqueConverter(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_bolted_joint(self, name: Optional['str'] = 'Bolted Joint') -> '_2117.BoltedJoint':
        ''' 'AddBoltedJoint' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.AddBoltedJoint(name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_belt_drive_with_options(self, belt_creation_options: Optional['_2242.BeltCreationOptions'] = None) -> '_2247.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            belt_creation_options (mastapy.system_model.part_model.creation_options.BeltCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        method_result = self.wrapped.AddBeltDrive.Overloads[_BELT_CREATION_OPTIONS](belt_creation_options.wrapped if belt_creation_options else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_belt_drive(self, centre_distance: Optional['float'] = 0.1, pulley_a_diameter: Optional['float'] = 0.08, pulley_b_diameter: Optional['float'] = 0.08, name: Optional['str'] = 'Belt Drive') -> '_2247.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            centre_distance (float, optional)
            pulley_a_diameter (float, optional)
            pulley_b_diameter (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        centre_distance = float(centre_distance)
        pulley_a_diameter = float(pulley_a_diameter)
        pulley_b_diameter = float(pulley_b_diameter)
        name = str(name)
        method_result = self.wrapped.AddBeltDrive.Overloads[_DOUBLE, _DOUBLE, _DOUBLE, _STRING](centre_distance if centre_distance else 0.0, pulley_a_diameter if pulley_a_diameter else 0.0, pulley_b_diameter if pulley_b_diameter else 0.0, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_planet_carrier_with_options(self, planet_carrier_creation_options: Optional['_2245.PlanetCarrierCreationOptions'] = None) -> '_2142.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            planet_carrier_creation_options (mastapy.system_model.part_model.creation_options.PlanetCarrierCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        method_result = self.wrapped.AddPlanetCarrier.Overloads[_PLANET_CARRIER_CREATION_OPTIONS](planet_carrier_creation_options.wrapped if planet_carrier_creation_options else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_planet_carrier(self, number_of_planets: Optional['int'] = 3, diameter: Optional['float'] = 0.05) -> '_2142.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            number_of_planets (int, optional)
            diameter (float, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        number_of_planets = int(number_of_planets)
        diameter = float(diameter)
        method_result = self.wrapped.AddPlanetCarrier.Overloads[_INT_32, _DOUBLE](number_of_planets if number_of_planets else 0, diameter if diameter else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_shaft_with_options(self, shaft_creation_options: '_2246.ShaftCreationOptions') -> '_2154.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            shaft_creation_options (mastapy.system_model.part_model.creation_options.ShaftCreationOptions)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        method_result = self.wrapped.AddShaft.Overloads[_SHAFT_CREATION_OPTIONS](shaft_creation_options.wrapped if shaft_creation_options else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_shaft(self, length: Optional['float'] = 0.1, outer_diameter: Optional['float'] = 0.025, bore: Optional['float'] = 0.0, name: Optional['str'] = 'Shaft') -> '_2154.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            length (float, optional)
            outer_diameter (float, optional)
            bore (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        length = float(length)
        outer_diameter = float(outer_diameter)
        bore = float(bore)
        name = str(name)
        method_result = self.wrapped.AddShaft.Overloads[_DOUBLE, _DOUBLE, _DOUBLE, _STRING](length if length else 0.0, outer_diameter if outer_diameter else 0.0, bore if bore else 0.0, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_cylindrical_gear_pair_with_options(self, cylindrical_gear_pair_creation_options: Optional['_1056.CylindricalGearPairCreationOptions'] = None) -> '_2197.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            cylindrical_gear_pair_creation_options (mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearPair.Overloads[_CYLINDRICAL_GEAR_PAIR_CREATION_OPTIONS](cylindrical_gear_pair_creation_options.wrapped if cylindrical_gear_pair_creation_options else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_cylindrical_gear_pair(self, centre_distance: 'float') -> '_2197.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            centre_distance (float)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        centre_distance = float(centre_distance)
        method_result = self.wrapped.AddCylindricalGearPair.Overloads[_DOUBLE](centre_distance if centre_distance else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_cylindrical_gear_set_with_options(self, cylindrical_gear_linear_train_creation_options: Optional['_2244.CylindricalGearLinearTrainCreationOptions'] = None) -> '_2197.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            cylindrical_gear_linear_train_creation_options (mastapy.system_model.part_model.creation_options.CylindricalGearLinearTrainCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearSet.Overloads[_CYLINDRICAL_GEAR_LINEAR_TRAIN_CREATION_OPTIONS](cylindrical_gear_linear_train_creation_options.wrapped if cylindrical_gear_linear_train_creation_options else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_cylindrical_gear_set(self, name: 'str', centre_distances: 'List[float]') -> '_2197.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        centre_distances = conversion.mp_to_pn_array_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet.Overloads[_STRING, _ARRAY[_DOUBLE]](name if name else None, centre_distances)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
