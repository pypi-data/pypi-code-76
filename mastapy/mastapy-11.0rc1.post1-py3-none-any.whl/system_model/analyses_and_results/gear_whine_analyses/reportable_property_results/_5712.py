'''_5712.py

ResultsForResponseOfANodeOnAHarmonic
'''


from typing import List

from mastapy.system_model.analyses_and_results.gear_whine_analyses.reportable_property_results import _5713, _5703
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'ResultsForResponseOfANodeOnAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForResponseOfANodeOnAHarmonic',)


class ResultsForResponseOfANodeOnAHarmonic(_0.APIBase):
    '''ResultsForResponseOfANodeOnAHarmonic

    This is a mastapy class.
    '''

    TYPE = _RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ResultsForResponseOfANodeOnAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def x(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'X' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.X) if self.wrapped.X else None

    @property
    def y(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'Y' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.Y) if self.wrapped.Y else None

    @property
    def z(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'Z' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.Z) if self.wrapped.Z else None

    @property
    def linear_magnitude(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'LinearMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.LinearMagnitude) if self.wrapped.LinearMagnitude else None

    @property
    def radial_magnitude(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'RadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.RadialMagnitude) if self.wrapped.RadialMagnitude else None

    @property
    def theta_x(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'ThetaX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.ThetaX) if self.wrapped.ThetaX else None

    @property
    def theta_y(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'ThetaY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.ThetaY) if self.wrapped.ThetaY else None

    @property
    def theta_z(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'ThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.ThetaZ) if self.wrapped.ThetaZ else None

    @property
    def angular_magnitude(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'AngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.AngularMagnitude) if self.wrapped.AngularMagnitude else None

    @property
    def radial_angular_magnitude(self) -> '_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        '''ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'RadialAngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5713.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic)(self.wrapped.RadialAngularMagnitude) if self.wrapped.RadialAngularMagnitude else None

    @property
    def result_at_reference_speed(self) -> '_5703.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic':
        '''DatapointForResponseOfANodeAtAFrequencyOnAHarmonic: 'ResultAtReferenceSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5703.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic)(self.wrapped.ResultAtReferenceSpeed) if self.wrapped.ResultAtReferenceSpeed else None

    @property
    def data_points(self) -> 'List[_5703.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic]':
        '''List[DatapointForResponseOfANodeAtAFrequencyOnAHarmonic]: 'DataPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DataPoints, constructor.new(_5703.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic))
        return value
