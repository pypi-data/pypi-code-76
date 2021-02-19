'''_1481.py

FEModel
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
    _1507, _1509, _1508, _1504,
    _1510, _1506, _1505, _1503,
    _1512, _1499, _1498, _1502,
    _1513
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_MODEL = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'FEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('FEModel',)


class FEModel(_0.APIBase):
    '''FEModel

    This is a mastapy class.
    '''

    TYPE = _FE_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def original_file_path(self) -> 'str':
        '''str: 'OriginalFilePath' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OriginalFilePath

    @property
    def edge_angle_tolerance(self) -> 'float':
        '''float: 'EdgeAngleTolerance' is the original name of this property.'''

        return self.wrapped.EdgeAngleTolerance

    @edge_angle_tolerance.setter
    def edge_angle_tolerance(self, value: 'float'):
        self.wrapped.EdgeAngleTolerance = float(value) if value else 0.0

    @property
    def number_of_nodes(self) -> 'int':
        '''int: 'NumberOfNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfNodes

    @property
    def number_of_elements(self) -> 'int':
        '''int: 'NumberOfElements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfElements

    @property
    def model_length_unit(self) -> 'str':
        '''str: 'ModelLengthUnit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModelLengthUnit

    @property
    def model_force_unit(self) -> 'str':
        '''str: 'ModelForceUnit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModelForceUnit

    @property
    def add_new_material(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'AddNewMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddNewMaterial

    @property
    def change_interpolation_constraints_to_distributing(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ChangeInterpolationConstraintsToDistributing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeInterpolationConstraintsToDistributing

    @property
    def rigid_element_properties(self) -> 'List[_1507.ElementPropertiesRigid]':
        '''List[ElementPropertiesRigid]: 'RigidElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RigidElementProperties, constructor.new(_1507.ElementPropertiesRigid))
        return value

    @property
    def solid_element_properties(self) -> 'List[_1509.ElementPropertiesSolid]':
        '''List[ElementPropertiesSolid]: 'SolidElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SolidElementProperties, constructor.new(_1509.ElementPropertiesSolid))
        return value

    @property
    def shell_element_properties(self) -> 'List[_1508.ElementPropertiesShell]':
        '''List[ElementPropertiesShell]: 'ShellElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShellElementProperties, constructor.new(_1508.ElementPropertiesShell))
        return value

    @property
    def beam_element_properties(self) -> 'List[_1504.ElementPropertiesBeam]':
        '''List[ElementPropertiesBeam]: 'BeamElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeamElementProperties, constructor.new(_1504.ElementPropertiesBeam))
        return value

    @property
    def spring_dashpot_element_properties(self) -> 'List[_1510.ElementPropertiesSpringDashpot]':
        '''List[ElementPropertiesSpringDashpot]: 'SpringDashpotElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDashpotElementProperties, constructor.new(_1510.ElementPropertiesSpringDashpot))
        return value

    @property
    def mass_element_properties(self) -> 'List[_1506.ElementPropertiesMass]':
        '''List[ElementPropertiesMass]: 'MassElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassElementProperties, constructor.new(_1506.ElementPropertiesMass))
        return value

    @property
    def interface_element_properties(self) -> 'List[_1505.ElementPropertiesInterface]':
        '''List[ElementPropertiesInterface]: 'InterfaceElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InterfaceElementProperties, constructor.new(_1505.ElementPropertiesInterface))
        return value

    @property
    def other_element_properties(self) -> 'List[_1503.ElementPropertiesBase]':
        '''List[ElementPropertiesBase]: 'OtherElementProperties' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OtherElementProperties, constructor.new(_1503.ElementPropertiesBase))
        return value

    @property
    def materials(self) -> 'List[_1512.MaterialPropertiesReporting]':
        '''List[MaterialPropertiesReporting]: 'Materials' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Materials, constructor.new(_1512.MaterialPropertiesReporting))
        return value

    @property
    def coordinate_systems(self) -> 'List[_1499.CoordinateSystemReporting]':
        '''List[CoordinateSystemReporting]: 'CoordinateSystems' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CoordinateSystems, constructor.new(_1499.CoordinateSystemReporting))
        return value

    @property
    def contact_pairs(self) -> 'List[_1498.ContactPairReporting]':
        '''List[ContactPairReporting]: 'ContactPairs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ContactPairs, constructor.new(_1498.ContactPairReporting))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def get_all_element_details(self) -> '_1502.ElementDetailsForFEModel':
        ''' 'GetAllElementDetails' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementDetailsForFEModel
        '''

        method_result = self.wrapped.GetAllElementDetails()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def get_all_node_details(self) -> '_1513.NodeDetailsForFEModel':
        ''' 'GetAllNodeDetails' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.NodeDetailsForFEModel
        '''

        method_result = self.wrapped.GetAllNodeDetails()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

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
