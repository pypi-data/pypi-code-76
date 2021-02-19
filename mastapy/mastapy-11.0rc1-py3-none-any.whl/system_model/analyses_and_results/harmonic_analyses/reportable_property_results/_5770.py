'''_5770.py

ResultsForResponseOfAComponentOrSurfaceInAHarmonic
'''


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5772, _5761
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_IN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'ResultsForResponseOfAComponentOrSurfaceInAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForResponseOfAComponentOrSurfaceInAHarmonic',)


class ResultsForResponseOfAComponentOrSurfaceInAHarmonic(_0.APIBase):
    '''ResultsForResponseOfAComponentOrSurfaceInAHarmonic

    This is a mastapy class.
    '''

    TYPE = _RESULTS_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_IN_A_HARMONIC

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultsForResponseOfAComponentOrSurfaceInAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def magnitude(self) -> '_5772.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'Magnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5772.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.Magnitude) if self.wrapped.Magnitude else None

    @property
    def result_at_reference_speed(self) -> '_5761.DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic':
        '''DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic: 'ResultAtReferenceSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5761.DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic)(self.wrapped.ResultAtReferenceSpeed) if self.wrapped.ResultAtReferenceSpeed else None

    @property
    def data_points(self) -> 'List[_5761.DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic]':
        '''List[DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic]: 'DataPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DataPoints, constructor.new(_5761.DatapointForResponseOfAComponentOrSurfaceAtAFrequencyInAHarmonic))
        return value
