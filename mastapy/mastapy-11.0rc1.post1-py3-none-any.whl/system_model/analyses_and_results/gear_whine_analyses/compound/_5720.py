'''_5720.py

AssemblyCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2021, _2058
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5304
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import (
    _5721, _5723, _5726, _5732,
    _5733, _5734, _5739, _5744,
    _5754, _5758, _5764, _5765,
    _5772, _5773, _5780, _5783,
    _5784, _5785, _5787, _5789,
    _5794, _5795, _5796, _5803,
    _5798, _5802, _5808, _5809,
    _5814, _5817, _5820, _5824,
    _5828, _5832, _5835, _5715
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'AssemblyCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundGearWhineAnalysis',)


class AssemblyCompoundGearWhineAnalysis(_5715.AbstractAssemblyCompoundGearWhineAnalysis):
    '''AssemblyCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2021.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

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
    def load_case_analyses_ready(self) -> 'List[_5304.AssemblyGearWhineAnalysis]':
        '''List[AssemblyGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5304.AssemblyGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5304.AssemblyGearWhineAnalysis]':
        '''List[AssemblyGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5304.AssemblyGearWhineAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5721.BearingCompoundGearWhineAnalysis]':
        '''List[BearingCompoundGearWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5721.BearingCompoundGearWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5723.BeltDriveCompoundGearWhineAnalysis]':
        '''List[BeltDriveCompoundGearWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5723.BeltDriveCompoundGearWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5726.BevelDifferentialGearSetCompoundGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetCompoundGearWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5726.BevelDifferentialGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5732.BoltCompoundGearWhineAnalysis]':
        '''List[BoltCompoundGearWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5732.BoltCompoundGearWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5733.BoltedJointCompoundGearWhineAnalysis]':
        '''List[BoltedJointCompoundGearWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5733.BoltedJointCompoundGearWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5734.ClutchCompoundGearWhineAnalysis]':
        '''List[ClutchCompoundGearWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5734.ClutchCompoundGearWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5739.ConceptCouplingCompoundGearWhineAnalysis]':
        '''List[ConceptCouplingCompoundGearWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5739.ConceptCouplingCompoundGearWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5744.ConceptGearSetCompoundGearWhineAnalysis]':
        '''List[ConceptGearSetCompoundGearWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5744.ConceptGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5754.CVTCompoundGearWhineAnalysis]':
        '''List[CVTCompoundGearWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5754.CVTCompoundGearWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5758.CylindricalGearSetCompoundGearWhineAnalysis]':
        '''List[CylindricalGearSetCompoundGearWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5758.CylindricalGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5764.FaceGearSetCompoundGearWhineAnalysis]':
        '''List[FaceGearSetCompoundGearWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5764.FaceGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5765.FlexiblePinAssemblyCompoundGearWhineAnalysis]':
        '''List[FlexiblePinAssemblyCompoundGearWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5765.FlexiblePinAssemblyCompoundGearWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5772.HypoidGearSetCompoundGearWhineAnalysis]':
        '''List[HypoidGearSetCompoundGearWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5772.HypoidGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5773.ImportedFEComponentCompoundGearWhineAnalysis]':
        '''List[ImportedFEComponentCompoundGearWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5773.ImportedFEComponentCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5780.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5780.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5783.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5783.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5784.MassDiscCompoundGearWhineAnalysis]':
        '''List[MassDiscCompoundGearWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5784.MassDiscCompoundGearWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5785.MeasurementComponentCompoundGearWhineAnalysis]':
        '''List[MeasurementComponentCompoundGearWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5785.MeasurementComponentCompoundGearWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5787.OilSealCompoundGearWhineAnalysis]':
        '''List[OilSealCompoundGearWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5787.OilSealCompoundGearWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5789.PartToPartShearCouplingCompoundGearWhineAnalysis]':
        '''List[PartToPartShearCouplingCompoundGearWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5789.PartToPartShearCouplingCompoundGearWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5794.PlanetCarrierCompoundGearWhineAnalysis]':
        '''List[PlanetCarrierCompoundGearWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5794.PlanetCarrierCompoundGearWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5795.PointLoadCompoundGearWhineAnalysis]':
        '''List[PointLoadCompoundGearWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5795.PointLoadCompoundGearWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5796.PowerLoadCompoundGearWhineAnalysis]':
        '''List[PowerLoadCompoundGearWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5796.PowerLoadCompoundGearWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5803.ShaftHubConnectionCompoundGearWhineAnalysis]':
        '''List[ShaftHubConnectionCompoundGearWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5803.ShaftHubConnectionCompoundGearWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5798.RollingRingAssemblyCompoundGearWhineAnalysis]':
        '''List[RollingRingAssemblyCompoundGearWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5798.RollingRingAssemblyCompoundGearWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5802.ShaftCompoundGearWhineAnalysis]':
        '''List[ShaftCompoundGearWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5802.ShaftCompoundGearWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5808.SpiralBevelGearSetCompoundGearWhineAnalysis]':
        '''List[SpiralBevelGearSetCompoundGearWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5808.SpiralBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5809.SpringDamperCompoundGearWhineAnalysis]':
        '''List[SpringDamperCompoundGearWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5809.SpringDamperCompoundGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5814.StraightBevelDiffGearSetCompoundGearWhineAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundGearWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5814.StraightBevelDiffGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5817.StraightBevelGearSetCompoundGearWhineAnalysis]':
        '''List[StraightBevelGearSetCompoundGearWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5817.StraightBevelGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5820.SynchroniserCompoundGearWhineAnalysis]':
        '''List[SynchroniserCompoundGearWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5820.SynchroniserCompoundGearWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5824.TorqueConverterCompoundGearWhineAnalysis]':
        '''List[TorqueConverterCompoundGearWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5824.TorqueConverterCompoundGearWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5828.UnbalancedMassCompoundGearWhineAnalysis]':
        '''List[UnbalancedMassCompoundGearWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5828.UnbalancedMassCompoundGearWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5832.WormGearSetCompoundGearWhineAnalysis]':
        '''List[WormGearSetCompoundGearWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5832.WormGearSetCompoundGearWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5835.ZerolBevelGearSetCompoundGearWhineAnalysis]':
        '''List[ZerolBevelGearSetCompoundGearWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5835.ZerolBevelGearSetCompoundGearWhineAnalysis))
        return value
