'''_3158.py

AssemblyCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2037, _2074
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3033
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3159, _3161, _3164, _3170,
    _3171, _3172, _3177, _3182,
    _3192, _3196, _3202, _3203,
    _3210, _3211, _3218, _3221,
    _3222, _3223, _3225, _3227,
    _3232, _3233, _3234, _3241,
    _3236, _3240, _3246, _3247,
    _3252, _3255, _3258, _3262,
    _3266, _3270, _3273, _3153
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'AssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponse',)


class AssemblyCompoundSteadyStateSynchronousResponse(_3153.AbstractAssemblyCompoundSteadyStateSynchronousResponse):
    '''AssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3033.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3033.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def assembly_steady_state_synchronous_response_load_cases(self) -> 'List[_3033.AssemblySteadyStateSynchronousResponse]':
        '''List[AssemblySteadyStateSynchronousResponse]: 'AssemblySteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseLoadCases, constructor.new(_3033.AssemblySteadyStateSynchronousResponse))
        return value

    @property
    def bearings(self) -> 'List[_3159.BearingCompoundSteadyStateSynchronousResponse]':
        '''List[BearingCompoundSteadyStateSynchronousResponse]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3159.BearingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def belt_drives(self) -> 'List[_3161.BeltDriveCompoundSteadyStateSynchronousResponse]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponse]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3161.BeltDriveCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3164.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3164.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolts(self) -> 'List[_3170.BoltCompoundSteadyStateSynchronousResponse]':
        '''List[BoltCompoundSteadyStateSynchronousResponse]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3170.BoltCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def bolted_joints(self) -> 'List[_3171.BoltedJointCompoundSteadyStateSynchronousResponse]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponse]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3171.BoltedJointCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def clutches(self) -> 'List[_3172.ClutchCompoundSteadyStateSynchronousResponse]':
        '''List[ClutchCompoundSteadyStateSynchronousResponse]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3172.ClutchCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_couplings(self) -> 'List[_3177.ConceptCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponse]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3177.ConceptCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3182.ConceptGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponse]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3182.ConceptGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cv_ts(self) -> 'List[_3192.CVTCompoundSteadyStateSynchronousResponse]':
        '''List[CVTCompoundSteadyStateSynchronousResponse]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3192.CVTCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3196.CylindricalGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponse]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3196.CylindricalGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3202.FaceGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponse]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3202.FaceGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3203.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3203.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3210.HypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponse]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3210.HypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3211.ImportedFEComponentCompoundSteadyStateSynchronousResponse]':
        '''List[ImportedFEComponentCompoundSteadyStateSynchronousResponse]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3211.ImportedFEComponentCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3218.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3218.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3221.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3221.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def mass_discs(self) -> 'List[_3222.MassDiscCompoundSteadyStateSynchronousResponse]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponse]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3222.MassDiscCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def measurement_components(self) -> 'List[_3223.MeasurementComponentCompoundSteadyStateSynchronousResponse]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponse]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3223.MeasurementComponentCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def oil_seals(self) -> 'List[_3225.OilSealCompoundSteadyStateSynchronousResponse]':
        '''List[OilSealCompoundSteadyStateSynchronousResponse]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3225.OilSealCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3227.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponse]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3227.PartToPartShearCouplingCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def planet_carriers(self) -> 'List[_3232.PlanetCarrierCompoundSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponse]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3232.PlanetCarrierCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def point_loads(self) -> 'List[_3233.PointLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponse]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3233.PointLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def power_loads(self) -> 'List[_3234.PowerLoadCompoundSteadyStateSynchronousResponse]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponse]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3234.PowerLoadCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3241.ShaftHubConnectionCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponse]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3241.ShaftHubConnectionCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3236.RollingRingAssemblyCompoundSteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponse]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3236.RollingRingAssemblyCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def shafts(self) -> 'List[_3240.ShaftCompoundSteadyStateSynchronousResponse]':
        '''List[ShaftCompoundSteadyStateSynchronousResponse]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3240.ShaftCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3246.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponse]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3246.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def spring_dampers(self) -> 'List[_3247.SpringDamperCompoundSteadyStateSynchronousResponse]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponse]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3247.SpringDamperCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3252.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3252.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3255.StraightBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponse]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3255.StraightBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def synchronisers(self) -> 'List[_3258.SynchroniserCompoundSteadyStateSynchronousResponse]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponse]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3258.SynchroniserCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def torque_converters(self) -> 'List[_3262.TorqueConverterCompoundSteadyStateSynchronousResponse]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponse]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3262.TorqueConverterCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3266.UnbalancedMassCompoundSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponse]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3266.UnbalancedMassCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3270.WormGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponse]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3270.WormGearSetCompoundSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3273.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponse]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3273.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse))
        return value
