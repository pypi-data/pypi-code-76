'''_6206.py

ImportedFEComponentLoadCase
'''


from mastapy.system_model.imported_fes import _1968, _1992
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model import _2058
from mastapy.system_model.analyses_and_results.static_loads import _6117
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ImportedFEComponentLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentLoadCase',)


class ImportedFEComponentLoadCase(_6117.AbstractShaftOrHousingLoadCase):
    '''ImportedFEComponentLoadCase

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_source(self) -> '_1968.AngleSource':
        '''AngleSource: 'AngleSource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.AngleSource)
        return constructor.new(_1968.AngleSource)(value) if value else None

    @property
    def angle(self) -> 'float':
        '''float: 'Angle' is the original name of this property.'''

        return self.wrapped.Angle

    @angle.setter
    def angle(self, value: 'float'):
        self.wrapped.Angle = float(value) if value else 0.0

    @property
    def active_angle_index(self) -> 'list_with_selected_item.ListWithSelectedItem_int':
        '''list_with_selected_item.ListWithSelectedItem_int: 'ActiveAngleIndex' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_int)(self.wrapped.ActiveAngleIndex) if self.wrapped.ActiveAngleIndex else None

    @active_angle_index.setter
    def active_angle_index(self, value: 'list_with_selected_item.ListWithSelectedItem_int.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.ActiveAngleIndex = value

    @property
    def stiffness_scaling_factor(self) -> 'float':
        '''float: 'StiffnessScalingFactor' is the original name of this property.'''

        return self.wrapped.StiffnessScalingFactor

    @stiffness_scaling_factor.setter
    def stiffness_scaling_factor(self, value: 'float'):
        self.wrapped.StiffnessScalingFactor = float(value) if value else 0.0

    @property
    def mass_scaling_factor(self) -> 'float':
        '''float: 'MassScalingFactor' is the original name of this property.'''

        return self.wrapped.MassScalingFactor

    @mass_scaling_factor.setter
    def mass_scaling_factor(self, value: 'float'):
        self.wrapped.MassScalingFactor = float(value) if value else 0.0

    @property
    def active_imported_fe(self) -> 'list_with_selected_item.ListWithSelectedItem_ImportedFE':
        '''list_with_selected_item.ListWithSelectedItem_ImportedFE: 'ActiveImportedFE' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ImportedFE)(self.wrapped.ActiveImportedFE) if self.wrapped.ActiveImportedFE else None

    @active_imported_fe.setter
    def active_imported_fe(self, value: 'list_with_selected_item.ListWithSelectedItem_ImportedFE.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ImportedFE.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ImportedFE.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.ActiveImportedFE = value

    @property
    def override_active_fe(self) -> 'bool':
        '''bool: 'OverrideActiveFE' is the original name of this property.'''

        return self.wrapped.OverrideActiveFE

    @override_active_fe.setter
    def override_active_fe(self, value: 'bool'):
        self.wrapped.OverrideActiveFE = bool(value) if value else False

    @property
    def component_design(self) -> '_2058.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2058.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
