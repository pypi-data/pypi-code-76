'''_5442.py

AssemblySingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2000, _2037
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6082, _6201
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import (
    _5443, _5445, _5447, _5455,
    _5454, _5458, _5463, _5465,
    _5477, _5479, _5485, _5487,
    _5493, _5495, _5501, _5504,
    _5506, _5507, _5510, _5514,
    _5517, _5518, _5519, _5525,
    _5521, _5526, _5531, _5535,
    _5537, _5540, _5546, _5550,
    _5552, _5555, _5558, _5437
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'AssemblySingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySingleMeshWhineAnalysis',)


class AssemblySingleMeshWhineAnalysis(_5437.AbstractAssemblySingleMeshWhineAnalysis):
    '''AssemblySingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySingleMeshWhineAnalysis.TYPE'):
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
    def bearings(self) -> 'List[_5443.BearingSingleMeshWhineAnalysis]':
        '''List[BearingSingleMeshWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5443.BearingSingleMeshWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5445.BeltDriveSingleMeshWhineAnalysis]':
        '''List[BeltDriveSingleMeshWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5445.BeltDriveSingleMeshWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5447.BevelDifferentialGearSetSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSetSingleMeshWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5447.BevelDifferentialGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5455.BoltSingleMeshWhineAnalysis]':
        '''List[BoltSingleMeshWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5455.BoltSingleMeshWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5454.BoltedJointSingleMeshWhineAnalysis]':
        '''List[BoltedJointSingleMeshWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5454.BoltedJointSingleMeshWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5458.ClutchSingleMeshWhineAnalysis]':
        '''List[ClutchSingleMeshWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5458.ClutchSingleMeshWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5463.ConceptCouplingSingleMeshWhineAnalysis]':
        '''List[ConceptCouplingSingleMeshWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5463.ConceptCouplingSingleMeshWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5465.ConceptGearSetSingleMeshWhineAnalysis]':
        '''List[ConceptGearSetSingleMeshWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5465.ConceptGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5477.CVTSingleMeshWhineAnalysis]':
        '''List[CVTSingleMeshWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5477.CVTSingleMeshWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5479.CylindricalGearSetSingleMeshWhineAnalysis]':
        '''List[CylindricalGearSetSingleMeshWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5479.CylindricalGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5485.FaceGearSetSingleMeshWhineAnalysis]':
        '''List[FaceGearSetSingleMeshWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5485.FaceGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5487.FlexiblePinAssemblySingleMeshWhineAnalysis]':
        '''List[FlexiblePinAssemblySingleMeshWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5487.FlexiblePinAssemblySingleMeshWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5493.HypoidGearSetSingleMeshWhineAnalysis]':
        '''List[HypoidGearSetSingleMeshWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5493.HypoidGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5495.ImportedFEComponentSingleMeshWhineAnalysis]':
        '''List[ImportedFEComponentSingleMeshWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5495.ImportedFEComponentSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5501.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5501.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5504.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5504.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5506.MassDiscSingleMeshWhineAnalysis]':
        '''List[MassDiscSingleMeshWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5506.MassDiscSingleMeshWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5507.MeasurementComponentSingleMeshWhineAnalysis]':
        '''List[MeasurementComponentSingleMeshWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5507.MeasurementComponentSingleMeshWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5510.OilSealSingleMeshWhineAnalysis]':
        '''List[OilSealSingleMeshWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5510.OilSealSingleMeshWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5514.PartToPartShearCouplingSingleMeshWhineAnalysis]':
        '''List[PartToPartShearCouplingSingleMeshWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5514.PartToPartShearCouplingSingleMeshWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5517.PlanetCarrierSingleMeshWhineAnalysis]':
        '''List[PlanetCarrierSingleMeshWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5517.PlanetCarrierSingleMeshWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5518.PointLoadSingleMeshWhineAnalysis]':
        '''List[PointLoadSingleMeshWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5518.PointLoadSingleMeshWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5519.PowerLoadSingleMeshWhineAnalysis]':
        '''List[PowerLoadSingleMeshWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5519.PowerLoadSingleMeshWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5525.ShaftHubConnectionSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionSingleMeshWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5525.ShaftHubConnectionSingleMeshWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5521.RollingRingAssemblySingleMeshWhineAnalysis]':
        '''List[RollingRingAssemblySingleMeshWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5521.RollingRingAssemblySingleMeshWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5526.ShaftSingleMeshWhineAnalysis]':
        '''List[ShaftSingleMeshWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5526.ShaftSingleMeshWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5531.SpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearSetSingleMeshWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5531.SpiralBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5535.SpringDamperSingleMeshWhineAnalysis]':
        '''List[SpringDamperSingleMeshWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5535.SpringDamperSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5537.StraightBevelDiffGearSetSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearSetSingleMeshWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5537.StraightBevelDiffGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5540.StraightBevelGearSetSingleMeshWhineAnalysis]':
        '''List[StraightBevelGearSetSingleMeshWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5540.StraightBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5546.SynchroniserSingleMeshWhineAnalysis]':
        '''List[SynchroniserSingleMeshWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5546.SynchroniserSingleMeshWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5550.TorqueConverterSingleMeshWhineAnalysis]':
        '''List[TorqueConverterSingleMeshWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5550.TorqueConverterSingleMeshWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5552.UnbalancedMassSingleMeshWhineAnalysis]':
        '''List[UnbalancedMassSingleMeshWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5552.UnbalancedMassSingleMeshWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5555.WormGearSetSingleMeshWhineAnalysis]':
        '''List[WormGearSetSingleMeshWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5555.WormGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5558.ZerolBevelGearSetSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSetSingleMeshWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5558.ZerolBevelGearSetSingleMeshWhineAnalysis))
        return value
