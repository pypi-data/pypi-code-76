'''_5968.py

FaceGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2200
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6516
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5966, _5967, _5973
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'FaceGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetDynamicAnalysis',)


class FaceGearSetDynamicAnalysis(_5973.GearSetDynamicAnalysis):
    '''FaceGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2200.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6516.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6516.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_dynamic_analysis(self) -> 'List[_5966.FaceGearDynamicAnalysis]':
        '''List[FaceGearDynamicAnalysis]: 'FaceGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsDynamicAnalysis, constructor.new(_5966.FaceGearDynamicAnalysis))
        return value

    @property
    def face_meshes_dynamic_analysis(self) -> 'List[_5967.FaceGearMeshDynamicAnalysis]':
        '''List[FaceGearMeshDynamicAnalysis]: 'FaceMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesDynamicAnalysis, constructor.new(_5967.FaceGearMeshDynamicAnalysis))
        return value
