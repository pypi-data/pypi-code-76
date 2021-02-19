'''_5740.py

AssemblyCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2037, _2074
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5324
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import (
    _5741, _5743, _5746, _5752,
    _5753, _5754, _5759, _5764,
    _5774, _5778, _5784, _5785,
    _5792, _5793, _5800, _5803,
    _5804, _5805, _5807, _5809,
    _5814, _5815, _5816, _5823,
    _5818, _5822, _5828, _5829,
    _5834, _5837, _5840, _5844,
    _5848, _5852, _5855, _5735
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'AssemblyCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundGearWhineAnalysis',)


class AssemblyCompoundGearWhineAnalysis(_5735.AbstractAssemblyCompoundGearWhineAnalysis):
    '''AssemblyCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2037.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2037.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5324.AssemblyGearWhineAnalysis]':
        '''List[AssemblyGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5324.AssemblyGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5324.AssemblyGearWhineAnalysis]':
        '''List[AssemblyGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5324.AssemblyGearWhineAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5741.BearingCompoundGearWhineAnalysis]':
        '''List[BearingCompoundGearWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5741.BearingCompoundGearWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5743.BeltDriveCompoundGearWhineAnalysis]':
        '''List[BeltDriveCompoundGearWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5743.BeltDriveCompoundGearWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5746.BevelDifferentialGearSetCompoundGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetCompoundGearWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5746.BevelDifferentialGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5752.BoltCompoundGearWhineAnalysis]':
        '''List[BoltCompoundGearWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5752.BoltCompoundGearWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5753.BoltedJointCompoundGearWhineAnalysis]':
        '''List[BoltedJointCompoundGearWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5753.BoltedJointCompoundGearWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5754.ClutchCompoundGearWhineAnalysis]':
        '''List[ClutchCompoundGearWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5754.ClutchCompoundGearWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5759.ConceptCouplingCompoundGearWhineAnalysis]':
        '''List[ConceptCouplingCompoundGearWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5759.ConceptCouplingCompoundGearWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5764.ConceptGearSetCompoundGearWhineAnalysis]':
        '''List[ConceptGearSetCompoundGearWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5764.ConceptGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5774.CVTCompoundGearWhineAnalysis]':
        '''List[CVTCompoundGearWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5774.CVTCompoundGearWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5778.CylindricalGearSetCompoundGearWhineAnalysis]':
        '''List[CylindricalGearSetCompoundGearWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5778.CylindricalGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5784.FaceGearSetCompoundGearWhineAnalysis]':
        '''List[FaceGearSetCompoundGearWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5784.FaceGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5785.FlexiblePinAssemblyCompoundGearWhineAnalysis]':
        '''List[FlexiblePinAssemblyCompoundGearWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5785.FlexiblePinAssemblyCompoundGearWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5792.HypoidGearSetCompoundGearWhineAnalysis]':
        '''List[HypoidGearSetCompoundGearWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5792.HypoidGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5793.ImportedFEComponentCompoundGearWhineAnalysis]':
        '''List[ImportedFEComponentCompoundGearWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5793.ImportedFEComponentCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5800.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5800.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5803.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5803.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5804.MassDiscCompoundGearWhineAnalysis]':
        '''List[MassDiscCompoundGearWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5804.MassDiscCompoundGearWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5805.MeasurementComponentCompoundGearWhineAnalysis]':
        '''List[MeasurementComponentCompoundGearWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5805.MeasurementComponentCompoundGearWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5807.OilSealCompoundGearWhineAnalysis]':
        '''List[OilSealCompoundGearWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5807.OilSealCompoundGearWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5809.PartToPartShearCouplingCompoundGearWhineAnalysis]':
        '''List[PartToPartShearCouplingCompoundGearWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5809.PartToPartShearCouplingCompoundGearWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5814.PlanetCarrierCompoundGearWhineAnalysis]':
        '''List[PlanetCarrierCompoundGearWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5814.PlanetCarrierCompoundGearWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5815.PointLoadCompoundGearWhineAnalysis]':
        '''List[PointLoadCompoundGearWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5815.PointLoadCompoundGearWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5816.PowerLoadCompoundGearWhineAnalysis]':
        '''List[PowerLoadCompoundGearWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5816.PowerLoadCompoundGearWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5823.ShaftHubConnectionCompoundGearWhineAnalysis]':
        '''List[ShaftHubConnectionCompoundGearWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5823.ShaftHubConnectionCompoundGearWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5818.RollingRingAssemblyCompoundGearWhineAnalysis]':
        '''List[RollingRingAssemblyCompoundGearWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5818.RollingRingAssemblyCompoundGearWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5822.ShaftCompoundGearWhineAnalysis]':
        '''List[ShaftCompoundGearWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5822.ShaftCompoundGearWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5828.SpiralBevelGearSetCompoundGearWhineAnalysis]':
        '''List[SpiralBevelGearSetCompoundGearWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5828.SpiralBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5829.SpringDamperCompoundGearWhineAnalysis]':
        '''List[SpringDamperCompoundGearWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5829.SpringDamperCompoundGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5834.StraightBevelDiffGearSetCompoundGearWhineAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundGearWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5834.StraightBevelDiffGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5837.StraightBevelGearSetCompoundGearWhineAnalysis]':
        '''List[StraightBevelGearSetCompoundGearWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5837.StraightBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5840.SynchroniserCompoundGearWhineAnalysis]':
        '''List[SynchroniserCompoundGearWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5840.SynchroniserCompoundGearWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5844.TorqueConverterCompoundGearWhineAnalysis]':
        '''List[TorqueConverterCompoundGearWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5844.TorqueConverterCompoundGearWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5848.UnbalancedMassCompoundGearWhineAnalysis]':
        '''List[UnbalancedMassCompoundGearWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5848.UnbalancedMassCompoundGearWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5852.WormGearSetCompoundGearWhineAnalysis]':
        '''List[WormGearSetCompoundGearWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5852.WormGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5855.ZerolBevelGearSetCompoundGearWhineAnalysis]':
        '''List[ZerolBevelGearSetCompoundGearWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5855.ZerolBevelGearSetCompoundGearWhineAnalysis))
        return value
