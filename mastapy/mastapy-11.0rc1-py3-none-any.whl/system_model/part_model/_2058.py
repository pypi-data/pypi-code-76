'''_2058.py

ImportedFEComponent
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.imported_fes import _1992
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.math_utility import _1072
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.part_model import _2039

_STRING = python_net_import('System', 'String')
_IMPORTED_FE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ImportedFEComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponent',)


class ImportedFEComponent(_2039.AbstractShaftOrHousing):
    '''ImportedFEComponent

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def current_fe(self) -> 'list_with_selected_item.ListWithSelectedItem_ImportedFE':
        '''list_with_selected_item.ListWithSelectedItem_ImportedFE: 'CurrentFE' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ImportedFE)(self.wrapped.CurrentFE) if self.wrapped.CurrentFE else None

    @current_fe.setter
    def current_fe(self, value: 'list_with_selected_item.ListWithSelectedItem_ImportedFE.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ImportedFE.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ImportedFE.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.CurrentFE = value

    @property
    def knows_scalar_mass(self) -> 'bool':
        '''bool: 'KnowsScalarMass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.KnowsScalarMass

    @property
    def three_d_node_size(self) -> 'float':
        '''float: 'ThreeDNodeSize' is the original name of this property.'''

        return self.wrapped.ThreeDNodeSize

    @three_d_node_size.setter
    def three_d_node_size(self, value: 'float'):
        self.wrapped.ThreeDNodeSize = float(value) if value else 0.0

    @property
    def default_active_imported_fe(self) -> '_1992.ImportedFE':
        '''ImportedFE: 'DefaultActiveImportedFE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1992.ImportedFE)(self.wrapped.DefaultActiveImportedFE) if self.wrapped.DefaultActiveImportedFE else None

    @property
    def local_coordinate_system(self) -> '_1072.CoordinateSystem3D':
        '''CoordinateSystem3D: 'LocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1072.CoordinateSystem3D)(self.wrapped.LocalCoordinateSystem) if self.wrapped.LocalCoordinateSystem else None

    def add_imported_fe(self) -> '_1992.ImportedFE':
        ''' 'AddImportedFE' is the original name of this method.

        Returns:
            mastapy.system_model.imported_fes.ImportedFE
        '''

        method_result = self.wrapped.AddImportedFE()
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def add_imported_fe_with_name(self, name: 'str') -> '_1992.ImportedFE':
        ''' 'AddImportedFE' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.imported_fes.ImportedFE
        '''

        name = str(name)
        method_result = self.wrapped.AddImportedFE.Overloads[_STRING](name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def select_imported_fe(self, imported_fe: '_1992.ImportedFE'):
        ''' 'SelectImportedFE' is the original name of this method.

        Args:
            imported_fe (mastapy.system_model.imported_fes.ImportedFE)
        '''

        self.wrapped.SelectImportedFE(imported_fe.wrapped if imported_fe else None)

    def remove_imported_fe(self, imported_fe: '_1992.ImportedFE') -> 'bool':
        ''' 'RemoveImportedFE' is the original name of this method.

        Args:
            imported_fe (mastapy.system_model.imported_fes.ImportedFE)

        Returns:
            bool
        '''

        method_result = self.wrapped.RemoveImportedFE(imported_fe.wrapped if imported_fe else None)
        return method_result
