'''_5304.py

AssemblyGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2021, _2058
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6103, _6222
from mastapy.system_model.analyses_and_results.system_deflections import _2256, _2349
from mastapy.system_model.analyses_and_results.gear_whine_analyses import (
    _5369, _5305, _5307, _5310,
    _5317, _5316, _5319, _5325,
    _5329, _5339, _5343, _5361,
    _5362, _5378, _5379, _5386,
    _5389, _5390, _5391, _5393,
    _5396, _5401, _5402, _5403,
    _5410, _5405, _5409, _5417,
    _5419, _5423, _5426, _5429,
    _5434, _5438, _5442, _5445,
    _5298
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'AssemblyGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyGearWhineAnalysis',)


class AssemblyGearWhineAnalysis(_5298.AbstractAssemblyGearWhineAnalysis):
    '''AssemblyGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyGearWhineAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2256.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.AssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def loaded_gear_sets(self) -> 'List[_5369.GearSetGearWhineAnalysis]':
        '''List[GearSetGearWhineAnalysis]: 'LoadedGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedGearSets, constructor.new(_5369.GearSetGearWhineAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5305.BearingGearWhineAnalysis]':
        '''List[BearingGearWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5305.BearingGearWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5307.BeltDriveGearWhineAnalysis]':
        '''List[BeltDriveGearWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5307.BeltDriveGearWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5310.BevelDifferentialGearSetGearWhineAnalysis]':
        '''List[BevelDifferentialGearSetGearWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5310.BevelDifferentialGearSetGearWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5317.BoltGearWhineAnalysis]':
        '''List[BoltGearWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5317.BoltGearWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5316.BoltedJointGearWhineAnalysis]':
        '''List[BoltedJointGearWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5316.BoltedJointGearWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5319.ClutchGearWhineAnalysis]':
        '''List[ClutchGearWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5319.ClutchGearWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5325.ConceptCouplingGearWhineAnalysis]':
        '''List[ConceptCouplingGearWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5325.ConceptCouplingGearWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5329.ConceptGearSetGearWhineAnalysis]':
        '''List[ConceptGearSetGearWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5329.ConceptGearSetGearWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5339.CVTGearWhineAnalysis]':
        '''List[CVTGearWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5339.CVTGearWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5343.CylindricalGearSetGearWhineAnalysis]':
        '''List[CylindricalGearSetGearWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5343.CylindricalGearSetGearWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5361.FaceGearSetGearWhineAnalysis]':
        '''List[FaceGearSetGearWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5361.FaceGearSetGearWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5362.FlexiblePinAssemblyGearWhineAnalysis]':
        '''List[FlexiblePinAssemblyGearWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5362.FlexiblePinAssemblyGearWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5378.HypoidGearSetGearWhineAnalysis]':
        '''List[HypoidGearSetGearWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5378.HypoidGearSetGearWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5379.ImportedFEComponentGearWhineAnalysis]':
        '''List[ImportedFEComponentGearWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5379.ImportedFEComponentGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5386.KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5386.KlingelnbergCycloPalloidHypoidGearSetGearWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5389.KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5389.KlingelnbergCycloPalloidSpiralBevelGearSetGearWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5390.MassDiscGearWhineAnalysis]':
        '''List[MassDiscGearWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5390.MassDiscGearWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5391.MeasurementComponentGearWhineAnalysis]':
        '''List[MeasurementComponentGearWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5391.MeasurementComponentGearWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5393.OilSealGearWhineAnalysis]':
        '''List[OilSealGearWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5393.OilSealGearWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5396.PartToPartShearCouplingGearWhineAnalysis]':
        '''List[PartToPartShearCouplingGearWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5396.PartToPartShearCouplingGearWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5401.PlanetCarrierGearWhineAnalysis]':
        '''List[PlanetCarrierGearWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5401.PlanetCarrierGearWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5402.PointLoadGearWhineAnalysis]':
        '''List[PointLoadGearWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5402.PointLoadGearWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5403.PowerLoadGearWhineAnalysis]':
        '''List[PowerLoadGearWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5403.PowerLoadGearWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5410.ShaftHubConnectionGearWhineAnalysis]':
        '''List[ShaftHubConnectionGearWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5410.ShaftHubConnectionGearWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5405.RollingRingAssemblyGearWhineAnalysis]':
        '''List[RollingRingAssemblyGearWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5405.RollingRingAssemblyGearWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5409.ShaftGearWhineAnalysis]':
        '''List[ShaftGearWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5409.ShaftGearWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5417.SpiralBevelGearSetGearWhineAnalysis]':
        '''List[SpiralBevelGearSetGearWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5417.SpiralBevelGearSetGearWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5419.SpringDamperGearWhineAnalysis]':
        '''List[SpringDamperGearWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5419.SpringDamperGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5423.StraightBevelDiffGearSetGearWhineAnalysis]':
        '''List[StraightBevelDiffGearSetGearWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5423.StraightBevelDiffGearSetGearWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5426.StraightBevelGearSetGearWhineAnalysis]':
        '''List[StraightBevelGearSetGearWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5426.StraightBevelGearSetGearWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5429.SynchroniserGearWhineAnalysis]':
        '''List[SynchroniserGearWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5429.SynchroniserGearWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5434.TorqueConverterGearWhineAnalysis]':
        '''List[TorqueConverterGearWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5434.TorqueConverterGearWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5438.UnbalancedMassGearWhineAnalysis]':
        '''List[UnbalancedMassGearWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5438.UnbalancedMassGearWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5442.WormGearSetGearWhineAnalysis]':
        '''List[WormGearSetGearWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5442.WormGearSetGearWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5445.ZerolBevelGearSetGearWhineAnalysis]':
        '''List[ZerolBevelGearSetGearWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5445.ZerolBevelGearSetGearWhineAnalysis))
        return value
