'''_6234.py

FaceGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2200
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6516
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6232, _6233, _6239
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'FaceGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCriticalSpeedAnalysis',)


class FaceGearSetCriticalSpeedAnalysis(_6239.GearSetCriticalSpeedAnalysis):
    '''FaceGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCriticalSpeedAnalysis.TYPE'):
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
    def face_gears_critical_speed_analysis(self) -> 'List[_6232.FaceGearCriticalSpeedAnalysis]':
        '''List[FaceGearCriticalSpeedAnalysis]: 'FaceGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCriticalSpeedAnalysis, constructor.new(_6232.FaceGearCriticalSpeedAnalysis))
        return value

    @property
    def face_meshes_critical_speed_analysis(self) -> 'List[_6233.FaceGearMeshCriticalSpeedAnalysis]':
        '''List[FaceGearMeshCriticalSpeedAnalysis]: 'FaceMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCriticalSpeedAnalysis, constructor.new(_6233.FaceGearMeshCriticalSpeedAnalysis))
        return value
