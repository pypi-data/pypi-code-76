'''_1994.py

ImportedFEGearMeshLink
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.imported_fes import _2004, _2015
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_GEAR_MESH_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEGearMeshLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEGearMeshLink',)


class ImportedFEGearMeshLink(_2015.MultiAngleConnectionLink):
    '''ImportedFEGearMeshLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_GEAR_MESH_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEGearMeshLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def use_active_mesh_node_for_reference_imported_fe_node_for_misalignments(self) -> 'bool':
        '''bool: 'UseActiveMeshNodeForReferenceImportedFENodeForMisalignments' is the original name of this property.'''

        return self.wrapped.UseActiveMeshNodeForReferenceImportedFENodeForMisalignments

    @use_active_mesh_node_for_reference_imported_fe_node_for_misalignments.setter
    def use_active_mesh_node_for_reference_imported_fe_node_for_misalignments(self, value: 'bool'):
        self.wrapped.UseActiveMeshNodeForReferenceImportedFENodeForMisalignments = bool(value) if value else False

    @property
    def reference_imported_fe_node_for_misalignments(self) -> 'list_with_selected_item.ListWithSelectedItem_ImportedFEStiffnessNode':
        '''list_with_selected_item.ListWithSelectedItem_ImportedFEStiffnessNode: 'ReferenceImportedFENodeForMisalignments' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ImportedFEStiffnessNode)(self.wrapped.ReferenceImportedFENodeForMisalignments) if self.wrapped.ReferenceImportedFENodeForMisalignments else None

    @reference_imported_fe_node_for_misalignments.setter
    def reference_imported_fe_node_for_misalignments(self, value: 'list_with_selected_item.ListWithSelectedItem_ImportedFEStiffnessNode.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ImportedFEStiffnessNode.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ImportedFEStiffnessNode.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ReferenceImportedFENodeForMisalignments = value
