'''_3836.py

FaceGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2127
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6185
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3835, _3834, _3840
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'FaceGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetModalAnalysesAtStiffnesses',)


class FaceGearSetModalAnalysesAtStiffnesses(_3840.GearSetModalAnalysesAtStiffnesses):
    '''FaceGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetModalAnalysesAtStiffnesses.TYPE'):
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
    def face_gears_modal_analyses_at_stiffnesses(self) -> 'List[_3835.FaceGearModalAnalysesAtStiffnesses]':
        '''List[FaceGearModalAnalysesAtStiffnesses]: 'FaceGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsModalAnalysesAtStiffnesses, constructor.new(_3835.FaceGearModalAnalysesAtStiffnesses))
        return value

    @property
    def face_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_3834.FaceGearMeshModalAnalysesAtStiffnesses]':
        '''List[FaceGearMeshModalAnalysesAtStiffnesses]: 'FaceMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesModalAnalysesAtStiffnesses, constructor.new(_3834.FaceGearMeshModalAnalysesAtStiffnesses))
        return value
