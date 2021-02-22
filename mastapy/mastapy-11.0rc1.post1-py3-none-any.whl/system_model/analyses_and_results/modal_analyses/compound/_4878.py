'''_4878.py

AssemblyCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2083, _2122
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses import _4725
from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
    _4879, _4881, _4884, _4890,
    _4891, _4892, _4897, _4902,
    _4912, _4914, _4916, _4920,
    _4926, _4927, _4928, _4935,
    _4942, _4945, _4946, _4947,
    _4949, _4951, _4956, _4957,
    _4958, _4967, _4960, _4962,
    _4966, _4972, _4973, _4978,
    _4981, _4984, _4988, _4992,
    _4996, _4999, _4871
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'AssemblyCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysis',)


class AssemblyCompoundModalAnalysis(_4871.AbstractAssemblyCompoundModalAnalysis):
    '''AssemblyCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_4725.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4725.AssemblyModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4725.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4725.AssemblyModalAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_4879.BearingCompoundModalAnalysis]':
        '''List[BearingCompoundModalAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4879.BearingCompoundModalAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_4881.BeltDriveCompoundModalAnalysis]':
        '''List[BeltDriveCompoundModalAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4881.BeltDriveCompoundModalAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4884.BevelDifferentialGearSetCompoundModalAnalysis]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4884.BevelDifferentialGearSetCompoundModalAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_4890.BoltCompoundModalAnalysis]':
        '''List[BoltCompoundModalAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4890.BoltCompoundModalAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_4891.BoltedJointCompoundModalAnalysis]':
        '''List[BoltedJointCompoundModalAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4891.BoltedJointCompoundModalAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_4892.ClutchCompoundModalAnalysis]':
        '''List[ClutchCompoundModalAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4892.ClutchCompoundModalAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_4897.ConceptCouplingCompoundModalAnalysis]':
        '''List[ConceptCouplingCompoundModalAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4897.ConceptCouplingCompoundModalAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4902.ConceptGearSetCompoundModalAnalysis]':
        '''List[ConceptGearSetCompoundModalAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4902.ConceptGearSetCompoundModalAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_4912.CVTCompoundModalAnalysis]':
        '''List[CVTCompoundModalAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4912.CVTCompoundModalAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4914.CycloidalAssemblyCompoundModalAnalysis]':
        '''List[CycloidalAssemblyCompoundModalAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4914.CycloidalAssemblyCompoundModalAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4916.CycloidalDiscCompoundModalAnalysis]':
        '''List[CycloidalDiscCompoundModalAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4916.CycloidalDiscCompoundModalAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4920.CylindricalGearSetCompoundModalAnalysis]':
        '''List[CylindricalGearSetCompoundModalAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4920.CylindricalGearSetCompoundModalAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4926.FaceGearSetCompoundModalAnalysis]':
        '''List[FaceGearSetCompoundModalAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4926.FaceGearSetCompoundModalAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_4927.FEPartCompoundModalAnalysis]':
        '''List[FEPartCompoundModalAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4927.FEPartCompoundModalAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4928.FlexiblePinAssemblyCompoundModalAnalysis]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4928.FlexiblePinAssemblyCompoundModalAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4935.HypoidGearSetCompoundModalAnalysis]':
        '''List[HypoidGearSetCompoundModalAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4935.HypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4942.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4942.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4945.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4945.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_4946.MassDiscCompoundModalAnalysis]':
        '''List[MassDiscCompoundModalAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4946.MassDiscCompoundModalAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_4947.MeasurementComponentCompoundModalAnalysis]':
        '''List[MeasurementComponentCompoundModalAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4947.MeasurementComponentCompoundModalAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_4949.OilSealCompoundModalAnalysis]':
        '''List[OilSealCompoundModalAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4949.OilSealCompoundModalAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4951.PartToPartShearCouplingCompoundModalAnalysis]':
        '''List[PartToPartShearCouplingCompoundModalAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4951.PartToPartShearCouplingCompoundModalAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_4956.PlanetCarrierCompoundModalAnalysis]':
        '''List[PlanetCarrierCompoundModalAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4956.PlanetCarrierCompoundModalAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_4957.PointLoadCompoundModalAnalysis]':
        '''List[PointLoadCompoundModalAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4957.PointLoadCompoundModalAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_4958.PowerLoadCompoundModalAnalysis]':
        '''List[PowerLoadCompoundModalAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4958.PowerLoadCompoundModalAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4967.ShaftHubConnectionCompoundModalAnalysis]':
        '''List[ShaftHubConnectionCompoundModalAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4967.ShaftHubConnectionCompoundModalAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_4960.RingPinsCompoundModalAnalysis]':
        '''List[RingPinsCompoundModalAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_4960.RingPinsCompoundModalAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4962.RollingRingAssemblyCompoundModalAnalysis]':
        '''List[RollingRingAssemblyCompoundModalAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4962.RollingRingAssemblyCompoundModalAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_4966.ShaftCompoundModalAnalysis]':
        '''List[ShaftCompoundModalAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4966.ShaftCompoundModalAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4972.SpiralBevelGearSetCompoundModalAnalysis]':
        '''List[SpiralBevelGearSetCompoundModalAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4972.SpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_4973.SpringDamperCompoundModalAnalysis]':
        '''List[SpringDamperCompoundModalAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4973.SpringDamperCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4978.StraightBevelDiffGearSetCompoundModalAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4978.StraightBevelDiffGearSetCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4981.StraightBevelGearSetCompoundModalAnalysis]':
        '''List[StraightBevelGearSetCompoundModalAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4981.StraightBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_4984.SynchroniserCompoundModalAnalysis]':
        '''List[SynchroniserCompoundModalAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4984.SynchroniserCompoundModalAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_4988.TorqueConverterCompoundModalAnalysis]':
        '''List[TorqueConverterCompoundModalAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4988.TorqueConverterCompoundModalAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4992.UnbalancedMassCompoundModalAnalysis]':
        '''List[UnbalancedMassCompoundModalAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4992.UnbalancedMassCompoundModalAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4996.WormGearSetCompoundModalAnalysis]':
        '''List[WormGearSetCompoundModalAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4996.WormGearSetCompoundModalAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4999.ZerolBevelGearSetCompoundModalAnalysis]':
        '''List[ZerolBevelGearSetCompoundModalAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4999.ZerolBevelGearSetCompoundModalAnalysis))
        return value
