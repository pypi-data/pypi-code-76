'''_1073.py

CoordinateSystemEditor
'''


from typing import Callable, List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.math_utility import (
    _1075, _1099, _1074, _1072
)
from mastapy.scripting import _6574
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COORDINATE_SYSTEM_EDITOR = python_net_import('SMT.MastaAPI.MathUtility', 'CoordinateSystemEditor')


__docformat__ = 'restructuredtext en'
__all__ = ('CoordinateSystemEditor',)


class CoordinateSystemEditor(_0.APIBase):
    '''CoordinateSystemEditor

    This is a mastapy class.
    '''

    TYPE = _COORDINATE_SYSTEM_EDITOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoordinateSystemEditor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def has_modified_coordinate_system(self) -> 'bool':
        '''bool: 'HasModifiedCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasModifiedCoordinateSystem

    @property
    def has_modified_coordinate_system_rotation(self) -> 'bool':
        '''bool: 'HasModifiedCoordinateSystemRotation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasModifiedCoordinateSystemRotation

    @property
    def has_modified_coordinate_system_translation(self) -> 'bool':
        '''bool: 'HasModifiedCoordinateSystemTranslation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasModifiedCoordinateSystemTranslation

    @property
    def has_rotation(self) -> 'bool':
        '''bool: 'HasRotation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasRotation

    @property
    def has_translation(self) -> 'bool':
        '''bool: 'HasTranslation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasTranslation

    @property
    def coordinate_system_for_rotation_origin(self) -> '_1075.CoordinateSystemForRotationOrigin':
        '''CoordinateSystemForRotationOrigin: 'CoordinateSystemForRotationOrigin' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CoordinateSystemForRotationOrigin)
        return constructor.new(_1075.CoordinateSystemForRotationOrigin)(value) if value else None

    @coordinate_system_for_rotation_origin.setter
    def coordinate_system_for_rotation_origin(self, value: '_1075.CoordinateSystemForRotationOrigin'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoordinateSystemForRotationOrigin = value

    @property
    def rotation_angle(self) -> 'float':
        '''float: 'RotationAngle' is the original name of this property.'''

        return self.wrapped.RotationAngle

    @rotation_angle.setter
    def rotation_angle(self, value: 'float'):
        self.wrapped.RotationAngle = float(value) if value else 0.0

    @property
    def rotation_axis(self) -> '_1099.RotationAxis':
        '''RotationAxis: 'RotationAxis' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RotationAxis)
        return constructor.new(_1099.RotationAxis)(value) if value else None

    @rotation_axis.setter
    def rotation_axis(self, value: '_1099.RotationAxis'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RotationAxis = value

    @property
    def coordinate_system_for_rotation_axes(self) -> '_1074.CoordinateSystemForRotation':
        '''CoordinateSystemForRotation: 'CoordinateSystemForRotationAxes' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CoordinateSystemForRotationAxes)
        return constructor.new(_1074.CoordinateSystemForRotation)(value) if value else None

    @coordinate_system_for_rotation_axes.setter
    def coordinate_system_for_rotation_axes(self, value: '_1074.CoordinateSystemForRotation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoordinateSystemForRotationAxes = value

    @property
    def apply_rotation(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ApplyRotation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ApplyRotation

    @property
    def update_origin(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'UpdateOrigin' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UpdateOrigin

    @property
    def cancel_pending_changes(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CancelPendingChanges' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CancelPendingChanges

    @property
    def align_to_world_coordinate_system(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AlignToWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AlignToWorldCoordinateSystem

    @property
    def set_local_origin_to_world_origin(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SetLocalOriginToWorldOrigin' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetLocalOriginToWorldOrigin

    @property
    def show_preview(self) -> 'bool':
        '''bool: 'ShowPreview' is the original name of this property.'''

        return self.wrapped.ShowPreview

    @show_preview.setter
    def show_preview(self, value: 'bool'):
        self.wrapped.ShowPreview = bool(value) if value else False

    @property
    def containing_assembly_image(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ContainingAssemblyImage' is the original name of this property.'''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ContainingAssemblyImage) if self.wrapped.ContainingAssemblyImage else None

    @containing_assembly_image.setter
    def containing_assembly_image(self, value: '_6574.SMTBitmap'):
        value = value.wrapped if value else None
        self.wrapped.ContainingAssemblyImage = value

    @property
    def containing_assembly_text(self) -> 'str':
        '''str: 'ContainingAssemblyText' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContainingAssemblyText

    @property
    def root_assembly_text(self) -> 'str':
        '''str: 'RootAssemblyText' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RootAssemblyText

    @property
    def root_assembly_image(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'RootAssemblyImage' is the original name of this property.'''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.RootAssemblyImage) if self.wrapped.RootAssemblyImage else None

    @root_assembly_image.setter
    def root_assembly_image(self, value: '_6574.SMTBitmap'):
        value = value.wrapped if value else None
        self.wrapped.RootAssemblyImage = value

    @property
    def coordinate_system(self) -> '_1072.CoordinateSystem3D':
        '''CoordinateSystem3D: 'CoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1072.CoordinateSystem3D)(self.wrapped.CoordinateSystem) if self.wrapped.CoordinateSystem else None

    @property
    def modified_coordinate_system_for_rotation(self) -> '_1072.CoordinateSystem3D':
        '''CoordinateSystem3D: 'ModifiedCoordinateSystemForRotation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1072.CoordinateSystem3D)(self.wrapped.ModifiedCoordinateSystemForRotation) if self.wrapped.ModifiedCoordinateSystemForRotation else None

    @property
    def modified_coordinate_system_for_translation(self) -> '_1072.CoordinateSystem3D':
        '''CoordinateSystem3D: 'ModifiedCoordinateSystemForTranslation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1072.CoordinateSystem3D)(self.wrapped.ModifiedCoordinateSystemForTranslation) if self.wrapped.ModifiedCoordinateSystemForTranslation else None

    @property
    def translation(self) -> 'Vector3D':
        '''Vector3D: 'Translation' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Translation)
        return value

    @translation.setter
    def translation(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.Translation = value

    @property
    def rotation_origin(self) -> 'Vector3D':
        '''Vector3D: 'RotationOrigin' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.RotationOrigin)
        return value

    @rotation_origin.setter
    def rotation_origin(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.RotationOrigin = value

    @property
    def specified_rotation_axis(self) -> 'Vector3D':
        '''Vector3D: 'SpecifiedRotationAxis' is the original name of this property.'''

        value = conversion.pn_to_mp_vector3d(self.wrapped.SpecifiedRotationAxis)
        return value

    @specified_rotation_axis.setter
    def specified_rotation_axis(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.SpecifiedRotationAxis = value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
