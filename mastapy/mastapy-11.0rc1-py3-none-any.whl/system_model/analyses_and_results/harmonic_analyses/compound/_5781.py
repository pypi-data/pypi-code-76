'''_5781.py

AssemblyCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2108, _2147
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5597
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
    _5782, _5784, _5787, _5793,
    _5794, _5795, _5800, _5805,
    _5815, _5817, _5819, _5823,
    _5829, _5830, _5831, _5838,
    _5845, _5848, _5849, _5850,
    _5852, _5854, _5859, _5860,
    _5861, _5870, _5863, _5865,
    _5869, _5875, _5876, _5881,
    _5884, _5887, _5891, _5895,
    _5899, _5902, _5774
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'AssemblyCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundHarmonicAnalysis',)


class AssemblyCompoundHarmonicAnalysis(_5774.AbstractAssemblyCompoundHarmonicAnalysis):
    '''AssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2108.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2108.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2108.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2108.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5597.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5597.AssemblyHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5597.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5597.AssemblyHarmonicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5782.BearingCompoundHarmonicAnalysis]':
        '''List[BearingCompoundHarmonicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5782.BearingCompoundHarmonicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5784.BeltDriveCompoundHarmonicAnalysis]':
        '''List[BeltDriveCompoundHarmonicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5784.BeltDriveCompoundHarmonicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5787.BevelDifferentialGearSetCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundHarmonicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5787.BevelDifferentialGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5793.BoltCompoundHarmonicAnalysis]':
        '''List[BoltCompoundHarmonicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5793.BoltCompoundHarmonicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5794.BoltedJointCompoundHarmonicAnalysis]':
        '''List[BoltedJointCompoundHarmonicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5794.BoltedJointCompoundHarmonicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5795.ClutchCompoundHarmonicAnalysis]':
        '''List[ClutchCompoundHarmonicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5795.ClutchCompoundHarmonicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5800.ConceptCouplingCompoundHarmonicAnalysis]':
        '''List[ConceptCouplingCompoundHarmonicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5800.ConceptCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5805.ConceptGearSetCompoundHarmonicAnalysis]':
        '''List[ConceptGearSetCompoundHarmonicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5805.ConceptGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5815.CVTCompoundHarmonicAnalysis]':
        '''List[CVTCompoundHarmonicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5815.CVTCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5817.CycloidalAssemblyCompoundHarmonicAnalysis]':
        '''List[CycloidalAssemblyCompoundHarmonicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5817.CycloidalAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5819.CycloidalDiscCompoundHarmonicAnalysis]':
        '''List[CycloidalDiscCompoundHarmonicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5819.CycloidalDiscCompoundHarmonicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5823.CylindricalGearSetCompoundHarmonicAnalysis]':
        '''List[CylindricalGearSetCompoundHarmonicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5823.CylindricalGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5829.FaceGearSetCompoundHarmonicAnalysis]':
        '''List[FaceGearSetCompoundHarmonicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5829.FaceGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5830.FEPartCompoundHarmonicAnalysis]':
        '''List[FEPartCompoundHarmonicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5830.FEPartCompoundHarmonicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5831.FlexiblePinAssemblyCompoundHarmonicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundHarmonicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5831.FlexiblePinAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5838.HypoidGearSetCompoundHarmonicAnalysis]':
        '''List[HypoidGearSetCompoundHarmonicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5838.HypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5845.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5845.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5848.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5848.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5849.MassDiscCompoundHarmonicAnalysis]':
        '''List[MassDiscCompoundHarmonicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5849.MassDiscCompoundHarmonicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5850.MeasurementComponentCompoundHarmonicAnalysis]':
        '''List[MeasurementComponentCompoundHarmonicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5850.MeasurementComponentCompoundHarmonicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5852.OilSealCompoundHarmonicAnalysis]':
        '''List[OilSealCompoundHarmonicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5852.OilSealCompoundHarmonicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5854.PartToPartShearCouplingCompoundHarmonicAnalysis]':
        '''List[PartToPartShearCouplingCompoundHarmonicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5854.PartToPartShearCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5859.PlanetCarrierCompoundHarmonicAnalysis]':
        '''List[PlanetCarrierCompoundHarmonicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5859.PlanetCarrierCompoundHarmonicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5860.PointLoadCompoundHarmonicAnalysis]':
        '''List[PointLoadCompoundHarmonicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5860.PointLoadCompoundHarmonicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5861.PowerLoadCompoundHarmonicAnalysis]':
        '''List[PowerLoadCompoundHarmonicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5861.PowerLoadCompoundHarmonicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5870.ShaftHubConnectionCompoundHarmonicAnalysis]':
        '''List[ShaftHubConnectionCompoundHarmonicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5870.ShaftHubConnectionCompoundHarmonicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5863.RingPinsCompoundHarmonicAnalysis]':
        '''List[RingPinsCompoundHarmonicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5863.RingPinsCompoundHarmonicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5865.RollingRingAssemblyCompoundHarmonicAnalysis]':
        '''List[RollingRingAssemblyCompoundHarmonicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5865.RollingRingAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5869.ShaftCompoundHarmonicAnalysis]':
        '''List[ShaftCompoundHarmonicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5869.ShaftCompoundHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5875.SpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[SpiralBevelGearSetCompoundHarmonicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5875.SpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5876.SpringDamperCompoundHarmonicAnalysis]':
        '''List[SpringDamperCompoundHarmonicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5876.SpringDamperCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5881.StraightBevelDiffGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundHarmonicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5881.StraightBevelDiffGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5884.StraightBevelGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelGearSetCompoundHarmonicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5884.StraightBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5887.SynchroniserCompoundHarmonicAnalysis]':
        '''List[SynchroniserCompoundHarmonicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5887.SynchroniserCompoundHarmonicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5891.TorqueConverterCompoundHarmonicAnalysis]':
        '''List[TorqueConverterCompoundHarmonicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5891.TorqueConverterCompoundHarmonicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5895.UnbalancedMassCompoundHarmonicAnalysis]':
        '''List[UnbalancedMassCompoundHarmonicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5895.UnbalancedMassCompoundHarmonicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5899.WormGearSetCompoundHarmonicAnalysis]':
        '''List[WormGearSetCompoundHarmonicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5899.WormGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5902.ZerolBevelGearSetCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearSetCompoundHarmonicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5902.ZerolBevelGearSetCompoundHarmonicAnalysis))
        return value
