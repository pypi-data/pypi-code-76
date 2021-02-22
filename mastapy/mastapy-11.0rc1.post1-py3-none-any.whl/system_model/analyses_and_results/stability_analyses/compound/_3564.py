'''_3564.py

AssemblyCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2108, _2147
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _3432
from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
    _3565, _3567, _3570, _3576,
    _3577, _3578, _3583, _3588,
    _3598, _3600, _3602, _3606,
    _3612, _3613, _3614, _3621,
    _3628, _3631, _3632, _3633,
    _3635, _3637, _3642, _3643,
    _3644, _3653, _3646, _3648,
    _3652, _3658, _3659, _3664,
    _3667, _3670, _3674, _3678,
    _3682, _3685, _3557
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'AssemblyCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundStabilityAnalysis',)


class AssemblyCompoundStabilityAnalysis(_3557.AbstractAssemblyCompoundStabilityAnalysis):
    '''AssemblyCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundStabilityAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3432.AssemblyStabilityAnalysis]':
        '''List[AssemblyStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3432.AssemblyStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3432.AssemblyStabilityAnalysis]':
        '''List[AssemblyStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3432.AssemblyStabilityAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_3565.BearingCompoundStabilityAnalysis]':
        '''List[BearingCompoundStabilityAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3565.BearingCompoundStabilityAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_3567.BeltDriveCompoundStabilityAnalysis]':
        '''List[BeltDriveCompoundStabilityAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3567.BeltDriveCompoundStabilityAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3570.BevelDifferentialGearSetCompoundStabilityAnalysis]':
        '''List[BevelDifferentialGearSetCompoundStabilityAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3570.BevelDifferentialGearSetCompoundStabilityAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_3576.BoltCompoundStabilityAnalysis]':
        '''List[BoltCompoundStabilityAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3576.BoltCompoundStabilityAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_3577.BoltedJointCompoundStabilityAnalysis]':
        '''List[BoltedJointCompoundStabilityAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3577.BoltedJointCompoundStabilityAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_3578.ClutchCompoundStabilityAnalysis]':
        '''List[ClutchCompoundStabilityAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3578.ClutchCompoundStabilityAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_3583.ConceptCouplingCompoundStabilityAnalysis]':
        '''List[ConceptCouplingCompoundStabilityAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3583.ConceptCouplingCompoundStabilityAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3588.ConceptGearSetCompoundStabilityAnalysis]':
        '''List[ConceptGearSetCompoundStabilityAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3588.ConceptGearSetCompoundStabilityAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_3598.CVTCompoundStabilityAnalysis]':
        '''List[CVTCompoundStabilityAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3598.CVTCompoundStabilityAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3600.CycloidalAssemblyCompoundStabilityAnalysis]':
        '''List[CycloidalAssemblyCompoundStabilityAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3600.CycloidalAssemblyCompoundStabilityAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3602.CycloidalDiscCompoundStabilityAnalysis]':
        '''List[CycloidalDiscCompoundStabilityAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3602.CycloidalDiscCompoundStabilityAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3606.CylindricalGearSetCompoundStabilityAnalysis]':
        '''List[CylindricalGearSetCompoundStabilityAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3606.CylindricalGearSetCompoundStabilityAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3612.FaceGearSetCompoundStabilityAnalysis]':
        '''List[FaceGearSetCompoundStabilityAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3612.FaceGearSetCompoundStabilityAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_3613.FEPartCompoundStabilityAnalysis]':
        '''List[FEPartCompoundStabilityAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3613.FEPartCompoundStabilityAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3614.FlexiblePinAssemblyCompoundStabilityAnalysis]':
        '''List[FlexiblePinAssemblyCompoundStabilityAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3614.FlexiblePinAssemblyCompoundStabilityAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3621.HypoidGearSetCompoundStabilityAnalysis]':
        '''List[HypoidGearSetCompoundStabilityAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3621.HypoidGearSetCompoundStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3628.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3628.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3631.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3631.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_3632.MassDiscCompoundStabilityAnalysis]':
        '''List[MassDiscCompoundStabilityAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3632.MassDiscCompoundStabilityAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_3633.MeasurementComponentCompoundStabilityAnalysis]':
        '''List[MeasurementComponentCompoundStabilityAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3633.MeasurementComponentCompoundStabilityAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_3635.OilSealCompoundStabilityAnalysis]':
        '''List[OilSealCompoundStabilityAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3635.OilSealCompoundStabilityAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3637.PartToPartShearCouplingCompoundStabilityAnalysis]':
        '''List[PartToPartShearCouplingCompoundStabilityAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3637.PartToPartShearCouplingCompoundStabilityAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_3642.PlanetCarrierCompoundStabilityAnalysis]':
        '''List[PlanetCarrierCompoundStabilityAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3642.PlanetCarrierCompoundStabilityAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_3643.PointLoadCompoundStabilityAnalysis]':
        '''List[PointLoadCompoundStabilityAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3643.PointLoadCompoundStabilityAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_3644.PowerLoadCompoundStabilityAnalysis]':
        '''List[PowerLoadCompoundStabilityAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3644.PowerLoadCompoundStabilityAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3653.ShaftHubConnectionCompoundStabilityAnalysis]':
        '''List[ShaftHubConnectionCompoundStabilityAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3653.ShaftHubConnectionCompoundStabilityAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_3646.RingPinsCompoundStabilityAnalysis]':
        '''List[RingPinsCompoundStabilityAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3646.RingPinsCompoundStabilityAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3648.RollingRingAssemblyCompoundStabilityAnalysis]':
        '''List[RollingRingAssemblyCompoundStabilityAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3648.RollingRingAssemblyCompoundStabilityAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_3652.ShaftCompoundStabilityAnalysis]':
        '''List[ShaftCompoundStabilityAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3652.ShaftCompoundStabilityAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3658.SpiralBevelGearSetCompoundStabilityAnalysis]':
        '''List[SpiralBevelGearSetCompoundStabilityAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3658.SpiralBevelGearSetCompoundStabilityAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_3659.SpringDamperCompoundStabilityAnalysis]':
        '''List[SpringDamperCompoundStabilityAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3659.SpringDamperCompoundStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3664.StraightBevelDiffGearSetCompoundStabilityAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundStabilityAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3664.StraightBevelDiffGearSetCompoundStabilityAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3667.StraightBevelGearSetCompoundStabilityAnalysis]':
        '''List[StraightBevelGearSetCompoundStabilityAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3667.StraightBevelGearSetCompoundStabilityAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_3670.SynchroniserCompoundStabilityAnalysis]':
        '''List[SynchroniserCompoundStabilityAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3670.SynchroniserCompoundStabilityAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_3674.TorqueConverterCompoundStabilityAnalysis]':
        '''List[TorqueConverterCompoundStabilityAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3674.TorqueConverterCompoundStabilityAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3678.UnbalancedMassCompoundStabilityAnalysis]':
        '''List[UnbalancedMassCompoundStabilityAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3678.UnbalancedMassCompoundStabilityAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3682.WormGearSetCompoundStabilityAnalysis]':
        '''List[WormGearSetCompoundStabilityAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3682.WormGearSetCompoundStabilityAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3685.ZerolBevelGearSetCompoundStabilityAnalysis]':
        '''List[ZerolBevelGearSetCompoundStabilityAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3685.ZerolBevelGearSetCompoundStabilityAnalysis))
        return value
