'''_4706.py

PulleyCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2261, _2258
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4577
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4657
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'PulleyCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundModalAnalysisAtASpeed',)


class PulleyCompoundModalAnalysisAtASpeed(_4657.CouplingHalfCompoundModalAnalysisAtASpeed):
    '''PulleyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2261.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4577.PulleyModalAnalysisAtASpeed]':
        '''List[PulleyModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4577.PulleyModalAnalysisAtASpeed))
        return value

    @property
    def component_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4577.PulleyModalAnalysisAtASpeed]':
        '''List[PulleyModalAnalysisAtASpeed]: 'ComponentModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisAtASpeedLoadCases, constructor.new(_4577.PulleyModalAnalysisAtASpeed))
        return value
