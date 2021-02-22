'''_3535.py

AssemblyCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2083, _2122
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _3403
from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
    _3536, _3538, _3541, _3547,
    _3548, _3549, _3554, _3559,
    _3569, _3571, _3573, _3577,
    _3583, _3584, _3585, _3592,
    _3599, _3602, _3603, _3604,
    _3606, _3608, _3613, _3614,
    _3615, _3624, _3617, _3619,
    _3623, _3629, _3630, _3635,
    _3638, _3641, _3645, _3649,
    _3653, _3656, _3528
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'AssemblyCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundStabilityAnalysis',)


class AssemblyCompoundStabilityAnalysis(_3528.AbstractAssemblyCompoundStabilityAnalysis):
    '''AssemblyCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundStabilityAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3403.AssemblyStabilityAnalysis]':
        '''List[AssemblyStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3403.AssemblyStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3403.AssemblyStabilityAnalysis]':
        '''List[AssemblyStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3403.AssemblyStabilityAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_3536.BearingCompoundStabilityAnalysis]':
        '''List[BearingCompoundStabilityAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3536.BearingCompoundStabilityAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_3538.BeltDriveCompoundStabilityAnalysis]':
        '''List[BeltDriveCompoundStabilityAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3538.BeltDriveCompoundStabilityAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3541.BevelDifferentialGearSetCompoundStabilityAnalysis]':
        '''List[BevelDifferentialGearSetCompoundStabilityAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3541.BevelDifferentialGearSetCompoundStabilityAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_3547.BoltCompoundStabilityAnalysis]':
        '''List[BoltCompoundStabilityAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3547.BoltCompoundStabilityAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_3548.BoltedJointCompoundStabilityAnalysis]':
        '''List[BoltedJointCompoundStabilityAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3548.BoltedJointCompoundStabilityAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_3549.ClutchCompoundStabilityAnalysis]':
        '''List[ClutchCompoundStabilityAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3549.ClutchCompoundStabilityAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_3554.ConceptCouplingCompoundStabilityAnalysis]':
        '''List[ConceptCouplingCompoundStabilityAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3554.ConceptCouplingCompoundStabilityAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3559.ConceptGearSetCompoundStabilityAnalysis]':
        '''List[ConceptGearSetCompoundStabilityAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3559.ConceptGearSetCompoundStabilityAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_3569.CVTCompoundStabilityAnalysis]':
        '''List[CVTCompoundStabilityAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3569.CVTCompoundStabilityAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3571.CycloidalAssemblyCompoundStabilityAnalysis]':
        '''List[CycloidalAssemblyCompoundStabilityAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3571.CycloidalAssemblyCompoundStabilityAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3573.CycloidalDiscCompoundStabilityAnalysis]':
        '''List[CycloidalDiscCompoundStabilityAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3573.CycloidalDiscCompoundStabilityAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3577.CylindricalGearSetCompoundStabilityAnalysis]':
        '''List[CylindricalGearSetCompoundStabilityAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3577.CylindricalGearSetCompoundStabilityAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3583.FaceGearSetCompoundStabilityAnalysis]':
        '''List[FaceGearSetCompoundStabilityAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3583.FaceGearSetCompoundStabilityAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_3584.FEPartCompoundStabilityAnalysis]':
        '''List[FEPartCompoundStabilityAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3584.FEPartCompoundStabilityAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3585.FlexiblePinAssemblyCompoundStabilityAnalysis]':
        '''List[FlexiblePinAssemblyCompoundStabilityAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3585.FlexiblePinAssemblyCompoundStabilityAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3592.HypoidGearSetCompoundStabilityAnalysis]':
        '''List[HypoidGearSetCompoundStabilityAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3592.HypoidGearSetCompoundStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3599.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3599.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3602.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_3603.MassDiscCompoundStabilityAnalysis]':
        '''List[MassDiscCompoundStabilityAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3603.MassDiscCompoundStabilityAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_3604.MeasurementComponentCompoundStabilityAnalysis]':
        '''List[MeasurementComponentCompoundStabilityAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3604.MeasurementComponentCompoundStabilityAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_3606.OilSealCompoundStabilityAnalysis]':
        '''List[OilSealCompoundStabilityAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3606.OilSealCompoundStabilityAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3608.PartToPartShearCouplingCompoundStabilityAnalysis]':
        '''List[PartToPartShearCouplingCompoundStabilityAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3608.PartToPartShearCouplingCompoundStabilityAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_3613.PlanetCarrierCompoundStabilityAnalysis]':
        '''List[PlanetCarrierCompoundStabilityAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3613.PlanetCarrierCompoundStabilityAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_3614.PointLoadCompoundStabilityAnalysis]':
        '''List[PointLoadCompoundStabilityAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3614.PointLoadCompoundStabilityAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_3615.PowerLoadCompoundStabilityAnalysis]':
        '''List[PowerLoadCompoundStabilityAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3615.PowerLoadCompoundStabilityAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3624.ShaftHubConnectionCompoundStabilityAnalysis]':
        '''List[ShaftHubConnectionCompoundStabilityAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3624.ShaftHubConnectionCompoundStabilityAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_3617.RingPinsCompoundStabilityAnalysis]':
        '''List[RingPinsCompoundStabilityAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3617.RingPinsCompoundStabilityAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3619.RollingRingAssemblyCompoundStabilityAnalysis]':
        '''List[RollingRingAssemblyCompoundStabilityAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3619.RollingRingAssemblyCompoundStabilityAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_3623.ShaftCompoundStabilityAnalysis]':
        '''List[ShaftCompoundStabilityAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3623.ShaftCompoundStabilityAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3629.SpiralBevelGearSetCompoundStabilityAnalysis]':
        '''List[SpiralBevelGearSetCompoundStabilityAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3629.SpiralBevelGearSetCompoundStabilityAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_3630.SpringDamperCompoundStabilityAnalysis]':
        '''List[SpringDamperCompoundStabilityAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3630.SpringDamperCompoundStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3635.StraightBevelDiffGearSetCompoundStabilityAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundStabilityAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3635.StraightBevelDiffGearSetCompoundStabilityAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3638.StraightBevelGearSetCompoundStabilityAnalysis]':
        '''List[StraightBevelGearSetCompoundStabilityAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3638.StraightBevelGearSetCompoundStabilityAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_3641.SynchroniserCompoundStabilityAnalysis]':
        '''List[SynchroniserCompoundStabilityAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3641.SynchroniserCompoundStabilityAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_3645.TorqueConverterCompoundStabilityAnalysis]':
        '''List[TorqueConverterCompoundStabilityAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3645.TorqueConverterCompoundStabilityAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3649.UnbalancedMassCompoundStabilityAnalysis]':
        '''List[UnbalancedMassCompoundStabilityAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3649.UnbalancedMassCompoundStabilityAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3653.WormGearSetCompoundStabilityAnalysis]':
        '''List[WormGearSetCompoundStabilityAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3653.WormGearSetCompoundStabilityAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3656.ZerolBevelGearSetCompoundStabilityAnalysis]':
        '''List[ZerolBevelGearSetCompoundStabilityAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3656.ZerolBevelGearSetCompoundStabilityAnalysis))
        return value
