'''_6315.py

AssemblyCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2108, _2147
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6184
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6316, _6318, _6321, _6327,
    _6328, _6329, _6334, _6339,
    _6349, _6351, _6353, _6357,
    _6363, _6364, _6365, _6372,
    _6379, _6382, _6383, _6384,
    _6386, _6388, _6393, _6394,
    _6395, _6404, _6397, _6399,
    _6403, _6409, _6410, _6415,
    _6418, _6421, _6425, _6429,
    _6433, _6436, _6308
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'AssemblyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundCriticalSpeedAnalysis',)


class AssemblyCompoundCriticalSpeedAnalysis(_6308.AbstractAssemblyCompoundCriticalSpeedAnalysis):
    '''AssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundCriticalSpeedAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6184.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6184.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6184.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6184.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_6316.BearingCompoundCriticalSpeedAnalysis]':
        '''List[BearingCompoundCriticalSpeedAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6316.BearingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_6318.BeltDriveCompoundCriticalSpeedAnalysis]':
        '''List[BeltDriveCompoundCriticalSpeedAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6318.BeltDriveCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6321.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6321.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_6327.BoltCompoundCriticalSpeedAnalysis]':
        '''List[BoltCompoundCriticalSpeedAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6327.BoltCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_6328.BoltedJointCompoundCriticalSpeedAnalysis]':
        '''List[BoltedJointCompoundCriticalSpeedAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6328.BoltedJointCompoundCriticalSpeedAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_6329.ClutchCompoundCriticalSpeedAnalysis]':
        '''List[ClutchCompoundCriticalSpeedAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6329.ClutchCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_6334.ConceptCouplingCompoundCriticalSpeedAnalysis]':
        '''List[ConceptCouplingCompoundCriticalSpeedAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6334.ConceptCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6339.ConceptGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCompoundCriticalSpeedAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6339.ConceptGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6349.CVTCompoundCriticalSpeedAnalysis]':
        '''List[CVTCompoundCriticalSpeedAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6349.CVTCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6351.CycloidalAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalAssemblyCompoundCriticalSpeedAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6351.CycloidalAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6353.CycloidalDiscCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCompoundCriticalSpeedAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6353.CycloidalDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6357.CylindricalGearSetCompoundCriticalSpeedAnalysis]':
        '''List[CylindricalGearSetCompoundCriticalSpeedAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6357.CylindricalGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6363.FaceGearSetCompoundCriticalSpeedAnalysis]':
        '''List[FaceGearSetCompoundCriticalSpeedAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6363.FaceGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6364.FEPartCompoundCriticalSpeedAnalysis]':
        '''List[FEPartCompoundCriticalSpeedAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6364.FEPartCompoundCriticalSpeedAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6365.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6365.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6372.HypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCompoundCriticalSpeedAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6372.HypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6379.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6379.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6382.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6382.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6383.MassDiscCompoundCriticalSpeedAnalysis]':
        '''List[MassDiscCompoundCriticalSpeedAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6383.MassDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6384.MeasurementComponentCompoundCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCompoundCriticalSpeedAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6384.MeasurementComponentCompoundCriticalSpeedAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6386.OilSealCompoundCriticalSpeedAnalysis]':
        '''List[OilSealCompoundCriticalSpeedAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6386.OilSealCompoundCriticalSpeedAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6388.PartToPartShearCouplingCompoundCriticalSpeedAnalysis]':
        '''List[PartToPartShearCouplingCompoundCriticalSpeedAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6388.PartToPartShearCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6393.PlanetCarrierCompoundCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCompoundCriticalSpeedAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6393.PlanetCarrierCompoundCriticalSpeedAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6394.PointLoadCompoundCriticalSpeedAnalysis]':
        '''List[PointLoadCompoundCriticalSpeedAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6394.PointLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6395.PowerLoadCompoundCriticalSpeedAnalysis]':
        '''List[PowerLoadCompoundCriticalSpeedAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6395.PowerLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6404.ShaftHubConnectionCompoundCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCompoundCriticalSpeedAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6404.ShaftHubConnectionCompoundCriticalSpeedAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6397.RingPinsCompoundCriticalSpeedAnalysis]':
        '''List[RingPinsCompoundCriticalSpeedAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6397.RingPinsCompoundCriticalSpeedAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6399.RollingRingAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[RollingRingAssemblyCompoundCriticalSpeedAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6399.RollingRingAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6403.ShaftCompoundCriticalSpeedAnalysis]':
        '''List[ShaftCompoundCriticalSpeedAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6403.ShaftCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6409.SpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6409.SpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6410.SpringDamperCompoundCriticalSpeedAnalysis]':
        '''List[SpringDamperCompoundCriticalSpeedAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6410.SpringDamperCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6415.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6415.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6418.StraightBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6418.StraightBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6421.SynchroniserCompoundCriticalSpeedAnalysis]':
        '''List[SynchroniserCompoundCriticalSpeedAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6421.SynchroniserCompoundCriticalSpeedAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6425.TorqueConverterCompoundCriticalSpeedAnalysis]':
        '''List[TorqueConverterCompoundCriticalSpeedAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6425.TorqueConverterCompoundCriticalSpeedAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6429.UnbalancedMassCompoundCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCompoundCriticalSpeedAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6429.UnbalancedMassCompoundCriticalSpeedAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6433.WormGearSetCompoundCriticalSpeedAnalysis]':
        '''List[WormGearSetCompoundCriticalSpeedAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6433.WormGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6436.ZerolBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCompoundCriticalSpeedAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6436.ZerolBevelGearSetCompoundCriticalSpeedAnalysis))
        return value
