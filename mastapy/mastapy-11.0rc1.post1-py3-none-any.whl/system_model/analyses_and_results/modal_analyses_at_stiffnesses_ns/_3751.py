'''_3751.py

AssemblyModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _2000, _2037
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6082, _6201
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import (
    _3752, _3754, _3757, _3764,
    _3763, _3767, _3772, _3775,
    _3786, _3790, _3796, _3797,
    _3804, _3805, _3812, _3815,
    _3816, _3817, _3821, _3825,
    _3828, _3829, _3830, _3836,
    _3832, _3837, _3842, _3845,
    _3848, _3851, _3855, _3859,
    _3862, _3866, _3869, _3746
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'AssemblyModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysesAtStiffnesses',)


class AssemblyModalAnalysesAtStiffnesses(_3746.AbstractAssemblyModalAnalysesAtStiffnesses):
    '''AssemblyModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2000.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6082.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6082.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_3752.BearingModalAnalysesAtStiffnesses]':
        '''List[BearingModalAnalysesAtStiffnesses]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3752.BearingModalAnalysesAtStiffnesses))
        return value

    @property
    def belt_drives(self) -> 'List[_3754.BeltDriveModalAnalysesAtStiffnesses]':
        '''List[BeltDriveModalAnalysesAtStiffnesses]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3754.BeltDriveModalAnalysesAtStiffnesses))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3757.BevelDifferentialGearSetModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetModalAnalysesAtStiffnesses]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3757.BevelDifferentialGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def bolts(self) -> 'List[_3764.BoltModalAnalysesAtStiffnesses]':
        '''List[BoltModalAnalysesAtStiffnesses]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3764.BoltModalAnalysesAtStiffnesses))
        return value

    @property
    def bolted_joints(self) -> 'List[_3763.BoltedJointModalAnalysesAtStiffnesses]':
        '''List[BoltedJointModalAnalysesAtStiffnesses]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3763.BoltedJointModalAnalysesAtStiffnesses))
        return value

    @property
    def clutches(self) -> 'List[_3767.ClutchModalAnalysesAtStiffnesses]':
        '''List[ClutchModalAnalysesAtStiffnesses]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3767.ClutchModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_couplings(self) -> 'List[_3772.ConceptCouplingModalAnalysesAtStiffnesses]':
        '''List[ConceptCouplingModalAnalysesAtStiffnesses]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3772.ConceptCouplingModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3775.ConceptGearSetModalAnalysesAtStiffnesses]':
        '''List[ConceptGearSetModalAnalysesAtStiffnesses]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3775.ConceptGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def cv_ts(self) -> 'List[_3786.CVTModalAnalysesAtStiffnesses]':
        '''List[CVTModalAnalysesAtStiffnesses]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3786.CVTModalAnalysesAtStiffnesses))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3790.CylindricalGearSetModalAnalysesAtStiffnesses]':
        '''List[CylindricalGearSetModalAnalysesAtStiffnesses]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3790.CylindricalGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3796.FaceGearSetModalAnalysesAtStiffnesses]':
        '''List[FaceGearSetModalAnalysesAtStiffnesses]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3796.FaceGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3797.FlexiblePinAssemblyModalAnalysesAtStiffnesses]':
        '''List[FlexiblePinAssemblyModalAnalysesAtStiffnesses]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3797.FlexiblePinAssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3804.HypoidGearSetModalAnalysesAtStiffnesses]':
        '''List[HypoidGearSetModalAnalysesAtStiffnesses]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3804.HypoidGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3805.ImportedFEComponentModalAnalysesAtStiffnesses]':
        '''List[ImportedFEComponentModalAnalysesAtStiffnesses]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3805.ImportedFEComponentModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3812.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3812.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3815.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3815.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def mass_discs(self) -> 'List[_3816.MassDiscModalAnalysesAtStiffnesses]':
        '''List[MassDiscModalAnalysesAtStiffnesses]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3816.MassDiscModalAnalysesAtStiffnesses))
        return value

    @property
    def measurement_components(self) -> 'List[_3817.MeasurementComponentModalAnalysesAtStiffnesses]':
        '''List[MeasurementComponentModalAnalysesAtStiffnesses]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3817.MeasurementComponentModalAnalysesAtStiffnesses))
        return value

    @property
    def oil_seals(self) -> 'List[_3821.OilSealModalAnalysesAtStiffnesses]':
        '''List[OilSealModalAnalysesAtStiffnesses]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3821.OilSealModalAnalysesAtStiffnesses))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3825.PartToPartShearCouplingModalAnalysesAtStiffnesses]':
        '''List[PartToPartShearCouplingModalAnalysesAtStiffnesses]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3825.PartToPartShearCouplingModalAnalysesAtStiffnesses))
        return value

    @property
    def planet_carriers(self) -> 'List[_3828.PlanetCarrierModalAnalysesAtStiffnesses]':
        '''List[PlanetCarrierModalAnalysesAtStiffnesses]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3828.PlanetCarrierModalAnalysesAtStiffnesses))
        return value

    @property
    def point_loads(self) -> 'List[_3829.PointLoadModalAnalysesAtStiffnesses]':
        '''List[PointLoadModalAnalysesAtStiffnesses]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3829.PointLoadModalAnalysesAtStiffnesses))
        return value

    @property
    def power_loads(self) -> 'List[_3830.PowerLoadModalAnalysesAtStiffnesses]':
        '''List[PowerLoadModalAnalysesAtStiffnesses]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3830.PowerLoadModalAnalysesAtStiffnesses))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3836.ShaftHubConnectionModalAnalysesAtStiffnesses]':
        '''List[ShaftHubConnectionModalAnalysesAtStiffnesses]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3836.ShaftHubConnectionModalAnalysesAtStiffnesses))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3832.RollingRingAssemblyModalAnalysesAtStiffnesses]':
        '''List[RollingRingAssemblyModalAnalysesAtStiffnesses]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3832.RollingRingAssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def shafts(self) -> 'List[_3837.ShaftModalAnalysesAtStiffnesses]':
        '''List[ShaftModalAnalysesAtStiffnesses]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3837.ShaftModalAnalysesAtStiffnesses))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3842.SpiralBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[SpiralBevelGearSetModalAnalysesAtStiffnesses]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3842.SpiralBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def spring_dampers(self) -> 'List[_3845.SpringDamperModalAnalysesAtStiffnesses]':
        '''List[SpringDamperModalAnalysesAtStiffnesses]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3845.SpringDamperModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3848.StraightBevelDiffGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtStiffnesses]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3848.StraightBevelDiffGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3851.StraightBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearSetModalAnalysesAtStiffnesses]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3851.StraightBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def synchronisers(self) -> 'List[_3855.SynchroniserModalAnalysesAtStiffnesses]':
        '''List[SynchroniserModalAnalysesAtStiffnesses]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3855.SynchroniserModalAnalysesAtStiffnesses))
        return value

    @property
    def torque_converters(self) -> 'List[_3859.TorqueConverterModalAnalysesAtStiffnesses]':
        '''List[TorqueConverterModalAnalysesAtStiffnesses]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3859.TorqueConverterModalAnalysesAtStiffnesses))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3862.UnbalancedMassModalAnalysesAtStiffnesses]':
        '''List[UnbalancedMassModalAnalysesAtStiffnesses]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3862.UnbalancedMassModalAnalysesAtStiffnesses))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3866.WormGearSetModalAnalysesAtStiffnesses]':
        '''List[WormGearSetModalAnalysesAtStiffnesses]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3866.WormGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3869.ZerolBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearSetModalAnalysesAtStiffnesses]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3869.ZerolBevelGearSetModalAnalysesAtStiffnesses))
        return value
