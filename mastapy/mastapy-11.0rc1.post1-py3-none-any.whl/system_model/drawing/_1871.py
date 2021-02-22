'''_1871.py

DynamicAnalysisViewable
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model.drawing import _1870, _1878
from mastapy.system_model.analyses_and_results.system_deflections import _2393
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3127
from mastapy.system_model.analyses_and_results.rotor_dynamics import _3274
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3859
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4105
from mastapy.system_model.analyses_and_results.modal_analyses import _4840
from mastapy.system_model.analyses_and_results.mbd_analyses import _5110
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5395
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5912
from mastapy._internal.python_net import python_net_import

_DYNAMIC_ANALYSIS_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'DynamicAnalysisViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicAnalysisViewable',)


class DynamicAnalysisViewable(_1878.PartAnalysisCaseWithContourViewable):
    '''DynamicAnalysisViewable

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_ANALYSIS_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicAnalysisViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fe_results(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'FEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FEResults

    @property
    def contour_draw_style(self) -> '_1870.ContourDrawStyle':
        '''ContourDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1870.ContourDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ContourDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_system_deflection_draw_style(self) -> '_2393.SystemDeflectionDrawStyle':
        '''SystemDeflectionDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2393.SystemDeflectionDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to SystemDeflectionDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_steady_state_synchronous_response_draw_style(self) -> '_3127.SteadyStateSynchronousResponseDrawStyle':
        '''SteadyStateSynchronousResponseDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3127.SteadyStateSynchronousResponseDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to SteadyStateSynchronousResponseDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_rotor_dynamics_draw_style(self) -> '_3274.RotorDynamicsDrawStyle':
        '''RotorDynamicsDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3274.RotorDynamicsDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to RotorDynamicsDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_modal_analysis_at_stiffnesses_draw_style(self) -> '_3859.ModalAnalysisAtStiffnessesDrawStyle':
        '''ModalAnalysisAtStiffnessesDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3859.ModalAnalysisAtStiffnessesDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ModalAnalysisAtStiffnessesDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_modal_analysis_at_speeds_draw_style(self) -> '_4105.ModalAnalysisAtSpeedsDrawStyle':
        '''ModalAnalysisAtSpeedsDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4105.ModalAnalysisAtSpeedsDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ModalAnalysisAtSpeedsDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_modal_analysis_draw_style(self) -> '_4840.ModalAnalysisDrawStyle':
        '''ModalAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4840.ModalAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ModalAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_mbd_analysis_draw_style(self) -> '_5110.MBDAnalysisDrawStyle':
        '''MBDAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5110.MBDAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to MBDAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_harmonic_analysis_draw_style(self) -> '_5395.HarmonicAnalysisDrawStyle':
        '''HarmonicAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5395.HarmonicAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to HarmonicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def contour_draw_style_of_type_dynamic_analysis_draw_style(self) -> '_5912.DynamicAnalysisDrawStyle':
        '''DynamicAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5912.DynamicAnalysisDrawStyle.TYPE not in self.wrapped.ContourDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to DynamicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.ContourDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ContourDrawStyle.__class__)(self.wrapped.ContourDrawStyle) if self.wrapped.ContourDrawStyle else None

    @property
    def dynamic_analysis_draw_style(self) -> '_5912.DynamicAnalysisDrawStyle':
        '''DynamicAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5912.DynamicAnalysisDrawStyle.TYPE not in self.wrapped.DynamicAnalysisDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to DynamicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.DynamicAnalysisDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DynamicAnalysisDrawStyle.__class__)(self.wrapped.DynamicAnalysisDrawStyle) if self.wrapped.DynamicAnalysisDrawStyle else None

    @property
    def dynamic_analysis_draw_style_of_type_modal_analysis_draw_style(self) -> '_4840.ModalAnalysisDrawStyle':
        '''ModalAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4840.ModalAnalysisDrawStyle.TYPE not in self.wrapped.DynamicAnalysisDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to ModalAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.DynamicAnalysisDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DynamicAnalysisDrawStyle.__class__)(self.wrapped.DynamicAnalysisDrawStyle) if self.wrapped.DynamicAnalysisDrawStyle else None

    @property
    def dynamic_analysis_draw_style_of_type_harmonic_analysis_draw_style(self) -> '_5395.HarmonicAnalysisDrawStyle':
        '''HarmonicAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5395.HarmonicAnalysisDrawStyle.TYPE not in self.wrapped.DynamicAnalysisDrawStyle.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to HarmonicAnalysisDrawStyle. Expected: {}.'.format(self.wrapped.DynamicAnalysisDrawStyle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.DynamicAnalysisDrawStyle.__class__)(self.wrapped.DynamicAnalysisDrawStyle) if self.wrapped.DynamicAnalysisDrawStyle else None
