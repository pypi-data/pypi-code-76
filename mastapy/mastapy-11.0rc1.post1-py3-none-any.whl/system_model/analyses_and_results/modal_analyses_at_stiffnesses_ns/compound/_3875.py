'''_3875.py

AssemblyCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _2000, _2037
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3751
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import (
    _3876, _3878, _3881, _3887,
    _3888, _3889, _3894, _3899,
    _3909, _3913, _3919, _3920,
    _3927, _3928, _3935, _3938,
    _3939, _3940, _3942, _3944,
    _3949, _3950, _3951, _3958,
    _3953, _3957, _3963, _3964,
    _3969, _3972, _3975, _3979,
    _3983, _3987, _3990, _3870
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'AssemblyCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysesAtStiffnesses',)


class AssemblyCompoundModalAnalysesAtStiffnesses(_3870.AbstractAssemblyCompoundModalAnalysesAtStiffnesses):
    '''AssemblyCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2000.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

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
    def load_case_analyses_ready(self) -> 'List[_3751.AssemblyModalAnalysesAtStiffnesses]':
        '''List[AssemblyModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3751.AssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3751.AssemblyModalAnalysesAtStiffnesses]':
        '''List[AssemblyModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_3751.AssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def bearings(self) -> 'List[_3876.BearingCompoundModalAnalysesAtStiffnesses]':
        '''List[BearingCompoundModalAnalysesAtStiffnesses]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3876.BearingCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def belt_drives(self) -> 'List[_3878.BeltDriveCompoundModalAnalysesAtStiffnesses]':
        '''List[BeltDriveCompoundModalAnalysesAtStiffnesses]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3878.BeltDriveCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3881.BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3881.BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bolts(self) -> 'List[_3887.BoltCompoundModalAnalysesAtStiffnesses]':
        '''List[BoltCompoundModalAnalysesAtStiffnesses]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3887.BoltCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bolted_joints(self) -> 'List[_3888.BoltedJointCompoundModalAnalysesAtStiffnesses]':
        '''List[BoltedJointCompoundModalAnalysesAtStiffnesses]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3888.BoltedJointCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def clutches(self) -> 'List[_3889.ClutchCompoundModalAnalysesAtStiffnesses]':
        '''List[ClutchCompoundModalAnalysesAtStiffnesses]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3889.ClutchCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_couplings(self) -> 'List[_3894.ConceptCouplingCompoundModalAnalysesAtStiffnesses]':
        '''List[ConceptCouplingCompoundModalAnalysesAtStiffnesses]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3894.ConceptCouplingCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3899.ConceptGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[ConceptGearSetCompoundModalAnalysesAtStiffnesses]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3899.ConceptGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def cv_ts(self) -> 'List[_3909.CVTCompoundModalAnalysesAtStiffnesses]':
        '''List[CVTCompoundModalAnalysesAtStiffnesses]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3909.CVTCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3913.CylindricalGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[CylindricalGearSetCompoundModalAnalysesAtStiffnesses]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3913.CylindricalGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3919.FaceGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[FaceGearSetCompoundModalAnalysesAtStiffnesses]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3919.FaceGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3920.FlexiblePinAssemblyCompoundModalAnalysesAtStiffnesses]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysesAtStiffnesses]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3920.FlexiblePinAssemblyCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3927.HypoidGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[HypoidGearSetCompoundModalAnalysesAtStiffnesses]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3927.HypoidGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3928.ImportedFEComponentCompoundModalAnalysesAtStiffnesses]':
        '''List[ImportedFEComponentCompoundModalAnalysesAtStiffnesses]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3928.ImportedFEComponentCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3935.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3935.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3938.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3938.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def mass_discs(self) -> 'List[_3939.MassDiscCompoundModalAnalysesAtStiffnesses]':
        '''List[MassDiscCompoundModalAnalysesAtStiffnesses]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3939.MassDiscCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def measurement_components(self) -> 'List[_3940.MeasurementComponentCompoundModalAnalysesAtStiffnesses]':
        '''List[MeasurementComponentCompoundModalAnalysesAtStiffnesses]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3940.MeasurementComponentCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def oil_seals(self) -> 'List[_3942.OilSealCompoundModalAnalysesAtStiffnesses]':
        '''List[OilSealCompoundModalAnalysesAtStiffnesses]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3942.OilSealCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3944.PartToPartShearCouplingCompoundModalAnalysesAtStiffnesses]':
        '''List[PartToPartShearCouplingCompoundModalAnalysesAtStiffnesses]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3944.PartToPartShearCouplingCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def planet_carriers(self) -> 'List[_3949.PlanetCarrierCompoundModalAnalysesAtStiffnesses]':
        '''List[PlanetCarrierCompoundModalAnalysesAtStiffnesses]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3949.PlanetCarrierCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def point_loads(self) -> 'List[_3950.PointLoadCompoundModalAnalysesAtStiffnesses]':
        '''List[PointLoadCompoundModalAnalysesAtStiffnesses]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3950.PointLoadCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def power_loads(self) -> 'List[_3951.PowerLoadCompoundModalAnalysesAtStiffnesses]':
        '''List[PowerLoadCompoundModalAnalysesAtStiffnesses]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3951.PowerLoadCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3958.ShaftHubConnectionCompoundModalAnalysesAtStiffnesses]':
        '''List[ShaftHubConnectionCompoundModalAnalysesAtStiffnesses]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3958.ShaftHubConnectionCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3953.RollingRingAssemblyCompoundModalAnalysesAtStiffnesses]':
        '''List[RollingRingAssemblyCompoundModalAnalysesAtStiffnesses]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3953.RollingRingAssemblyCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def shafts(self) -> 'List[_3957.ShaftCompoundModalAnalysesAtStiffnesses]':
        '''List[ShaftCompoundModalAnalysesAtStiffnesses]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3957.ShaftCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3963.SpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[SpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3963.SpiralBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def spring_dampers(self) -> 'List[_3964.SpringDamperCompoundModalAnalysesAtStiffnesses]':
        '''List[SpringDamperCompoundModalAnalysesAtStiffnesses]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3964.SpringDamperCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3969.StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3969.StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3972.StraightBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3972.StraightBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def synchronisers(self) -> 'List[_3975.SynchroniserCompoundModalAnalysesAtStiffnesses]':
        '''List[SynchroniserCompoundModalAnalysesAtStiffnesses]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3975.SynchroniserCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def torque_converters(self) -> 'List[_3979.TorqueConverterCompoundModalAnalysesAtStiffnesses]':
        '''List[TorqueConverterCompoundModalAnalysesAtStiffnesses]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3979.TorqueConverterCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3983.UnbalancedMassCompoundModalAnalysesAtStiffnesses]':
        '''List[UnbalancedMassCompoundModalAnalysesAtStiffnesses]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3983.UnbalancedMassCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3987.WormGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[WormGearSetCompoundModalAnalysesAtStiffnesses]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3987.WormGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3990.ZerolBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3990.ZerolBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value
