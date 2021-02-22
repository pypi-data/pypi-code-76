'''_5381.py

FaceGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2127
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6185
from mastapy.system_model.analyses_and_results.system_deflections import _2326
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5379, _5380, _5389
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'FaceGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetGearWhineAnalysis',)


class FaceGearSetGearWhineAnalysis(_5389.GearSetGearWhineAnalysis):
    '''FaceGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2127.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2127.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6185.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6185.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2326.FaceGearSetSystemDeflection':
        '''FaceGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2326.FaceGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5379.FaceGearGearWhineAnalysis]':
        '''List[FaceGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5379.FaceGearGearWhineAnalysis))
        return value

    @property
    def face_gears_gear_whine_analysis(self) -> 'List[_5379.FaceGearGearWhineAnalysis]':
        '''List[FaceGearGearWhineAnalysis]: 'FaceGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsGearWhineAnalysis, constructor.new(_5379.FaceGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5380.FaceGearMeshGearWhineAnalysis]':
        '''List[FaceGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5380.FaceGearMeshGearWhineAnalysis))
        return value

    @property
    def face_meshes_gear_whine_analysis(self) -> 'List[_5380.FaceGearMeshGearWhineAnalysis]':
        '''List[FaceGearMeshGearWhineAnalysis]: 'FaceMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesGearWhineAnalysis, constructor.new(_5380.FaceGearMeshGearWhineAnalysis))
        return value
