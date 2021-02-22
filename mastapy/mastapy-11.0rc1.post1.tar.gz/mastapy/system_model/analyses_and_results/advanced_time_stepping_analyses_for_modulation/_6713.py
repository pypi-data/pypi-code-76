'''_6713.py

KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2210
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6546
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6711, _6712, _6710
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation',)


class KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation(_6710.KlingelnbergCycloPalloidConicalGearSetAdvancedTimeSteppingAnalysisForModulation):
    '''KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2210.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6546.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6546.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6711.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidHypoidGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6711.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6712.KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidHypoidMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6712.KlingelnbergCycloPalloidHypoidGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value
