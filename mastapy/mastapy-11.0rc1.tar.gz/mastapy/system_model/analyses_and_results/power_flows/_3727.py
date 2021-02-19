'''_3727.py

ConnectionPowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1948, _1941, _1944, _1945,
    _1949, _1957, _1963, _1968,
    _1971
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1975, _1977, _1979, _1981,
    _1983, _1985, _1987, _1989,
    _1991, _1994, _1995, _1996,
    _1999, _2001, _2003, _2005,
    _2007
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2011, _2014, _2017
from mastapy.system_model.connections_and_sockets.couplings import (
    _2018, _2020, _2022, _2024,
    _2026, _2028
)
from mastapy.system_model.analyses_and_results.power_flows import _3780
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2391, _2357, _2358, _2363,
    _2365, _2370, _2375, _2378,
    _2381, _2384, _2388, _2393,
    _2396, _2400, _2401, _2403,
    _2404, _2405, _2416, _2421,
    _2425, _2429, _2430, _2433,
    _2436, _2448, _2451, _2457,
    _2460, _2467, _2469, _2472,
    _2475, _2478, _2490, _2498,
    _2501
)
from mastapy.system_model.analyses_and_results.analysis_cases import _7171
from mastapy._internal.python_net import python_net_import

_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionPowerFlow',)


class ConnectionPowerFlow(_7171.ConnectionStaticLoadAnalysisCase):
    '''ConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_loaded(self) -> 'bool':
        '''bool: 'IsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoaded

    @property
    def component_design(self) -> '_1948.Connection':
        '''Connection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1948.Connection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1941.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1941.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_belt_connection(self) -> '_1944.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1944.BeltConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coaxial_connection(self) -> '_1945.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.CoaxialConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_belt_connection(self) -> '_1949.CVTBeltConnection':
        '''CVTBeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.CVTBeltConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_inter_mountable_component_connection(self) -> '_1957.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.InterMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planetary_connection(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.PlanetaryConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring_connection(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.RollingRingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_to_mountable_component_connection(self) -> '_1971.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1971.ShaftToMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1975.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear_mesh(self) -> '_1977.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1977.BevelDifferentialGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_gear_mesh(self) -> '_1979.BevelGearMesh':
        '''BevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1979.BevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear_mesh(self) -> '_1981.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.ConceptGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_conical_gear_mesh(self) -> '_1983.ConicalGearMesh':
        '''ConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.ConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear_mesh(self) -> '_1985.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.CylindricalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear_mesh(self) -> '_1987.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.FaceGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_gear_mesh(self) -> '_1989.GearMesh':
        '''GearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.GearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear_mesh(self) -> '_1991.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.HypoidGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1994.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1995.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1996.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear_mesh(self) -> '_1999.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.SpiralBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_2001.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear_mesh(self) -> '_2003.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.StraightBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear_mesh(self) -> '_2005.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.WormGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear_mesh(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.ZerolBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2011.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_ring_pins_to_disc_connection(self) -> '_2017.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.RingPinsToDiscConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_connection(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.ClutchConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_connection(self) -> '_2020.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.ConceptCouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coupling_connection(self) -> '_2022.CouplingConnection':
        '''CouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.CouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling_connection(self) -> '_2024.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_connection(self) -> '_2026.SpringDamperConnection':
        '''SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.SpringDamperConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_connection(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.TorqueConverterConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1948.Connection':
        '''Connection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1948.Connection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to Connection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1941.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1941.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_belt_connection(self) -> '_1944.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1944.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coaxial_connection(self) -> '_1945.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.CoaxialConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cvt_belt_connection(self) -> '_1949.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.CVTBeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_inter_mountable_component_connection(self) -> '_1957.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.InterMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_planetary_connection(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.PlanetaryConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_rolling_ring_connection(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1968.RollingRingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_shaft_to_mountable_component_connection(self) -> '_1971.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1971.ShaftToMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1975.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1977.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1977.BevelDifferentialGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_1979.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1979.BevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_gear_mesh(self) -> '_1981.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.ConceptGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_conical_gear_mesh(self) -> '_1983.ConicalGearMesh':
        '''ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.ConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cylindrical_gear_mesh(self) -> '_1985.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.CylindricalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_face_gear_mesh(self) -> '_1987.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.FaceGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_gear_mesh(self) -> '_1989.GearMesh':
        '''GearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.GearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to GearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1991.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.HypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1994.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1995.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1996.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1999.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.SpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_2001.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_2003.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.StraightBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_worm_gear_mesh(self) -> '_2005.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.WormGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_2007.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.ZerolBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2011.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_ring_pins_to_disc_connection(self) -> '_2017.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.RingPinsToDiscConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_clutch_connection(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.ClutchConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_coupling_connection(self) -> '_2020.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2020.ConceptCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coupling_connection(self) -> '_2022.CouplingConnection':
        '''CouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.CouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_part_to_part_shear_coupling_connection(self) -> '_2024.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spring_damper_connection(self) -> '_2026.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.SpringDamperConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_torque_converter_connection(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.TorqueConverterConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def power_flow(self) -> '_3780.PowerFlow':
        '''PowerFlow: 'PowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3780.PowerFlow)(self.wrapped.PowerFlow) if self.wrapped.PowerFlow else None

    @property
    def torsional_system_deflection_analysis(self) -> '_2391.ConnectionSystemDeflection':
        '''ConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2391.ConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_abstract_shaft_to_mountable_component_connection_system_deflection(self) -> '_2357.AbstractShaftToMountableComponentConnectionSystemDeflection':
        '''AbstractShaftToMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2357.AbstractShaftToMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to AbstractShaftToMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2358.AGMAGleasonConicalGearMeshSystemDeflection':
        '''AGMAGleasonConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2358.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_belt_connection_system_deflection(self) -> '_2363.BeltConnectionSystemDeflection':
        '''BeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2363.BeltConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2365.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2365.BevelDifferentialGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_bevel_gear_mesh_system_deflection(self) -> '_2370.BevelGearMeshSystemDeflection':
        '''BevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2370.BevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_clutch_connection_system_deflection(self) -> '_2375.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2375.ClutchConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ClutchConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_coaxial_connection_system_deflection(self) -> '_2378.CoaxialConnectionSystemDeflection':
        '''CoaxialConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2378.CoaxialConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CoaxialConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_coupling_connection_system_deflection(self) -> '_2381.ConceptCouplingConnectionSystemDeflection':
        '''ConceptCouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2381.ConceptCouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptCouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_gear_mesh_system_deflection(self) -> '_2384.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2384.ConceptGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_conical_gear_mesh_system_deflection(self) -> '_2388.ConicalGearMeshSystemDeflection':
        '''ConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2388.ConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_coupling_connection_system_deflection(self) -> '_2393.CouplingConnectionSystemDeflection':
        '''CouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2393.CouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cvt_belt_connection_system_deflection(self) -> '_2396.CVTBeltConnectionSystemDeflection':
        '''CVTBeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2396.CVTBeltConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CVTBeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cycloidal_disc_central_bearing_connection_system_deflection(self) -> '_2400.CycloidalDiscCentralBearingConnectionSystemDeflection':
        '''CycloidalDiscCentralBearingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2400.CycloidalDiscCentralBearingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CycloidalDiscCentralBearingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cycloidal_disc_planetary_bearing_connection_system_deflection(self) -> '_2401.CycloidalDiscPlanetaryBearingConnectionSystemDeflection':
        '''CycloidalDiscPlanetaryBearingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2401.CycloidalDiscPlanetaryBearingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CycloidalDiscPlanetaryBearingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2403.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2403.CylindricalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2404.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2404.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2405.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2405.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_face_gear_mesh_system_deflection(self) -> '_2416.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2416.FaceGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_gear_mesh_system_deflection(self) -> '_2421.GearMeshSystemDeflection':
        '''GearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2421.GearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to GearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2425.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2425.HypoidGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_inter_mountable_component_connection_system_deflection(self) -> '_2429.InterMountableComponentConnectionSystemDeflection':
        '''InterMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2429.InterMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to InterMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2430.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2430.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2433.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2433.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2436.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2436.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_part_to_part_shear_coupling_connection_system_deflection(self) -> '_2448.PartToPartShearCouplingConnectionSystemDeflection':
        '''PartToPartShearCouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2448.PartToPartShearCouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to PartToPartShearCouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_planetary_connection_system_deflection(self) -> '_2451.PlanetaryConnectionSystemDeflection':
        '''PlanetaryConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2451.PlanetaryConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to PlanetaryConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_ring_pins_to_disc_connection_system_deflection(self) -> '_2457.RingPinsToDiscConnectionSystemDeflection':
        '''RingPinsToDiscConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2457.RingPinsToDiscConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to RingPinsToDiscConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_rolling_ring_connection_system_deflection(self) -> '_2460.RollingRingConnectionSystemDeflection':
        '''RollingRingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2460.RollingRingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to RollingRingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_shaft_to_mountable_component_connection_system_deflection(self) -> '_2467.ShaftToMountableComponentConnectionSystemDeflection':
        '''ShaftToMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2467.ShaftToMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ShaftToMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2469.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2469.SpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spring_damper_connection_system_deflection(self) -> '_2472.SpringDamperConnectionSystemDeflection':
        '''SpringDamperConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2472.SpringDamperConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpringDamperConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2475.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2475.StraightBevelDiffGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2478.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2478.StraightBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_torque_converter_connection_system_deflection(self) -> '_2490.TorqueConverterConnectionSystemDeflection':
        '''TorqueConverterConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2490.TorqueConverterConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to TorqueConverterConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_worm_gear_mesh_system_deflection(self) -> '_2498.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2498.WormGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to WormGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2501.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2501.ZerolBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None
