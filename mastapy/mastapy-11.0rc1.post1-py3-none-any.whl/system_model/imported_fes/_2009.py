'''_2009.py

ImportedFEWithSelectionModalAnalysis
'''


from typing import Callable, List

from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses import _1485, _1476
from mastapy.nodal_analysis import _1389
from mastapy.system_model.imported_fes import _2006
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_WITH_SELECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEWithSelectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEWithSelectionModalAnalysis',)


class ImportedFEWithSelectionModalAnalysis(_2006.ImportedFEWithSelection):
    '''ImportedFEWithSelectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_WITH_SELECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEWithSelectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def max_displacement_scaling(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaxDisplacementScaling' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaxDisplacementScaling) if self.wrapped.MaxDisplacementScaling else None

    @max_displacement_scaling.setter
    def max_displacement_scaling(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MaxDisplacementScaling = value

    @property
    def calculate_full_fe_modes(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateFullFEModes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateFullFEModes

    @property
    def mode_to_draw(self) -> 'list_with_selected_item.ListWithSelectedItem_int':
        '''list_with_selected_item.ListWithSelectedItem_int: 'ModeToDraw' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_int)(self.wrapped.ModeToDraw) if self.wrapped.ModeToDraw else None

    @mode_to_draw.setter
    def mode_to_draw(self, value: 'list_with_selected_item.ListWithSelectedItem_int.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.ModeToDraw = value

    @property
    def show_full_fe_mode_shapes(self) -> 'bool':
        '''bool: 'ShowFullFEModeShapes' is the original name of this property.'''

        return self.wrapped.ShowFullFEModeShapes

    @show_full_fe_mode_shapes.setter
    def show_full_fe_mode_shapes(self, value: 'bool'):
        self.wrapped.ShowFullFEModeShapes = bool(value) if value else False

    @property
    def modal_draw_style(self) -> '_1485.FEModelModalAnalysisDrawStyle':
        '''FEModelModalAnalysisDrawStyle: 'ModalDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1485.FEModelModalAnalysisDrawStyle)(self.wrapped.ModalDrawStyle) if self.wrapped.ModalDrawStyle else None

    @property
    def eigenvalue_options(self) -> '_1476.EigenvalueOptions':
        '''EigenvalueOptions: 'EigenvalueOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1476.EigenvalueOptions)(self.wrapped.EigenvalueOptions) if self.wrapped.EigenvalueOptions else None

    @property
    def fe_modal_frequencies(self) -> 'List[_1389.FEModalFrequencyComparison]':
        '''List[FEModalFrequencyComparison]: 'FEModalFrequencies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEModalFrequencies, constructor.new(_1389.FEModalFrequencyComparison))
        return value
