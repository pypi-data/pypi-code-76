'''_3274.py

AssemblyCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2083, _2122
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3141
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3275, _3277, _3280, _3286,
    _3287, _3288, _3293, _3298,
    _3308, _3310, _3312, _3316,
    _3322, _3323, _3324, _3331,
    _3338, _3341, _3342, _3343,
    _3345, _3347, _3352, _3353,
    _3354, _3363, _3356, _3358,
    _3362, _3368, _3369, _3374,
    _3377, _3380, _3384, _3388,
    _3392, _3395, _3267
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'AssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponse',)


class AssemblyCompoundSteadyStateSynchronousResponse(_3267.AbstractAssemblyCompoundSteadyStateSynchronousResponse):
    '''AssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3141.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3141.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_3141.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_3141.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def bearings(self) -> 'List[_3275.BearingCompoundSteadyStateSynchronousResponse]':
        '''List[BearingCompoundSteadyStateSynchronousResponse]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3275.BearingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def belt_drives(self) -> 'List[_3277.BeltDriveCompoundSteadyStateSynchronousResponse]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponse]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3277.BeltDriveCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3280.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3280.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolts(self) -> 'List[_3286.BoltCompoundSteadyStateSynchronousResponse]':
        '''List[BoltCompoundSteadyStateSynchronousResponse]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3286.BoltCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolted_joints(self) -> 'List[_3287.BoltedJointCompoundSteadyStateSynchronousResponse]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponse]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3287.BoltedJointCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def clutches(self) -> 'List[_3288.ClutchCompoundSteadyStateSynchronousResponse]':
        '''List[ClutchCompoundSteadyStateSynchronousResponse]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3288.ClutchCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_couplings(self) -> 'List[_3293.ConceptCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponse]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3293.ConceptCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3298.ConceptGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponse]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3298.ConceptGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cv_ts(self) -> 'List[_3308.CVTCompoundSteadyStateSynchronousResponse]':
        '''List[CVTCompoundSteadyStateSynchronousResponse]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3308.CVTCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3310.CycloidalAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalAssemblyCompoundSteadyStateSynchronousResponse]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3310.CycloidalAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3312.CycloidalDiscCompoundSteadyStateSynchronousResponse]':
        '''List[CycloidalDiscCompoundSteadyStateSynchronousResponse]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3312.CycloidalDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3316.CylindricalGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponse]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3316.CylindricalGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3322.FaceGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponse]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3322.FaceGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def fe_parts(self) -> 'List[_3323.FEPartCompoundSteadyStateSynchronousResponse]':
        '''List[FEPartCompoundSteadyStateSynchronousResponse]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3323.FEPartCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3324.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3324.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3331.HypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponse]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3331.HypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3338.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3338.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3341.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3341.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def mass_discs(self) -> 'List[_3342.MassDiscCompoundSteadyStateSynchronousResponse]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponse]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3342.MassDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def measurement_components(self) -> 'List[_3343.MeasurementComponentCompoundSteadyStateSynchronousResponse]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponse]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3343.MeasurementComponentCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def oil_seals(self) -> 'List[_3345.OilSealCompoundSteadyStateSynchronousResponse]':
        '''List[OilSealCompoundSteadyStateSynchronousResponse]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3345.OilSealCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3347.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3347.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def planet_carriers(self) -> 'List[_3352.PlanetCarrierCompoundSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponse]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3352.PlanetCarrierCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def point_loads(self) -> 'List[_3353.PointLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponse]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3353.PointLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def power_loads(self) -> 'List[_3354.PowerLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponse]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3354.PowerLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3363.ShaftHubConnectionCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponse]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3363.ShaftHubConnectionCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def ring_pins(self) -> 'List[_3356.RingPinsCompoundSteadyStateSynchronousResponse]':
        '''List[RingPinsCompoundSteadyStateSynchronousResponse]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3356.RingPinsCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3358.RollingRingAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponse]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3358.RollingRingAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shafts(self) -> 'List[_3362.ShaftCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftCompoundSteadyStateSynchronousResponse]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3362.ShaftCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3368.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3368.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spring_dampers(self) -> 'List[_3369.SpringDamperCompoundSteadyStateSynchronousResponse]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponse]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3369.SpringDamperCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3374.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3374.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3377.StraightBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3377.StraightBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def synchronisers(self) -> 'List[_3380.SynchroniserCompoundSteadyStateSynchronousResponse]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponse]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3380.SynchroniserCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def torque_converters(self) -> 'List[_3384.TorqueConverterCompoundSteadyStateSynchronousResponse]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponse]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3384.TorqueConverterCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3388.UnbalancedMassCompoundSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponse]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3388.UnbalancedMassCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3392.WormGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponse]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3392.WormGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3395.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3395.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value
