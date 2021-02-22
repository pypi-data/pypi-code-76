'''_4828.py

ModalAnalysisOptions
'''


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4806
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisOptions',)


class ModalAnalysisOptions(_0.APIBase):
    '''ModalAnalysisOptions

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_modes(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfModes' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfModes) if self.wrapped.NumberOfModes else None

    @number_of_modes.setter
    def number_of_modes(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.NumberOfModes = value

    @property
    def minimum_mode_frequency(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MinimumModeFrequency' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MinimumModeFrequency) if self.wrapped.MinimumModeFrequency else None

    @minimum_mode_frequency.setter
    def minimum_mode_frequency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MinimumModeFrequency = value

    @property
    def maximum_mode_frequency(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaximumModeFrequency' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaximumModeFrequency) if self.wrapped.MaximumModeFrequency else None

    @maximum_mode_frequency.setter
    def maximum_mode_frequency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.MaximumModeFrequency = value

    @property
    def frequency_response_options_for_reports(self) -> '_4806.FrequencyResponseAnalysisOptions':
        '''FrequencyResponseAnalysisOptions: 'FrequencyResponseOptionsForReports' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4806.FrequencyResponseAnalysisOptions)(self.wrapped.FrequencyResponseOptionsForReports) if self.wrapped.FrequencyResponseOptionsForReports else None
