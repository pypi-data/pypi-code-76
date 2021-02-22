'''_6282.py

AssemblyCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2083, _2122
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6151
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6283, _6285, _6288, _6294,
    _6295, _6296, _6301, _6306,
    _6316, _6318, _6320, _6324,
    _6330, _6331, _6332, _6339,
    _6346, _6349, _6350, _6351,
    _6353, _6355, _6360, _6361,
    _6362, _6371, _6364, _6366,
    _6370, _6376, _6377, _6382,
    _6385, _6388, _6392, _6396,
    _6400, _6403, _6275
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'AssemblyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundCriticalSpeedAnalysis',)


class AssemblyCompoundCriticalSpeedAnalysis(_6275.AbstractAssemblyCompoundCriticalSpeedAnalysis):
    '''AssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundCriticalSpeedAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6151.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6151.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6151.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6151.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_6283.BearingCompoundCriticalSpeedAnalysis]':
        '''List[BearingCompoundCriticalSpeedAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6283.BearingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_6285.BeltDriveCompoundCriticalSpeedAnalysis]':
        '''List[BeltDriveCompoundCriticalSpeedAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6285.BeltDriveCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6288.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6288.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_6294.BoltCompoundCriticalSpeedAnalysis]':
        '''List[BoltCompoundCriticalSpeedAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6294.BoltCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_6295.BoltedJointCompoundCriticalSpeedAnalysis]':
        '''List[BoltedJointCompoundCriticalSpeedAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6295.BoltedJointCompoundCriticalSpeedAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_6296.ClutchCompoundCriticalSpeedAnalysis]':
        '''List[ClutchCompoundCriticalSpeedAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6296.ClutchCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_6301.ConceptCouplingCompoundCriticalSpeedAnalysis]':
        '''List[ConceptCouplingCompoundCriticalSpeedAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6301.ConceptCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6306.ConceptGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCompoundCriticalSpeedAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6306.ConceptGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6316.CVTCompoundCriticalSpeedAnalysis]':
        '''List[CVTCompoundCriticalSpeedAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6316.CVTCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6318.CycloidalAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalAssemblyCompoundCriticalSpeedAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6318.CycloidalAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6320.CycloidalDiscCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCompoundCriticalSpeedAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6320.CycloidalDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6324.CylindricalGearSetCompoundCriticalSpeedAnalysis]':
        '''List[CylindricalGearSetCompoundCriticalSpeedAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6324.CylindricalGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6330.FaceGearSetCompoundCriticalSpeedAnalysis]':
        '''List[FaceGearSetCompoundCriticalSpeedAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6330.FaceGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6331.FEPartCompoundCriticalSpeedAnalysis]':
        '''List[FEPartCompoundCriticalSpeedAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6331.FEPartCompoundCriticalSpeedAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6332.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6332.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6339.HypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCompoundCriticalSpeedAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6339.HypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6346.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6346.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6349.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6349.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6350.MassDiscCompoundCriticalSpeedAnalysis]':
        '''List[MassDiscCompoundCriticalSpeedAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6350.MassDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6351.MeasurementComponentCompoundCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCompoundCriticalSpeedAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6351.MeasurementComponentCompoundCriticalSpeedAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6353.OilSealCompoundCriticalSpeedAnalysis]':
        '''List[OilSealCompoundCriticalSpeedAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6353.OilSealCompoundCriticalSpeedAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6355.PartToPartShearCouplingCompoundCriticalSpeedAnalysis]':
        '''List[PartToPartShearCouplingCompoundCriticalSpeedAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6355.PartToPartShearCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6360.PlanetCarrierCompoundCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCompoundCriticalSpeedAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6360.PlanetCarrierCompoundCriticalSpeedAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6361.PointLoadCompoundCriticalSpeedAnalysis]':
        '''List[PointLoadCompoundCriticalSpeedAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6361.PointLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6362.PowerLoadCompoundCriticalSpeedAnalysis]':
        '''List[PowerLoadCompoundCriticalSpeedAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6362.PowerLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6371.ShaftHubConnectionCompoundCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCompoundCriticalSpeedAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6371.ShaftHubConnectionCompoundCriticalSpeedAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6364.RingPinsCompoundCriticalSpeedAnalysis]':
        '''List[RingPinsCompoundCriticalSpeedAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6364.RingPinsCompoundCriticalSpeedAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6366.RollingRingAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[RollingRingAssemblyCompoundCriticalSpeedAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6366.RollingRingAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6370.ShaftCompoundCriticalSpeedAnalysis]':
        '''List[ShaftCompoundCriticalSpeedAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6370.ShaftCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6376.SpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6376.SpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6377.SpringDamperCompoundCriticalSpeedAnalysis]':
        '''List[SpringDamperCompoundCriticalSpeedAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6377.SpringDamperCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6382.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6382.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6385.StraightBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6385.StraightBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6388.SynchroniserCompoundCriticalSpeedAnalysis]':
        '''List[SynchroniserCompoundCriticalSpeedAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6388.SynchroniserCompoundCriticalSpeedAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6392.TorqueConverterCompoundCriticalSpeedAnalysis]':
        '''List[TorqueConverterCompoundCriticalSpeedAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6392.TorqueConverterCompoundCriticalSpeedAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6396.UnbalancedMassCompoundCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCompoundCriticalSpeedAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6396.UnbalancedMassCompoundCriticalSpeedAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6400.WormGearSetCompoundCriticalSpeedAnalysis]':
        '''List[WormGearSetCompoundCriticalSpeedAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6400.WormGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6403.ZerolBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCompoundCriticalSpeedAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6403.ZerolBevelGearSetCompoundCriticalSpeedAnalysis))
        return value
