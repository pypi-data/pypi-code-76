'''_5565.py

AssemblyCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2000, _2037
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5442
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import (
    _5566, _5568, _5571, _5577,
    _5578, _5579, _5584, _5589,
    _5599, _5603, _5609, _5610,
    _5617, _5618, _5625, _5628,
    _5629, _5630, _5632, _5634,
    _5639, _5640, _5641, _5648,
    _5643, _5647, _5653, _5654,
    _5659, _5662, _5665, _5669,
    _5673, _5677, _5680, _5560
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'AssemblyCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSingleMeshWhineAnalysis',)


class AssemblyCompoundSingleMeshWhineAnalysis(_5560.AbstractAssemblyCompoundSingleMeshWhineAnalysis):
    '''AssemblyCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2000.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2000.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5442.AssemblySingleMeshWhineAnalysis]':
        '''List[AssemblySingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5442.AssemblySingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_5442.AssemblySingleMeshWhineAnalysis]':
        '''List[AssemblySingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_5442.AssemblySingleMeshWhineAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5566.BearingCompoundSingleMeshWhineAnalysis]':
        '''List[BearingCompoundSingleMeshWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5566.BearingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5568.BeltDriveCompoundSingleMeshWhineAnalysis]':
        '''List[BeltDriveCompoundSingleMeshWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5568.BeltDriveCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5571.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5571.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5577.BoltCompoundSingleMeshWhineAnalysis]':
        '''List[BoltCompoundSingleMeshWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5577.BoltCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5578.BoltedJointCompoundSingleMeshWhineAnalysis]':
        '''List[BoltedJointCompoundSingleMeshWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5578.BoltedJointCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5579.ClutchCompoundSingleMeshWhineAnalysis]':
        '''List[ClutchCompoundSingleMeshWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5579.ClutchCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5584.ConceptCouplingCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptCouplingCompoundSingleMeshWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5584.ConceptCouplingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5589.ConceptGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptGearSetCompoundSingleMeshWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5589.ConceptGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5599.CVTCompoundSingleMeshWhineAnalysis]':
        '''List[CVTCompoundSingleMeshWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5599.CVTCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5603.CylindricalGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[CylindricalGearSetCompoundSingleMeshWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5603.CylindricalGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5609.FaceGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[FaceGearSetCompoundSingleMeshWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5609.FaceGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5610.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]':
        '''List[FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5610.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5617.HypoidGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[HypoidGearSetCompoundSingleMeshWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5617.HypoidGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5618.ImportedFEComponentCompoundSingleMeshWhineAnalysis]':
        '''List[ImportedFEComponentCompoundSingleMeshWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5618.ImportedFEComponentCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5625.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5625.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5628.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5628.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5629.MassDiscCompoundSingleMeshWhineAnalysis]':
        '''List[MassDiscCompoundSingleMeshWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5629.MassDiscCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5630.MeasurementComponentCompoundSingleMeshWhineAnalysis]':
        '''List[MeasurementComponentCompoundSingleMeshWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5630.MeasurementComponentCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5632.OilSealCompoundSingleMeshWhineAnalysis]':
        '''List[OilSealCompoundSingleMeshWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5632.OilSealCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5634.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]':
        '''List[PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5634.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5639.PlanetCarrierCompoundSingleMeshWhineAnalysis]':
        '''List[PlanetCarrierCompoundSingleMeshWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5639.PlanetCarrierCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5640.PointLoadCompoundSingleMeshWhineAnalysis]':
        '''List[PointLoadCompoundSingleMeshWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5640.PointLoadCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5641.PowerLoadCompoundSingleMeshWhineAnalysis]':
        '''List[PowerLoadCompoundSingleMeshWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5641.PowerLoadCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5648.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionCompoundSingleMeshWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5648.ShaftHubConnectionCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5643.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]':
        '''List[RollingRingAssemblyCompoundSingleMeshWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5643.RollingRingAssemblyCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5647.ShaftCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftCompoundSingleMeshWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5647.ShaftCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5653.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5653.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5654.SpringDamperCompoundSingleMeshWhineAnalysis]':
        '''List[SpringDamperCompoundSingleMeshWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5654.SpringDamperCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5659.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5659.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5662.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[StraightBevelGearSetCompoundSingleMeshWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5662.StraightBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5665.SynchroniserCompoundSingleMeshWhineAnalysis]':
        '''List[SynchroniserCompoundSingleMeshWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5665.SynchroniserCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5669.TorqueConverterCompoundSingleMeshWhineAnalysis]':
        '''List[TorqueConverterCompoundSingleMeshWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5669.TorqueConverterCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5673.UnbalancedMassCompoundSingleMeshWhineAnalysis]':
        '''List[UnbalancedMassCompoundSingleMeshWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5673.UnbalancedMassCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5677.WormGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[WormGearSetCompoundSingleMeshWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5677.WormGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5680.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5680.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value
