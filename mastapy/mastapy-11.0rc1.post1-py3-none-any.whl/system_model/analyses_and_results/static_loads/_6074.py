'''_6074.py

LoadCase
'''


from typing import List

from mastapy.system_model.analyses_and_results import (
    _2198, _2193, _2176, _2184,
    _2191, _2192, _2178, _2195,
    _2196, _2197, _2189, _2179,
    _2188, _2187, _2185, _2186,
    _2199, _2194, _2177, _2182,
    _2181, _2180, _2183, _2190,
    _2175, _2202
)
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1732
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_results.rolling import _1599
from mastapy.system_model import _1822, _1819, _1830
from mastapy.gears import _137
from mastapy.system_model.analyses_and_results.static_loads import (
    _6234, _6077, _6195, _6079,
    _6122, _6163, _6169, _6172,
    _6175, _6208, _6218, _6239,
    _6242, _6149, _6185, _6096,
    _6101, _6114, _6210, _6228,
    _6081, _6075, _6076, _6083,
    _6095, _6094, _6100, _6113,
    _6128, _6141, _6145, _6082,
    _6153, _6165, _6177, _6178,
    _6180, _6182, _6184, _6191,
    _6194, _6201, _6205, _6236,
    _6237, _6203, _6104, _6106,
    _6142, _6144, _6078, _6080,
    _6086, _6088, _6089, _6090,
    _6091, _6093, _6107, _6111,
    _6120, _6124, _6125, _6147,
    _6152, _6162, _6164, _6168,
    _6170, _6171, _6173, _6174,
    _6176, _6189, _6207, _6209,
    _6214, _6216, _6217, _6219,
    _6220, _6221, _6238, _6240,
    _6241, _6243, _6187, _6186,
    _6085, _6098, _6097, _6103,
    _6102, _6116, _6115, _6118,
    _6119, _6196, _6202, _6200,
    _6198, _6212, _6211, _6223,
    _6222, _6224, _6225, _6229,
    _6230, _6231, _6117, _6084,
    _6099, _6112, _6167, _6188,
    _6199, _6204, _6087, _6105,
    _6143, _6215, _6092, _6109
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3574
from mastapy.system_model.connections_and_sockets.gears import (
    _1879, _1889, _1895, _1898,
    _1899, _1900, _1903, _1907,
    _1909, _1911, _1893, _1881,
    _1885, _1891, _1905, _1883,
    _1887
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1919, _1913, _1915, _1917,
    _1921, _1923
)
from mastapy.system_model.part_model import (
    _2001, _2002, _2005, _2007,
    _2008, _2009, _2012, _2013,
    _2016, _2017, _2000, _2018,
    _2021, _2025, _2026, _2027,
    _2029, _2031, _2032, _2034,
    _2035, _2037, _2039, _2040,
    _2041
)
from mastapy.system_model.part_model.shaft_model import _2044
from mastapy.system_model.part_model.gears import (
    _2082, _2083, _2089, _2090,
    _2074, _2075, _2076, _2077,
    _2078, _2079, _2080, _2081,
    _2084, _2085, _2086, _2087,
    _2088, _2091, _2093, _2095,
    _2096, _2097, _2098, _2099,
    _2100, _2101, _2102, _2103,
    _2104, _2105, _2106, _2107,
    _2108, _2109, _2110, _2111,
    _2112, _2113, _2114, _2115
)
from mastapy.system_model.part_model.couplings import (
    _2144, _2145, _2133, _2135,
    _2136, _2138, _2139, _2140,
    _2141, _2142, _2143, _2146,
    _2154, _2152, _2153, _2155,
    _2156, _2157, _2159, _2160,
    _2161, _2162, _2163, _2165
)
from mastapy.system_model.connections_and_sockets import (
    _1856, _1851, _1852, _1855,
    _1864, _1867, _1871, _1875
)
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_IMPORTED_FE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ImportedFEComponent')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'LoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCase',)


class LoadCase(_2202.Context):
    '''LoadCase

    This is a mastapy class.
    '''

    TYPE = _LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def system_deflection(self) -> '_2198.SystemDeflectionAnalysis':
        '''SystemDeflectionAnalysis: 'SystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.SystemDeflectionAnalysis)(self.wrapped.SystemDeflection) if self.wrapped.SystemDeflection else None

    @property
    def power_flow(self) -> '_2193.PowerFlowAnalysis':
        '''PowerFlowAnalysis: 'PowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2193.PowerFlowAnalysis)(self.wrapped.PowerFlow) if self.wrapped.PowerFlow else None

    @property
    def advanced_system_deflection(self) -> '_2176.AdvancedSystemDeflectionAnalysis':
        '''AdvancedSystemDeflectionAnalysis: 'AdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2176.AdvancedSystemDeflectionAnalysis)(self.wrapped.AdvancedSystemDeflection) if self.wrapped.AdvancedSystemDeflection else None

    @property
    def gear_whine_analysis(self) -> '_2184.GearWhineAnalysisAnalysis':
        '''GearWhineAnalysisAnalysis: 'GearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2184.GearWhineAnalysisAnalysis)(self.wrapped.GearWhineAnalysis) if self.wrapped.GearWhineAnalysis else None

    @property
    def multibody_dynamics(self) -> '_2191.MultibodyDynamicsAnalysis':
        '''MultibodyDynamicsAnalysis: 'MultibodyDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2191.MultibodyDynamicsAnalysis)(self.wrapped.MultibodyDynamics) if self.wrapped.MultibodyDynamics else None

    @property
    def parametric_study_tool(self) -> '_2192.ParametricStudyToolAnalysis':
        '''ParametricStudyToolAnalysis: 'ParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.ParametricStudyToolAnalysis)(self.wrapped.ParametricStudyTool) if self.wrapped.ParametricStudyTool else None

    @property
    def compound_parametric_study_tool(self) -> '_2178.CompoundParametricStudyToolAnalysis':
        '''CompoundParametricStudyToolAnalysis: 'CompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2178.CompoundParametricStudyToolAnalysis)(self.wrapped.CompoundParametricStudyTool) if self.wrapped.CompoundParametricStudyTool else None

    @property
    def steady_state_synchronous_response(self) -> '_2195.SteadyStateSynchronousResponseAnalysis':
        '''SteadyStateSynchronousResponseAnalysis: 'SteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2195.SteadyStateSynchronousResponseAnalysis)(self.wrapped.SteadyStateSynchronousResponse) if self.wrapped.SteadyStateSynchronousResponse else None

    @property
    def steady_state_synchronous_responseata_speed(self) -> '_2196.SteadyStateSynchronousResponseataSpeedAnalysis':
        '''SteadyStateSynchronousResponseataSpeedAnalysis: 'SteadyStateSynchronousResponseataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.SteadyStateSynchronousResponseataSpeedAnalysis)(self.wrapped.SteadyStateSynchronousResponseataSpeed) if self.wrapped.SteadyStateSynchronousResponseataSpeed else None

    @property
    def steady_state_synchronous_responseona_shaft(self) -> '_2197.SteadyStateSynchronousResponseonaShaftAnalysis':
        '''SteadyStateSynchronousResponseonaShaftAnalysis: 'SteadyStateSynchronousResponseonaShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2197.SteadyStateSynchronousResponseonaShaftAnalysis)(self.wrapped.SteadyStateSynchronousResponseonaShaft) if self.wrapped.SteadyStateSynchronousResponseonaShaft else None

    @property
    def modal_analysis(self) -> '_2189.ModalAnalysisAnalysis':
        '''ModalAnalysisAnalysis: 'ModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2189.ModalAnalysisAnalysis)(self.wrapped.ModalAnalysis) if self.wrapped.ModalAnalysis else None

    @property
    def dynamic_analysis(self) -> '_2179.DynamicAnalysisAnalysis':
        '''DynamicAnalysisAnalysis: 'DynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2179.DynamicAnalysisAnalysis)(self.wrapped.DynamicAnalysis) if self.wrapped.DynamicAnalysis else None

    @property
    def modal_analysesat_stiffnesses(self) -> '_2188.ModalAnalysesatStiffnessesAnalysis':
        '''ModalAnalysesatStiffnessesAnalysis: 'ModalAnalysesatStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2188.ModalAnalysesatStiffnessesAnalysis)(self.wrapped.ModalAnalysesatStiffnesses) if self.wrapped.ModalAnalysesatStiffnesses else None

    @property
    def modal_analysesat_speeds(self) -> '_2187.ModalAnalysesatSpeedsAnalysis':
        '''ModalAnalysesatSpeedsAnalysis: 'ModalAnalysesatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.ModalAnalysesatSpeedsAnalysis)(self.wrapped.ModalAnalysesatSpeeds) if self.wrapped.ModalAnalysesatSpeeds else None

    @property
    def modal_analysesata_speed(self) -> '_2185.ModalAnalysesataSpeedAnalysis':
        '''ModalAnalysesataSpeedAnalysis: 'ModalAnalysesataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.ModalAnalysesataSpeedAnalysis)(self.wrapped.ModalAnalysesataSpeed) if self.wrapped.ModalAnalysesataSpeed else None

    @property
    def modal_analysesata_stiffness(self) -> '_2186.ModalAnalysesataStiffnessAnalysis':
        '''ModalAnalysesataStiffnessAnalysis: 'ModalAnalysesataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2186.ModalAnalysesataStiffnessAnalysis)(self.wrapped.ModalAnalysesataStiffness) if self.wrapped.ModalAnalysesataStiffness else None

    @property
    def torsional_system_deflection(self) -> '_2199.TorsionalSystemDeflectionAnalysis':
        '''TorsionalSystemDeflectionAnalysis: 'TorsionalSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2199.TorsionalSystemDeflectionAnalysis)(self.wrapped.TorsionalSystemDeflection) if self.wrapped.TorsionalSystemDeflection else None

    @property
    def single_mesh_whine_analysis(self) -> '_2194.SingleMeshWhineAnalysisAnalysis':
        '''SingleMeshWhineAnalysisAnalysis: 'SingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.SingleMeshWhineAnalysisAnalysis)(self.wrapped.SingleMeshWhineAnalysis) if self.wrapped.SingleMeshWhineAnalysis else None

    @property
    def advanced_system_deflection_sub_analysis(self) -> '_2177.AdvancedSystemDeflectionSubAnalysisAnalysis':
        '''AdvancedSystemDeflectionSubAnalysisAnalysis: 'AdvancedSystemDeflectionSubAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.AdvancedSystemDeflectionSubAnalysisAnalysis)(self.wrapped.AdvancedSystemDeflectionSubAnalysis) if self.wrapped.AdvancedSystemDeflectionSubAnalysis else None

    @property
    def dynamic_modelfor_gear_whine(self) -> '_2182.DynamicModelforGearWhineAnalysis':
        '''DynamicModelforGearWhineAnalysis: 'DynamicModelforGearWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2182.DynamicModelforGearWhineAnalysis)(self.wrapped.DynamicModelforGearWhine) if self.wrapped.DynamicModelforGearWhine else None

    @property
    def dynamic_modelforat_speeds(self) -> '_2181.DynamicModelforatSpeedsAnalysis':
        '''DynamicModelforatSpeedsAnalysis: 'DynamicModelforatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.DynamicModelforatSpeedsAnalysis)(self.wrapped.DynamicModelforatSpeeds) if self.wrapped.DynamicModelforatSpeeds else None

    @property
    def dynamic_modelata_stiffness(self) -> '_2180.DynamicModelataStiffnessAnalysis':
        '''DynamicModelataStiffnessAnalysis: 'DynamicModelataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.DynamicModelataStiffnessAnalysis)(self.wrapped.DynamicModelataStiffness) if self.wrapped.DynamicModelataStiffness else None

    @property
    def dynamic_modelfor_steady_state_synchronous_response(self) -> '_2183.DynamicModelforSteadyStateSynchronousResponseAnalysis':
        '''DynamicModelforSteadyStateSynchronousResponseAnalysis: 'DynamicModelforSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2183.DynamicModelforSteadyStateSynchronousResponseAnalysis)(self.wrapped.DynamicModelforSteadyStateSynchronousResponse) if self.wrapped.DynamicModelforSteadyStateSynchronousResponse else None

    @property
    def modal_analysisfor_whine(self) -> '_2190.ModalAnalysisforWhineAnalysis':
        '''ModalAnalysisforWhineAnalysis: 'ModalAnalysisforWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.ModalAnalysisforWhineAnalysis)(self.wrapped.ModalAnalysisforWhine) if self.wrapped.ModalAnalysisforWhine else None

    @property
    def include_bearing_centrifugal(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugal

    @include_bearing_centrifugal.setter
    def include_bearing_centrifugal(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugal = bool(value) if value else False

    @property
    def include_bearing_centrifugal_ring_expansion(self) -> 'bool':
        '''bool: 'IncludeBearingCentrifugalRingExpansion' is the original name of this property.'''

        return self.wrapped.IncludeBearingCentrifugalRingExpansion

    @include_bearing_centrifugal_ring_expansion.setter
    def include_bearing_centrifugal_ring_expansion(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugalRingExpansion = bool(value) if value else False

    @property
    def include_planetary_centrifugal(self) -> 'bool':
        '''bool: 'IncludePlanetaryCentrifugal' is the original name of this property.'''

        return self.wrapped.IncludePlanetaryCentrifugal

    @include_planetary_centrifugal.setter
    def include_planetary_centrifugal(self, value: 'bool'):
        self.wrapped.IncludePlanetaryCentrifugal = bool(value) if value else False

    @property
    def include_gravity(self) -> 'bool':
        '''bool: 'IncludeGravity' is the original name of this property.'''

        return self.wrapped.IncludeGravity

    @include_gravity.setter
    def include_gravity(self, value: 'bool'):
        self.wrapped.IncludeGravity = bool(value) if value else False

    @property
    def stress_concentration_method_for_rating(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod: 'StressConcentrationMethodForRating' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.StressConcentrationMethodForRating, value) if self.wrapped.StressConcentrationMethodForRating else None

    @stress_concentration_method_for_rating.setter
    def stress_concentration_method_for_rating(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.StressConcentrationMethodForRating = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfStripsForRollerCalculation) if self.wrapped.NumberOfStripsForRollerCalculation else None

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def use_default_temperatures(self) -> 'bool':
        '''bool: 'UseDefaultTemperatures' is the original name of this property.'''

        return self.wrapped.UseDefaultTemperatures

    @use_default_temperatures.setter
    def use_default_temperatures(self, value: 'bool'):
        self.wrapped.UseDefaultTemperatures = bool(value) if value else False

    @property
    def include_fitting_effects(self) -> 'bool':
        '''bool: 'IncludeFittingEffects' is the original name of this property.'''

        return self.wrapped.IncludeFittingEffects

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: 'bool'):
        self.wrapped.IncludeFittingEffects = bool(value) if value else False

    @property
    def include_thermal_expansion_effects(self) -> 'bool':
        '''bool: 'IncludeThermalExpansionEffects' is the original name of this property.'''

        return self.wrapped.IncludeThermalExpansionEffects

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: 'bool'):
        self.wrapped.IncludeThermalExpansionEffects = bool(value) if value else False

    @property
    def include_ring_ovality(self) -> 'bool':
        '''bool: 'IncludeRingOvality' is the original name of this property.'''

        return self.wrapped.IncludeRingOvality

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: 'bool'):
        self.wrapped.IncludeRingOvality = bool(value) if value else False

    @property
    def ring_ovality_scaling(self) -> 'float':
        '''float: 'RingOvalityScaling' is the original name of this property.'''

        return self.wrapped.RingOvalityScaling

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'float'):
        self.wrapped.RingOvalityScaling = float(value) if value else 0.0

    @property
    def include_gear_blank_elastic_distortion(self) -> 'bool':
        '''bool: 'IncludeGearBlankElasticDistortion' is the original name of this property.'''

        return self.wrapped.IncludeGearBlankElasticDistortion

    @include_gear_blank_elastic_distortion.setter
    def include_gear_blank_elastic_distortion(self, value: 'bool'):
        self.wrapped.IncludeGearBlankElasticDistortion = bool(value) if value else False

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> 'bool':
        '''bool: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property.'''

        return self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: 'bool'):
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = bool(value) if value else False

    @property
    def ball_bearing_contact_calculation(self) -> '_1599.BallBearingContactCalculation':
        '''BallBearingContactCalculation: 'BallBearingContactCalculation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BallBearingContactCalculation)
        return constructor.new(_1599.BallBearingContactCalculation)(value) if value else None

    @ball_bearing_contact_calculation.setter
    def ball_bearing_contact_calculation(self, value: '_1599.BallBearingContactCalculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BallBearingContactCalculation = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'bool':
        '''bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property.'''

        return self.wrapped.ModelBearingMountingClearancesAutomatically

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'bool'):
        self.wrapped.ModelBearingMountingClearancesAutomatically = bool(value) if value else False

    @property
    def maximum_shaft_section_length_to_diameter_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionLengthToDiameterRatio

    @maximum_shaft_section_length_to_diameter_ratio.setter
    def maximum_shaft_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_cross_sectional_area_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionCrossSectionalAreaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio

    @maximum_shaft_section_cross_sectional_area_ratio.setter
    def maximum_shaft_section_cross_sectional_area_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self) -> 'float':
        '''float: 'MaximumShaftSectionPolarAreaMomentOfInertiaRatio' is the original name of this property.'''

        return self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio

    @maximum_shaft_section_polar_area_moment_of_inertia_ratio.setter
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self) -> 'bool':
        '''bool: 'UseSingleNodeForSplineRigidBondDetailedConnectionConnections' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections

    @use_single_node_for_spline_rigid_bond_detailed_connection_connections.setter
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections = bool(value) if value else False

    @property
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio

    @spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForCylindricalGearMeshes

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value else False

    @property
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes

    @force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes.setter
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes = bool(value) if value else False

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        '''int: 'MinimumNumberOfGearMeshNodes' is the original name of this property.'''

        return self.wrapped.MinimumNumberOfGearMeshNodes

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value else 0

    @property
    def peak_load_factor_for_shafts(self) -> 'float':
        '''float: 'PeakLoadFactorForShafts' is the original name of this property.'''

        return self.wrapped.PeakLoadFactorForShafts

    @peak_load_factor_for_shafts.setter
    def peak_load_factor_for_shafts(self, value: 'float'):
        self.wrapped.PeakLoadFactorForShafts = float(value) if value else 0.0

    @property
    def mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel':
        '''enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel: 'MeshStiffnessModel' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MeshStiffnessModel, value) if self.wrapped.MeshStiffnessModel else None

    @mesh_stiffness_model.setter
    def mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MeshStiffnessModel = value

    @property
    def micro_geometry_model_in_system_deflection(self) -> 'overridable.Overridable_MicroGeometryModel':
        '''overridable.Overridable_MicroGeometryModel: 'MicroGeometryModelInSystemDeflection' is the original name of this property.'''

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MicroGeometryModelInSystemDeflection, value) if self.wrapped.MicroGeometryModelInSystemDeflection else None

    @micro_geometry_model_in_system_deflection.setter
    def micro_geometry_model_in_system_deflection(self, value: 'overridable.Overridable_MicroGeometryModel.implicit_type()'):
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None, is_overridden)
        self.wrapped.MicroGeometryModelInSystemDeflection = value

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumForceForBearingToBeConsideredLoaded) if self.wrapped.MinimumForceForBearingToBeConsideredLoaded else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumMomentForBearingToBeConsideredLoaded) if self.wrapped.MinimumMomentForBearingToBeConsideredLoaded else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def energy_convergence_absolute_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'EnergyConvergenceAbsoluteTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.EnergyConvergenceAbsoluteTolerance) if self.wrapped.EnergyConvergenceAbsoluteTolerance else None

    @energy_convergence_absolute_tolerance.setter
    def energy_convergence_absolute_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.EnergyConvergenceAbsoluteTolerance = value

    @property
    def hypoid_gear_wind_up_removal_method_for_misalignments(self) -> '_1819.HypoidWindUpRemovalMethod':
        '''HypoidWindUpRemovalMethod: 'HypoidGearWindUpRemovalMethodForMisalignments' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments)
        return constructor.new(_1819.HypoidWindUpRemovalMethod)(value) if value else None

    @hypoid_gear_wind_up_removal_method_for_misalignments.setter
    def hypoid_gear_wind_up_removal_method_for_misalignments(self, value: '_1819.HypoidWindUpRemovalMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments = value

    @property
    def include_tilt_stiffness_for_bevel_hypoid_gears(self) -> 'bool':
        '''bool: 'IncludeTiltStiffnessForBevelHypoidGears' is the original name of this property.'''

        return self.wrapped.IncludeTiltStiffnessForBevelHypoidGears

    @include_tilt_stiffness_for_bevel_hypoid_gears.setter
    def include_tilt_stiffness_for_bevel_hypoid_gears(self, value: 'bool'):
        self.wrapped.IncludeTiltStiffnessForBevelHypoidGears = bool(value) if value else False

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumPowerForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumPowerForGearMeshToBeLoaded) if self.wrapped.MinimumPowerForGearMeshToBeLoaded else None

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    def minimum_power_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumPowerForGearMeshToBeLoaded = value

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumTorqueForGearMeshToBeLoaded' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumTorqueForGearMeshToBeLoaded) if self.wrapped.MinimumTorqueForGearMeshToBeLoaded else None

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    def minimum_torque_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumTorqueForGearMeshToBeLoaded = value

    @property
    def tolerance_factor_for_outer_fit(self) -> 'float':
        '''float: 'ToleranceFactorForOuterFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForOuterFit

    @tolerance_factor_for_outer_fit.setter
    def tolerance_factor_for_outer_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForOuterFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_fit(self) -> 'float':
        '''float: 'ToleranceFactorForInnerFit' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForInnerFit

    @tolerance_factor_for_inner_fit.setter
    def tolerance_factor_for_inner_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForInnerFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_outer_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterSupport) if self.wrapped.ToleranceFactorForOuterSupport else None

    @tolerance_factor_for_outer_support.setter
    def tolerance_factor_for_outer_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterSupport = value

    @property
    def tolerance_factor_for_outer_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterRing) if self.wrapped.ToleranceFactorForOuterRing else None

    @tolerance_factor_for_outer_ring.setter
    def tolerance_factor_for_outer_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterRing = value

    @property
    def tolerance_factor_for_inner_support(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerSupport' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerSupport) if self.wrapped.ToleranceFactorForInnerSupport else None

    @tolerance_factor_for_inner_support.setter
    def tolerance_factor_for_inner_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerSupport = value

    @property
    def tolerance_factor_for_inner_ring(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerRing) if self.wrapped.ToleranceFactorForInnerRing else None

    @tolerance_factor_for_inner_ring.setter
    def tolerance_factor_for_inner_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerRing = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveBore' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerMountingSleeveBore) if self.wrapped.ToleranceFactorForInnerMountingSleeveBore else None

    @tolerance_factor_for_inner_mounting_sleeve_bore.setter
    def tolerance_factor_for_inner_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveBore = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveOuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter) if self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter else None

    @tolerance_factor_for_inner_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveBore' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterMountingSleeveBore) if self.wrapped.ToleranceFactorForOuterMountingSleeveBore else None

    @tolerance_factor_for_outer_mounting_sleeve_bore.setter
    def tolerance_factor_for_outer_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveBore = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveOuterDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter) if self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter else None

    @tolerance_factor_for_outer_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_radial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForRadialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForRadialInternalClearances

    @tolerance_factor_for_radial_internal_clearances.setter
    def tolerance_factor_for_radial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForRadialInternalClearances = float(value) if value else 0.0

    @property
    def tolerance_factor_for_axial_internal_clearances(self) -> 'float':
        '''float: 'ToleranceFactorForAxialInternalClearances' is the original name of this property.'''

        return self.wrapped.ToleranceFactorForAxialInternalClearances

    @tolerance_factor_for_axial_internal_clearances.setter
    def tolerance_factor_for_axial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForAxialInternalClearances = float(value) if value else 0.0

    @property
    def relative_tolerance_for_convergence(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RelativeToleranceForConvergence' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RelativeToleranceForConvergence) if self.wrapped.RelativeToleranceForConvergence else None

    @relative_tolerance_for_convergence.setter
    def relative_tolerance_for_convergence(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RelativeToleranceForConvergence = value

    @property
    def air_density(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AirDensity' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AirDensity) if self.wrapped.AirDensity else None

    @air_density.setter
    def air_density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AirDensity = value

    @property
    def speed_of_sound(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpeedOfSound' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpeedOfSound) if self.wrapped.SpeedOfSound else None

    @speed_of_sound.setter
    def speed_of_sound(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SpeedOfSound = value

    @property
    def characteristic_specific_acoustic_impedance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CharacteristicSpecificAcousticImpedance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CharacteristicSpecificAcousticImpedance) if self.wrapped.CharacteristicSpecificAcousticImpedance else None

    @characteristic_specific_acoustic_impedance.setter
    def characteristic_specific_acoustic_impedance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.CharacteristicSpecificAcousticImpedance = value

    @property
    def transmission_efficiency_settings(self) -> '_6234.TransmissionEfficiencySettings':
        '''TransmissionEfficiencySettings: 'TransmissionEfficiencySettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6234.TransmissionEfficiencySettings)(self.wrapped.TransmissionEfficiencySettings) if self.wrapped.TransmissionEfficiencySettings else None

    @property
    def additional_acceleration(self) -> '_6077.AdditionalAccelerationOptions':
        '''AdditionalAccelerationOptions: 'AdditionalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6077.AdditionalAccelerationOptions)(self.wrapped.AdditionalAcceleration) if self.wrapped.AdditionalAcceleration else None

    @property
    def temperatures(self) -> '_1830.TransmissionTemperatureSet':
        '''TransmissionTemperatureSet: 'Temperatures' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1830.TransmissionTemperatureSet)(self.wrapped.Temperatures) if self.wrapped.Temperatures else None

    @property
    def input_power_load(self) -> '_6195.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'InputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6195.PowerLoadLoadCase)(self.wrapped.InputPowerLoad) if self.wrapped.InputPowerLoad else None

    @property
    def output_power_load(self) -> '_6195.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'OutputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6195.PowerLoadLoadCase)(self.wrapped.OutputPowerLoad) if self.wrapped.OutputPowerLoad else None

    @property
    def parametric_study_tool_options(self) -> '_3574.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricStudyToolOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3574.ParametricStudyToolOptions)(self.wrapped.ParametricStudyToolOptions) if self.wrapped.ParametricStudyToolOptions else None

    @property
    def power_loads(self) -> 'List[_6195.PowerLoadLoadCase]':
        '''List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6195.PowerLoadLoadCase))
        return value

    def inputs_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1879.AGMAGleasonConicalGearMesh') -> '_6079.AGMAGleasonConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_cylindrical_gear_mesh(self, design_entity: '_1889.CylindricalGearMesh') -> '_6122.CylindricalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_hypoid_gear_mesh(self, design_entity: '_1895.HypoidGearMesh') -> '_6163.HypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1898.KlingelnbergCycloPalloidConicalGearMesh') -> '_6169.KlingelnbergCycloPalloidConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1899.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6172.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1900.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6175.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear_mesh(self, design_entity: '_1903.SpiralBevelGearMesh') -> '_6208.SpiralBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear_mesh(self, design_entity: '_1907.StraightBevelGearMesh') -> '_6218.StraightBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_worm_gear_mesh(self, design_entity: '_1909.WormGearMesh') -> '_6239.WormGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear_mesh(self, design_entity: '_1911.ZerolBevelGearMesh') -> '_6242.ZerolBevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_gear_mesh(self, design_entity: '_1893.GearMesh') -> '_6149.GearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling_connection(self, design_entity: '_1919.PartToPartShearCouplingConnection') -> '_6185.PartToPartShearCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_clutch_connection(self, design_entity: '_1913.ClutchConnection') -> '_6096.ClutchConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_concept_coupling_connection(self, design_entity: '_1915.ConceptCouplingConnection') -> '_6101.ConceptCouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_coupling_connection(self, design_entity: '_1917.CouplingConnection') -> '_6114.CouplingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_spring_damper_connection(self, design_entity: '_1921.SpringDamperConnection') -> '_6210.SpringDamperConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_torque_converter_connection(self, design_entity: '_1923.TorqueConverterConnection') -> '_6228.TorqueConverterConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def analysis_of(self, analysis_type: '_6081.AnalysisType') -> '_2175.SingleAnalysis':
        ''' 'AnalysisOf' is the original name of this method.

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)

        Returns:
            mastapy.system_model.analyses_and_results.SingleAnalysis
        '''

        analysis_type = conversion.mp_to_pn_enum(analysis_type)
        method_result = self.wrapped.AnalysisOf(analysis_type)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()

    def inputs_for_abstract_assembly(self, design_entity: '_2001.AbstractAssembly') -> '_6075.AbstractAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_abstract_shaft_or_housing(self, design_entity: '_2002.AbstractShaftOrHousing') -> '_6076.AbstractShaftOrHousingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bearing(self, design_entity: '_2005.Bearing') -> '_6083.BearingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bolt(self, design_entity: '_2007.Bolt') -> '_6095.BoltLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bolted_joint(self, design_entity: '_2008.BoltedJoint') -> '_6094.BoltedJointLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_component(self, design_entity: '_2009.Component') -> '_6100.ComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_connector(self, design_entity: '_2012.Connector') -> '_6113.ConnectorLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_datum(self, design_entity: '_2013.Datum') -> '_6128.DatumLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_external_cad_model(self, design_entity: '_2016.ExternalCADModel') -> '_6141.ExternalCADModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_flexible_pin_assembly(self, design_entity: '_2017.FlexiblePinAssembly') -> '_6145.FlexiblePinAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_assembly(self, design_entity: '_2000.Assembly') -> '_6082.AssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_guide_dxf_model(self, design_entity: '_2018.GuideDxfModel') -> '_6153.GuideDxfModelLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_imported_fe_component(self, design_entity: '_2021.ImportedFEComponent') -> '_6165.ImportedFEComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_IMPORTED_FE_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_mass_disc(self, design_entity: '_2025.MassDisc') -> '_6177.MassDiscLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_measurement_component(self, design_entity: '_2026.MeasurementComponent') -> '_6178.MeasurementComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_mountable_component(self, design_entity: '_2027.MountableComponent') -> '_6180.MountableComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_oil_seal(self, design_entity: '_2029.OilSeal') -> '_6182.OilSealLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_part(self, design_entity: '_2031.Part') -> '_6184.PartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_planet_carrier(self, design_entity: '_2032.PlanetCarrier') -> '_6191.PlanetCarrierLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_point_load(self, design_entity: '_2034.PointLoad') -> '_6194.PointLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_power_load(self, design_entity: '_2035.PowerLoad') -> '_6195.PowerLoadLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_root_assembly(self, design_entity: '_2037.RootAssembly') -> '_6201.RootAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_specialised_assembly(self, design_entity: '_2039.SpecialisedAssembly') -> '_6205.SpecialisedAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_unbalanced_mass(self, design_entity: '_2040.UnbalancedMass') -> '_6236.UnbalancedMassLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_virtual_component(self, design_entity: '_2041.VirtualComponent') -> '_6237.VirtualComponentLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_shaft(self, design_entity: '_2044.Shaft') -> '_6203.ShaftLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_concept_gear(self, design_entity: '_2082.ConceptGear') -> '_6104.ConceptGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_concept_gear_set(self, design_entity: '_2083.ConceptGearSet') -> '_6106.ConceptGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_face_gear(self, design_entity: '_2089.FaceGear') -> '_6142.FaceGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_face_gear_set(self, design_entity: '_2090.FaceGearSet') -> '_6144.FaceGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_agma_gleason_conical_gear(self, design_entity: '_2074.AGMAGleasonConicalGear') -> '_6078.AGMAGleasonConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_agma_gleason_conical_gear_set(self, design_entity: '_2075.AGMAGleasonConicalGearSet') -> '_6080.AGMAGleasonConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear(self, design_entity: '_2076.BevelDifferentialGear') -> '_6086.BevelDifferentialGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear_set(self, design_entity: '_2077.BevelDifferentialGearSet') -> '_6088.BevelDifferentialGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_differential_planet_gear(self, design_entity: '_2078.BevelDifferentialPlanetGear') -> '_6089.BevelDifferentialPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_differential_sun_gear(self, design_entity: '_2079.BevelDifferentialSunGear') -> '_6090.BevelDifferentialSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_gear(self, design_entity: '_2080.BevelGear') -> '_6091.BevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_gear_set(self, design_entity: '_2081.BevelGearSet') -> '_6093.BevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_conical_gear(self, design_entity: '_2084.ConicalGear') -> '_6107.ConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_conical_gear_set(self, design_entity: '_2085.ConicalGearSet') -> '_6111.ConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_cylindrical_gear(self, design_entity: '_2086.CylindricalGear') -> '_6120.CylindricalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_cylindrical_gear_set(self, design_entity: '_2087.CylindricalGearSet') -> '_6124.CylindricalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_cylindrical_planet_gear(self, design_entity: '_2088.CylindricalPlanetGear') -> '_6125.CylindricalPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_gear(self, design_entity: '_2091.Gear') -> '_6147.GearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_gear_set(self, design_entity: '_2093.GearSet') -> '_6152.GearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_hypoid_gear(self, design_entity: '_2095.HypoidGear') -> '_6162.HypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_hypoid_gear_set(self, design_entity: '_2096.HypoidGearSet') -> '_6164.HypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2097.KlingelnbergCycloPalloidConicalGear') -> '_6168.KlingelnbergCycloPalloidConicalGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2098.KlingelnbergCycloPalloidConicalGearSet') -> '_6170.KlingelnbergCycloPalloidConicalGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2099.KlingelnbergCycloPalloidHypoidGear') -> '_6171.KlingelnbergCycloPalloidHypoidGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2100.KlingelnbergCycloPalloidHypoidGearSet') -> '_6173.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2101.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6174.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2102.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6176.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_planetary_gear_set(self, design_entity: '_2103.PlanetaryGearSet') -> '_6189.PlanetaryGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear(self, design_entity: '_2104.SpiralBevelGear') -> '_6207.SpiralBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_spiral_bevel_gear_set(self, design_entity: '_2105.SpiralBevelGearSet') -> '_6209.SpiralBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear(self, design_entity: '_2106.StraightBevelDiffGear') -> '_6214.StraightBevelDiffGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear_set(self, design_entity: '_2107.StraightBevelDiffGearSet') -> '_6216.StraightBevelDiffGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear(self, design_entity: '_2108.StraightBevelGear') -> '_6217.StraightBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_gear_set(self, design_entity: '_2109.StraightBevelGearSet') -> '_6219.StraightBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_planet_gear(self, design_entity: '_2110.StraightBevelPlanetGear') -> '_6220.StraightBevelPlanetGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_sun_gear(self, design_entity: '_2111.StraightBevelSunGear') -> '_6221.StraightBevelSunGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_worm_gear(self, design_entity: '_2112.WormGear') -> '_6238.WormGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_worm_gear_set(self, design_entity: '_2113.WormGearSet') -> '_6240.WormGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear(self, design_entity: '_2114.ZerolBevelGear') -> '_6241.ZerolBevelGearLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_zerol_bevel_gear_set(self, design_entity: '_2115.ZerolBevelGearSet') -> '_6243.ZerolBevelGearSetLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling(self, design_entity: '_2144.PartToPartShearCoupling') -> '_6187.PartToPartShearCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_part_to_part_shear_coupling_half(self, design_entity: '_2145.PartToPartShearCouplingHalf') -> '_6186.PartToPartShearCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_belt_drive(self, design_entity: '_2133.BeltDrive') -> '_6085.BeltDriveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_clutch(self, design_entity: '_2135.Clutch') -> '_6098.ClutchLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_clutch_half(self, design_entity: '_2136.ClutchHalf') -> '_6097.ClutchHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_concept_coupling(self, design_entity: '_2138.ConceptCoupling') -> '_6103.ConceptCouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_concept_coupling_half(self, design_entity: '_2139.ConceptCouplingHalf') -> '_6102.ConceptCouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_coupling(self, design_entity: '_2140.Coupling') -> '_6116.CouplingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_coupling_half(self, design_entity: '_2141.CouplingHalf') -> '_6115.CouplingHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_cvt(self, design_entity: '_2142.CVT') -> '_6118.CVTLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_cvt_pulley(self, design_entity: '_2143.CVTPulley') -> '_6119.CVTPulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_pulley(self, design_entity: '_2146.Pulley') -> '_6196.PulleyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_shaft_hub_connection(self, design_entity: '_2154.ShaftHubConnection') -> '_6202.ShaftHubConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_rolling_ring(self, design_entity: '_2152.RollingRing') -> '_6200.RollingRingLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_rolling_ring_assembly(self, design_entity: '_2153.RollingRingAssembly') -> '_6198.RollingRingAssemblyLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_spring_damper(self, design_entity: '_2155.SpringDamper') -> '_6212.SpringDamperLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_spring_damper_half(self, design_entity: '_2156.SpringDamperHalf') -> '_6211.SpringDamperHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_synchroniser(self, design_entity: '_2157.Synchroniser') -> '_6223.SynchroniserLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_synchroniser_half(self, design_entity: '_2159.SynchroniserHalf') -> '_6222.SynchroniserHalfLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_synchroniser_part(self, design_entity: '_2160.SynchroniserPart') -> '_6224.SynchroniserPartLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_synchroniser_sleeve(self, design_entity: '_2161.SynchroniserSleeve') -> '_6225.SynchroniserSleeveLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_torque_converter(self, design_entity: '_2162.TorqueConverter') -> '_6229.TorqueConverterLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_torque_converter_pump(self, design_entity: '_2163.TorqueConverterPump') -> '_6230.TorqueConverterPumpLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_torque_converter_turbine(self, design_entity: '_2165.TorqueConverterTurbine') -> '_6231.TorqueConverterTurbineLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_cvt_belt_connection(self, design_entity: '_1856.CVTBeltConnection') -> '_6117.CVTBeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_belt_connection(self, design_entity: '_1851.BeltConnection') -> '_6084.BeltConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_coaxial_connection(self, design_entity: '_1852.CoaxialConnection') -> '_6099.CoaxialConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_connection(self, design_entity: '_1855.Connection') -> '_6112.ConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_inter_mountable_component_connection(self, design_entity: '_1864.InterMountableComponentConnection') -> '_6167.InterMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_planetary_connection(self, design_entity: '_1867.PlanetaryConnection') -> '_6188.PlanetaryConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_rolling_ring_connection(self, design_entity: '_1871.RollingRingConnection') -> '_6199.RollingRingConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_shaft_to_mountable_component_connection(self, design_entity: '_1875.ShaftToMountableComponentConnection') -> '_6204.ShaftToMountableComponentConnectionLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_differential_gear_mesh(self, design_entity: '_1881.BevelDifferentialGearMesh') -> '_6087.BevelDifferentialGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_concept_gear_mesh(self, design_entity: '_1885.ConceptGearMesh') -> '_6105.ConceptGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_face_gear_mesh(self, design_entity: '_1891.FaceGearMesh') -> '_6143.FaceGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1905.StraightBevelDiffGearMesh') -> '_6215.StraightBevelDiffGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_bevel_gear_mesh(self, design_entity: '_1883.BevelGearMesh') -> '_6092.BevelGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def inputs_for_conical_gear_mesh(self, design_entity: '_1887.ConicalGearMesh') -> '_6109.ConicalGearMeshLoadCase':
        ''' 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase
        '''

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
