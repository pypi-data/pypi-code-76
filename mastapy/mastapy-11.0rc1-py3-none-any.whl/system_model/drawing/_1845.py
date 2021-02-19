'''_1845.py

ContourDrawStyle
'''


from mastapy.utility.enums import _1341
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.drawing import _1847, _1846
from mastapy.geometry import _110
from mastapy._internal.python_net import python_net_import

_CONTOUR_DRAW_STYLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ContourDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('ContourDrawStyle',)


class ContourDrawStyle(_110.DrawStyleBase):
    '''ContourDrawStyle

    This is a mastapy class.
    '''

    TYPE = _CONTOUR_DRAW_STYLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ContourDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contour(self) -> '_1341.ThreeDViewContourOption':
        '''ThreeDViewContourOption: 'Contour' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Contour)
        return constructor.new(_1341.ThreeDViewContourOption)(value) if value else None

    @contour.setter
    def contour(self, value: '_1341.ThreeDViewContourOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Contour = value

    @property
    def show_local_maxima(self) -> 'bool':
        '''bool: 'ShowLocalMaxima' is the original name of this property.'''

        return self.wrapped.ShowLocalMaxima

    @show_local_maxima.setter
    def show_local_maxima(self, value: 'bool'):
        self.wrapped.ShowLocalMaxima = bool(value) if value else False

    @property
    def minimum_peak_value_displacement(self) -> 'float':
        '''float: 'MinimumPeakValueDisplacement' is the original name of this property.'''

        return self.wrapped.MinimumPeakValueDisplacement

    @minimum_peak_value_displacement.setter
    def minimum_peak_value_displacement(self, value: 'float'):
        self.wrapped.MinimumPeakValueDisplacement = float(value) if value else 0.0

    @property
    def minimum_peak_value_stress(self) -> 'float':
        '''float: 'MinimumPeakValueStress' is the original name of this property.'''

        return self.wrapped.MinimumPeakValueStress

    @minimum_peak_value_stress.setter
    def minimum_peak_value_stress(self, value: 'float'):
        self.wrapped.MinimumPeakValueStress = float(value) if value else 0.0

    @property
    def deflection_scaling(self) -> '_1847.ScalingDrawStyle':
        '''ScalingDrawStyle: 'DeflectionScaling' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1847.ScalingDrawStyle)(self.wrapped.DeflectionScaling) if self.wrapped.DeflectionScaling else None

    @property
    def model_view_options(self) -> '_1846.ModelViewOptionsDrawStyle':
        '''ModelViewOptionsDrawStyle: 'ModelViewOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1846.ModelViewOptionsDrawStyle)(self.wrapped.ModelViewOptions) if self.wrapped.ModelViewOptions else None
