'''_4017.py

AssemblyModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _2021, _2058
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6103, _6222
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import (
    _4018, _4020, _4023, _4030,
    _4029, _4033, _4038, _4041,
    _4051, _4055, _4062, _4063,
    _4070, _4071, _4078, _4081,
    _4082, _4083, _4087, _4091,
    _4094, _4095, _4096, _4102,
    _4098, _4103, _4108, _4111,
    _4115, _4118, _4122, _4126,
    _4129, _4133, _4136, _4012
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'AssemblyModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysesAtSpeeds',)


class AssemblyModalAnalysesAtSpeeds(_4012.AbstractAssemblyModalAnalysesAtSpeeds):
    '''AssemblyModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2021.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6103.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6103.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_4018.BearingModalAnalysesAtSpeeds]':
        '''List[BearingModalAnalysesAtSpeeds]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4018.BearingModalAnalysesAtSpeeds))
        return value

    @property
    def belt_drives(self) -> 'List[_4020.BeltDriveModalAnalysesAtSpeeds]':
        '''List[BeltDriveModalAnalysesAtSpeeds]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4020.BeltDriveModalAnalysesAtSpeeds))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4023.BevelDifferentialGearSetModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearSetModalAnalysesAtSpeeds]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4023.BevelDifferentialGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def bolts(self) -> 'List[_4030.BoltModalAnalysesAtSpeeds]':
        '''List[BoltModalAnalysesAtSpeeds]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4030.BoltModalAnalysesAtSpeeds))
        return value

    @property
    def bolted_joints(self) -> 'List[_4029.BoltedJointModalAnalysesAtSpeeds]':
        '''List[BoltedJointModalAnalysesAtSpeeds]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4029.BoltedJointModalAnalysesAtSpeeds))
        return value

    @property
    def clutches(self) -> 'List[_4033.ClutchModalAnalysesAtSpeeds]':
        '''List[ClutchModalAnalysesAtSpeeds]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4033.ClutchModalAnalysesAtSpeeds))
        return value

    @property
    def concept_couplings(self) -> 'List[_4038.ConceptCouplingModalAnalysesAtSpeeds]':
        '''List[ConceptCouplingModalAnalysesAtSpeeds]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4038.ConceptCouplingModalAnalysesAtSpeeds))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4041.ConceptGearSetModalAnalysesAtSpeeds]':
        '''List[ConceptGearSetModalAnalysesAtSpeeds]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4041.ConceptGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def cv_ts(self) -> 'List[_4051.CVTModalAnalysesAtSpeeds]':
        '''List[CVTModalAnalysesAtSpeeds]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4051.CVTModalAnalysesAtSpeeds))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4055.CylindricalGearSetModalAnalysesAtSpeeds]':
        '''List[CylindricalGearSetModalAnalysesAtSpeeds]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4055.CylindricalGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4062.FaceGearSetModalAnalysesAtSpeeds]':
        '''List[FaceGearSetModalAnalysesAtSpeeds]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4062.FaceGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4063.FlexiblePinAssemblyModalAnalysesAtSpeeds]':
        '''List[FlexiblePinAssemblyModalAnalysesAtSpeeds]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4063.FlexiblePinAssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4070.HypoidGearSetModalAnalysesAtSpeeds]':
        '''List[HypoidGearSetModalAnalysesAtSpeeds]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4070.HypoidGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4071.ImportedFEComponentModalAnalysesAtSpeeds]':
        '''List[ImportedFEComponentModalAnalysesAtSpeeds]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4071.ImportedFEComponentModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4078.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4078.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4081.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4081.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def mass_discs(self) -> 'List[_4082.MassDiscModalAnalysesAtSpeeds]':
        '''List[MassDiscModalAnalysesAtSpeeds]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4082.MassDiscModalAnalysesAtSpeeds))
        return value

    @property
    def measurement_components(self) -> 'List[_4083.MeasurementComponentModalAnalysesAtSpeeds]':
        '''List[MeasurementComponentModalAnalysesAtSpeeds]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4083.MeasurementComponentModalAnalysesAtSpeeds))
        return value

    @property
    def oil_seals(self) -> 'List[_4087.OilSealModalAnalysesAtSpeeds]':
        '''List[OilSealModalAnalysesAtSpeeds]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4087.OilSealModalAnalysesAtSpeeds))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4091.PartToPartShearCouplingModalAnalysesAtSpeeds]':
        '''List[PartToPartShearCouplingModalAnalysesAtSpeeds]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4091.PartToPartShearCouplingModalAnalysesAtSpeeds))
        return value

    @property
    def planet_carriers(self) -> 'List[_4094.PlanetCarrierModalAnalysesAtSpeeds]':
        '''List[PlanetCarrierModalAnalysesAtSpeeds]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4094.PlanetCarrierModalAnalysesAtSpeeds))
        return value

    @property
    def point_loads(self) -> 'List[_4095.PointLoadModalAnalysesAtSpeeds]':
        '''List[PointLoadModalAnalysesAtSpeeds]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4095.PointLoadModalAnalysesAtSpeeds))
        return value

    @property
    def power_loads(self) -> 'List[_4096.PowerLoadModalAnalysesAtSpeeds]':
        '''List[PowerLoadModalAnalysesAtSpeeds]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4096.PowerLoadModalAnalysesAtSpeeds))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4102.ShaftHubConnectionModalAnalysesAtSpeeds]':
        '''List[ShaftHubConnectionModalAnalysesAtSpeeds]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4102.ShaftHubConnectionModalAnalysesAtSpeeds))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4098.RollingRingAssemblyModalAnalysesAtSpeeds]':
        '''List[RollingRingAssemblyModalAnalysesAtSpeeds]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4098.RollingRingAssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def shafts(self) -> 'List[_4103.ShaftModalAnalysesAtSpeeds]':
        '''List[ShaftModalAnalysesAtSpeeds]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4103.ShaftModalAnalysesAtSpeeds))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4108.SpiralBevelGearSetModalAnalysesAtSpeeds]':
        '''List[SpiralBevelGearSetModalAnalysesAtSpeeds]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4108.SpiralBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def spring_dampers(self) -> 'List[_4111.SpringDamperModalAnalysesAtSpeeds]':
        '''List[SpringDamperModalAnalysesAtSpeeds]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4111.SpringDamperModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4115.StraightBevelDiffGearSetModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtSpeeds]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4115.StraightBevelDiffGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4118.StraightBevelGearSetModalAnalysesAtSpeeds]':
        '''List[StraightBevelGearSetModalAnalysesAtSpeeds]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4118.StraightBevelGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def synchronisers(self) -> 'List[_4122.SynchroniserModalAnalysesAtSpeeds]':
        '''List[SynchroniserModalAnalysesAtSpeeds]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4122.SynchroniserModalAnalysesAtSpeeds))
        return value

    @property
    def torque_converters(self) -> 'List[_4126.TorqueConverterModalAnalysesAtSpeeds]':
        '''List[TorqueConverterModalAnalysesAtSpeeds]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4126.TorqueConverterModalAnalysesAtSpeeds))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4129.UnbalancedMassModalAnalysesAtSpeeds]':
        '''List[UnbalancedMassModalAnalysesAtSpeeds]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4129.UnbalancedMassModalAnalysesAtSpeeds))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4133.WormGearSetModalAnalysesAtSpeeds]':
        '''List[WormGearSetModalAnalysesAtSpeeds]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4133.WormGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4136.ZerolBevelGearSetModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearSetModalAnalysesAtSpeeds]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4136.ZerolBevelGearSetModalAnalysesAtSpeeds))
        return value
