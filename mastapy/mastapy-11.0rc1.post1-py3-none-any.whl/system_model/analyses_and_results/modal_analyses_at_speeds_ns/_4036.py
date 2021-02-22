'''_4036.py

AssemblyModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _2037, _2074
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6123, _6242
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import (
    _4037, _4039, _4042, _4049,
    _4048, _4052, _4057, _4060,
    _4071, _4075, _4082, _4083,
    _4090, _4091, _4098, _4101,
    _4102, _4103, _4107, _4111,
    _4114, _4115, _4116, _4122,
    _4118, _4123, _4128, _4131,
    _4135, _4138, _4142, _4146,
    _4149, _4153, _4156, _4031
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'AssemblyModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysesAtSpeeds',)


class AssemblyModalAnalysesAtSpeeds(_4031.AbstractAssemblyModalAnalysesAtSpeeds):
    '''AssemblyModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def assembly_load_case(self) -> '_6123.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6123.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_4037.BearingModalAnalysesAtSpeeds]':
        '''List[BearingModalAnalysesAtSpeeds]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4037.BearingModalAnalysesAtSpeeds))
        return value

    @property
    def belt_drives(self) -> 'List[_4039.BeltDriveModalAnalysesAtSpeeds]':
        '''List[BeltDriveModalAnalysesAtSpeeds]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4039.BeltDriveModalAnalysesAtSpeeds))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4042.BevelDifferentialGearSetModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearSetModalAnalysesAtSpeeds]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4042.BevelDifferentialGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def bolts(self) -> 'List[_4049.BoltModalAnalysesAtSpeeds]':
        '''List[BoltModalAnalysesAtSpeeds]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4049.BoltModalAnalysesAtSpeeds))
        return value

    @property
    def bolted_joints(self) -> 'List[_4048.BoltedJointModalAnalysesAtSpeeds]':
        '''List[BoltedJointModalAnalysesAtSpeeds]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4048.BoltedJointModalAnalysesAtSpeeds))
        return value

    @property
    def clutches(self) -> 'List[_4052.ClutchModalAnalysesAtSpeeds]':
        '''List[ClutchModalAnalysesAtSpeeds]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4052.ClutchModalAnalysesAtSpeeds))
        return value

    @property
    def concept_couplings(self) -> 'List[_4057.ConceptCouplingModalAnalysesAtSpeeds]':
        '''List[ConceptCouplingModalAnalysesAtSpeeds]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4057.ConceptCouplingModalAnalysesAtSpeeds))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4060.ConceptGearSetModalAnalysesAtSpeeds]':
        '''List[ConceptGearSetModalAnalysesAtSpeeds]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4060.ConceptGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def cv_ts(self) -> 'List[_4071.CVTModalAnalysesAtSpeeds]':
        '''List[CVTModalAnalysesAtSpeeds]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4071.CVTModalAnalysesAtSpeeds))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4075.CylindricalGearSetModalAnalysesAtSpeeds]':
        '''List[CylindricalGearSetModalAnalysesAtSpeeds]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4075.CylindricalGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4082.FaceGearSetModalAnalysesAtSpeeds]':
        '''List[FaceGearSetModalAnalysesAtSpeeds]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4082.FaceGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4083.FlexiblePinAssemblyModalAnalysesAtSpeeds]':
        '''List[FlexiblePinAssemblyModalAnalysesAtSpeeds]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4083.FlexiblePinAssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4090.HypoidGearSetModalAnalysesAtSpeeds]':
        '''List[HypoidGearSetModalAnalysesAtSpeeds]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4090.HypoidGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4091.ImportedFEComponentModalAnalysesAtSpeeds]':
        '''List[ImportedFEComponentModalAnalysesAtSpeeds]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4091.ImportedFEComponentModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4098.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4098.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4101.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4101.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def mass_discs(self) -> 'List[_4102.MassDiscModalAnalysesAtSpeeds]':
        '''List[MassDiscModalAnalysesAtSpeeds]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4102.MassDiscModalAnalysesAtSpeeds))
        return value

    @property
    def measurement_components(self) -> 'List[_4103.MeasurementComponentModalAnalysesAtSpeeds]':
        '''List[MeasurementComponentModalAnalysesAtSpeeds]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4103.MeasurementComponentModalAnalysesAtSpeeds))
        return value

    @property
    def oil_seals(self) -> 'List[_4107.OilSealModalAnalysesAtSpeeds]':
        '''List[OilSealModalAnalysesAtSpeeds]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4107.OilSealModalAnalysesAtSpeeds))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4111.PartToPartShearCouplingModalAnalysesAtSpeeds]':
        '''List[PartToPartShearCouplingModalAnalysesAtSpeeds]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4111.PartToPartShearCouplingModalAnalysesAtSpeeds))
        return value

    @property
    def planet_carriers(self) -> 'List[_4114.PlanetCarrierModalAnalysesAtSpeeds]':
        '''List[PlanetCarrierModalAnalysesAtSpeeds]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4114.PlanetCarrierModalAnalysesAtSpeeds))
        return value

    @property
    def point_loads(self) -> 'List[_4115.PointLoadModalAnalysesAtSpeeds]':
        '''List[PointLoadModalAnalysesAtSpeeds]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4115.PointLoadModalAnalysesAtSpeeds))
        return value

    @property
    def power_loads(self) -> 'List[_4116.PowerLoadModalAnalysesAtSpeeds]':
        '''List[PowerLoadModalAnalysesAtSpeeds]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4116.PowerLoadModalAnalysesAtSpeeds))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4122.ShaftHubConnectionModalAnalysesAtSpeeds]':
        '''List[ShaftHubConnectionModalAnalysesAtSpeeds]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4122.ShaftHubConnectionModalAnalysesAtSpeeds))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4118.RollingRingAssemblyModalAnalysesAtSpeeds]':
        '''List[RollingRingAssemblyModalAnalysesAtSpeeds]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4118.RollingRingAssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def shafts(self) -> 'List[_4123.ShaftModalAnalysesAtSpeeds]':
        '''List[ShaftModalAnalysesAtSpeeds]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4123.ShaftModalAnalysesAtSpeeds))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4128.SpiralBevelGearSetModalAnalysesAtSpeeds]':
        '''List[SpiralBevelGearSetModalAnalysesAtSpeeds]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4128.SpiralBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def spring_dampers(self) -> 'List[_4131.SpringDamperModalAnalysesAtSpeeds]':
        '''List[SpringDamperModalAnalysesAtSpeeds]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4131.SpringDamperModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4135.StraightBevelDiffGearSetModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtSpeeds]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4135.StraightBevelDiffGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4138.StraightBevelGearSetModalAnalysesAtSpeeds]':
        '''List[StraightBevelGearSetModalAnalysesAtSpeeds]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4138.StraightBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def synchronisers(self) -> 'List[_4142.SynchroniserModalAnalysesAtSpeeds]':
        '''List[SynchroniserModalAnalysesAtSpeeds]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4142.SynchroniserModalAnalysesAtSpeeds))
        return value

    @property
    def torque_converters(self) -> 'List[_4146.TorqueConverterModalAnalysesAtSpeeds]':
        '''List[TorqueConverterModalAnalysesAtSpeeds]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4146.TorqueConverterModalAnalysesAtSpeeds))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4149.UnbalancedMassModalAnalysesAtSpeeds]':
        '''List[UnbalancedMassModalAnalysesAtSpeeds]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4149.UnbalancedMassModalAnalysesAtSpeeds))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4153.WormGearSetModalAnalysesAtSpeeds]':
        '''List[WormGearSetModalAnalysesAtSpeeds]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4153.WormGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4156.ZerolBevelGearSetModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearSetModalAnalysesAtSpeeds]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4156.ZerolBevelGearSetModalAnalysesAtSpeeds))
        return value
