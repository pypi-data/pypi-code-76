'''_5586.py

AssemblyCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2021, _2058
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5463
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import (
    _5587, _5589, _5592, _5598,
    _5599, _5600, _5605, _5610,
    _5620, _5624, _5630, _5631,
    _5638, _5639, _5646, _5649,
    _5650, _5651, _5653, _5655,
    _5660, _5661, _5662, _5669,
    _5664, _5668, _5674, _5675,
    _5680, _5683, _5686, _5690,
    _5694, _5698, _5701, _5581
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'AssemblyCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSingleMeshWhineAnalysis',)


class AssemblyCompoundSingleMeshWhineAnalysis(_5581.AbstractAssemblyCompoundSingleMeshWhineAnalysis):
    '''AssemblyCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2021.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2021.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5463.AssemblySingleMeshWhineAnalysis]':
        '''List[AssemblySingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5463.AssemblySingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_5463.AssemblySingleMeshWhineAnalysis]':
        '''List[AssemblySingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_5463.AssemblySingleMeshWhineAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5587.BearingCompoundSingleMeshWhineAnalysis]':
        '''List[BearingCompoundSingleMeshWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5587.BearingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5589.BeltDriveCompoundSingleMeshWhineAnalysis]':
        '''List[BeltDriveCompoundSingleMeshWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5589.BeltDriveCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5592.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5592.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5598.BoltCompoundSingleMeshWhineAnalysis]':
        '''List[BoltCompoundSingleMeshWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5598.BoltCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5599.BoltedJointCompoundSingleMeshWhineAnalysis]':
        '''List[BoltedJointCompoundSingleMeshWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5599.BoltedJointCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5600.ClutchCompoundSingleMeshWhineAnalysis]':
        '''List[ClutchCompoundSingleMeshWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5600.ClutchCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5605.ConceptCouplingCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptCouplingCompoundSingleMeshWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5605.ConceptCouplingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5610.ConceptGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptGearSetCompoundSingleMeshWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5610.ConceptGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5620.CVTCompoundSingleMeshWhineAnalysis]':
        '''List[CVTCompoundSingleMeshWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5620.CVTCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5624.CylindricalGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[CylindricalGearSetCompoundSingleMeshWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5624.CylindricalGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5630.FaceGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[FaceGearSetCompoundSingleMeshWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5630.FaceGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5631.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]':
        '''List[FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5631.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5638.HypoidGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[HypoidGearSetCompoundSingleMeshWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5638.HypoidGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5639.ImportedFEComponentCompoundSingleMeshWhineAnalysis]':
        '''List[ImportedFEComponentCompoundSingleMeshWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5639.ImportedFEComponentCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5646.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5646.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5649.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5649.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5650.MassDiscCompoundSingleMeshWhineAnalysis]':
        '''List[MassDiscCompoundSingleMeshWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5650.MassDiscCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5651.MeasurementComponentCompoundSingleMeshWhineAnalysis]':
        '''List[MeasurementComponentCompoundSingleMeshWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5651.MeasurementComponentCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5653.OilSealCompoundSingleMeshWhineAnalysis]':
        '''List[OilSealCompoundSingleMeshWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5653.OilSealCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5655.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]':
        '''List[PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5655.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5660.PlanetCarrierCompoundSingleMeshWhineAnalysis]':
        '''List[PlanetCarrierCompoundSingleMeshWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5660.PlanetCarrierCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5661.PointLoadCompoundSingleMeshWhineAnalysis]':
        '''List[PointLoadCompoundSingleMeshWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5661.PointLoadCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5662.PowerLoadCompoundSingleMeshWhineAnalysis]':
        '''List[PowerLoadCompoundSingleMeshWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5662.PowerLoadCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5669.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionCompoundSingleMeshWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5669.ShaftHubConnectionCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5664.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]':
        '''List[RollingRingAssemblyCompoundSingleMeshWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5664.RollingRingAssemblyCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5668.ShaftCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftCompoundSingleMeshWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5668.ShaftCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5674.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5674.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5675.SpringDamperCompoundSingleMeshWhineAnalysis]':
        '''List[SpringDamperCompoundSingleMeshWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5675.SpringDamperCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5680.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5680.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5683.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[StraightBevelGearSetCompoundSingleMeshWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5683.StraightBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5686.SynchroniserCompoundSingleMeshWhineAnalysis]':
        '''List[SynchroniserCompoundSingleMeshWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5686.SynchroniserCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5690.TorqueConverterCompoundSingleMeshWhineAnalysis]':
        '''List[TorqueConverterCompoundSingleMeshWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5690.TorqueConverterCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5694.UnbalancedMassCompoundSingleMeshWhineAnalysis]':
        '''List[UnbalancedMassCompoundSingleMeshWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5694.UnbalancedMassCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5698.WormGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[WormGearSetCompoundSingleMeshWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5698.WormGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5701.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5701.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value
