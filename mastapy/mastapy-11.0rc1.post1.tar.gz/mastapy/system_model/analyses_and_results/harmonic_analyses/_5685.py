'''_5685.py

KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2210
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6546
from mastapy.system_model.analyses_and_results.system_deflections import _2434
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5683, _5684, _5682
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis(_5682.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2434.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2434.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5683.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsHarmonicAnalysis, constructor.new(_5683.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_harmonic_analysis(self) -> 'List[_5683.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsHarmonicAnalysis, constructor.new(_5683.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis))
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesHarmonicAnalysis, constructor.new(_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_harmonic_analysis(self) -> 'List[_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesHarmonicAnalysis, constructor.new(_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis))
        return value
