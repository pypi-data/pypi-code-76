'''_5159.py

AssemblyCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2083, _2122
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.mbd_analyses import _5008
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
    _5160, _5162, _5165, _5171,
    _5172, _5173, _5178, _5183,
    _5193, _5195, _5197, _5201,
    _5207, _5208, _5209, _5216,
    _5223, _5226, _5227, _5228,
    _5230, _5232, _5237, _5238,
    _5239, _5248, _5241, _5243,
    _5247, _5253, _5254, _5259,
    _5262, _5265, _5269, _5273,
    _5277, _5280, _5152
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'AssemblyCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundMultibodyDynamicsAnalysis',)


class AssemblyCompoundMultibodyDynamicsAnalysis(_5152.AbstractAssemblyCompoundMultibodyDynamicsAnalysis):
    '''AssemblyCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2083.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2083.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5008.AssemblyMultibodyDynamicsAnalysis]':
        '''List[AssemblyMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5008.AssemblyMultibodyDynamicsAnalysis))
        return value

    @property
    def assembly_multibody_dynamics_analysis_load_cases(self) -> 'List[_5008.AssemblyMultibodyDynamicsAnalysis]':
        '''List[AssemblyMultibodyDynamicsAnalysis]: 'AssemblyMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultibodyDynamicsAnalysisLoadCases, constructor.new(_5008.AssemblyMultibodyDynamicsAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5160.BearingCompoundMultibodyDynamicsAnalysis]':
        '''List[BearingCompoundMultibodyDynamicsAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5160.BearingCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5162.BeltDriveCompoundMultibodyDynamicsAnalysis]':
        '''List[BeltDriveCompoundMultibodyDynamicsAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5162.BeltDriveCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5165.BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5165.BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5171.BoltCompoundMultibodyDynamicsAnalysis]':
        '''List[BoltCompoundMultibodyDynamicsAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5171.BoltCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5172.BoltedJointCompoundMultibodyDynamicsAnalysis]':
        '''List[BoltedJointCompoundMultibodyDynamicsAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5172.BoltedJointCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5173.ClutchCompoundMultibodyDynamicsAnalysis]':
        '''List[ClutchCompoundMultibodyDynamicsAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5173.ClutchCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5178.ConceptCouplingCompoundMultibodyDynamicsAnalysis]':
        '''List[ConceptCouplingCompoundMultibodyDynamicsAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5178.ConceptCouplingCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5183.ConceptGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[ConceptGearSetCompoundMultibodyDynamicsAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5183.ConceptGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5193.CVTCompoundMultibodyDynamicsAnalysis]':
        '''List[CVTCompoundMultibodyDynamicsAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5193.CVTCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5195.CycloidalAssemblyCompoundMultibodyDynamicsAnalysis]':
        '''List[CycloidalAssemblyCompoundMultibodyDynamicsAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5195.CycloidalAssemblyCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5197.CycloidalDiscCompoundMultibodyDynamicsAnalysis]':
        '''List[CycloidalDiscCompoundMultibodyDynamicsAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5197.CycloidalDiscCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5201.CylindricalGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[CylindricalGearSetCompoundMultibodyDynamicsAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5201.CylindricalGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5207.FaceGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[FaceGearSetCompoundMultibodyDynamicsAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5207.FaceGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5208.FEPartCompoundMultibodyDynamicsAnalysis]':
        '''List[FEPartCompoundMultibodyDynamicsAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5208.FEPartCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5209.FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5209.FlexiblePinAssemblyCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5216.HypoidGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[HypoidGearSetCompoundMultibodyDynamicsAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5216.HypoidGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5223.KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5223.KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5226.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5226.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5227.MassDiscCompoundMultibodyDynamicsAnalysis]':
        '''List[MassDiscCompoundMultibodyDynamicsAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5227.MassDiscCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5228.MeasurementComponentCompoundMultibodyDynamicsAnalysis]':
        '''List[MeasurementComponentCompoundMultibodyDynamicsAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5228.MeasurementComponentCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5230.OilSealCompoundMultibodyDynamicsAnalysis]':
        '''List[OilSealCompoundMultibodyDynamicsAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5230.OilSealCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5232.PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis]':
        '''List[PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5232.PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5237.PlanetCarrierCompoundMultibodyDynamicsAnalysis]':
        '''List[PlanetCarrierCompoundMultibodyDynamicsAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5237.PlanetCarrierCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5238.PointLoadCompoundMultibodyDynamicsAnalysis]':
        '''List[PointLoadCompoundMultibodyDynamicsAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5238.PointLoadCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5239.PowerLoadCompoundMultibodyDynamicsAnalysis]':
        '''List[PowerLoadCompoundMultibodyDynamicsAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5239.PowerLoadCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5248.ShaftHubConnectionCompoundMultibodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionCompoundMultibodyDynamicsAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5248.ShaftHubConnectionCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5241.RingPinsCompoundMultibodyDynamicsAnalysis]':
        '''List[RingPinsCompoundMultibodyDynamicsAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5241.RingPinsCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5243.RollingRingAssemblyCompoundMultibodyDynamicsAnalysis]':
        '''List[RollingRingAssemblyCompoundMultibodyDynamicsAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5243.RollingRingAssemblyCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5247.ShaftCompoundMultibodyDynamicsAnalysis]':
        '''List[ShaftCompoundMultibodyDynamicsAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5247.ShaftCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5253.SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5253.SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5254.SpringDamperCompoundMultibodyDynamicsAnalysis]':
        '''List[SpringDamperCompoundMultibodyDynamicsAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5254.SpringDamperCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5259.StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5259.StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5262.StraightBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5262.StraightBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5265.SynchroniserCompoundMultibodyDynamicsAnalysis]':
        '''List[SynchroniserCompoundMultibodyDynamicsAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5265.SynchroniserCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5269.TorqueConverterCompoundMultibodyDynamicsAnalysis]':
        '''List[TorqueConverterCompoundMultibodyDynamicsAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5269.TorqueConverterCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5273.UnbalancedMassCompoundMultibodyDynamicsAnalysis]':
        '''List[UnbalancedMassCompoundMultibodyDynamicsAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5273.UnbalancedMassCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5277.WormGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[WormGearSetCompoundMultibodyDynamicsAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5277.WormGearSetCompoundMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5280.ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5280.ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis))
        return value
