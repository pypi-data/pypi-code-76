'''_2010.py

ImportedFEWithSelectionStaticAnalysis
'''


from typing import Callable, List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.utility.enums import _1356
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis.component_mode_synthesis import _1528
from mastapy.nodal_analysis.dev_tools_analyses import _1487
from mastapy.system_model.imported_fes import _2016, _2006
from mastapy.math_utility.measured_vectors import _1137
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_WITH_SELECTION_STATIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEWithSelectionStaticAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEWithSelectionStaticAnalysis',)


class ImportedFEWithSelectionStaticAnalysis(_2006.ImportedFEWithSelection):
    '''ImportedFEWithSelectionStaticAnalysis

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_WITH_SELECTION_STATIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEWithSelectionStaticAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def reset_forces(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ResetForces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResetForces

    @property
    def reset_displacements(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ResetDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResetDisplacements

    @property
    def temperature_change_from_nominal(self) -> 'float':
        '''float: 'TemperatureChangeFromNominal' is the original name of this property.'''

        return self.wrapped.TemperatureChangeFromNominal

    @temperature_change_from_nominal.setter
    def temperature_change_from_nominal(self, value: 'float'):
        self.wrapped.TemperatureChangeFromNominal = float(value) if value else 0.0

    @property
    def torque_transfer_check(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'TorqueTransferCheck' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueTransferCheck

    @property
    def solve(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'Solve' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Solve

    @property
    def contour_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption: 'ContourOption' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ContourOption, value) if self.wrapped.ContourOption else None

    @contour_option.setter
    def contour_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThreeDViewContourOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ContourOption = value

    @property
    def average_stress_to_nodes(self) -> 'bool':
        '''bool: 'AverageStressToNodes' is the original name of this property.'''

        return self.wrapped.AverageStressToNodes

    @average_stress_to_nodes.setter
    def average_stress_to_nodes(self, value: 'bool'):
        self.wrapped.AverageStressToNodes = bool(value) if value else False

    @property
    def full_fe_results(self) -> '_1528.StaticCMSResults':
        '''StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1528.StaticCMSResults)(self.wrapped.FullFEResults) if self.wrapped.FullFEResults else None

    @property
    def static_draw_style(self) -> '_1487.FEModelStaticAnalysisDrawStyle':
        '''FEModelStaticAnalysisDrawStyle: 'StaticDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1487.FEModelStaticAnalysisDrawStyle)(self.wrapped.StaticDrawStyle) if self.wrapped.StaticDrawStyle else None

    @property
    def boundary_conditions_selected_nodes(self) -> 'List[_2016.NodeBoundaryConditionStaticAnalysis]':
        '''List[NodeBoundaryConditionStaticAnalysis]: 'BoundaryConditionsSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsSelectedNodes, constructor.new(_2016.NodeBoundaryConditionStaticAnalysis))
        return value

    @property
    def boundary_conditions_all_nodes(self) -> 'List[_2016.NodeBoundaryConditionStaticAnalysis]':
        '''List[NodeBoundaryConditionStaticAnalysis]: 'BoundaryConditionsAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsAllNodes, constructor.new(_2016.NodeBoundaryConditionStaticAnalysis))
        return value

    @property
    def force_results(self) -> 'List[_1137.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'ForceResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ForceResults, constructor.new(_1137.VectorWithLinearAndAngularComponents))
        return value

    @property
    def displacement_results(self) -> 'List[_1137.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'DisplacementResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DisplacementResults, constructor.new(_1137.VectorWithLinearAndAngularComponents))
        return value
