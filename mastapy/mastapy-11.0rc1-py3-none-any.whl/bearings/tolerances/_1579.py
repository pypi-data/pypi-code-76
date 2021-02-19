'''_1579.py

RoundnessSpecification
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.tolerances import _1580, _1577
from mastapy.utility import _1152
from mastapy._internal.python_net import python_net_import

_ROUNDNESS_SPECIFICATION = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'RoundnessSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('RoundnessSpecification',)


class RoundnessSpecification(_1152.IndependentReportablePropertiesBase['RoundnessSpecification']):
    '''RoundnessSpecification

    This is a mastapy class.
    '''

    TYPE = _ROUNDNESS_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RoundnessSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_deviation_from_round(self) -> 'float':
        '''float: 'MaximumDeviationFromRound' is the original name of this property.'''

        return self.wrapped.MaximumDeviationFromRound

    @maximum_deviation_from_round.setter
    def maximum_deviation_from_round(self, value: 'float'):
        self.wrapped.MaximumDeviationFromRound = float(value) if value else 0.0

    @property
    def angle_of_first_max_deviation_from_round(self) -> 'float':
        '''float: 'AngleOfFirstMaxDeviationFromRound' is the original name of this property.'''

        return self.wrapped.AngleOfFirstMaxDeviationFromRound

    @angle_of_first_max_deviation_from_round.setter
    def angle_of_first_max_deviation_from_round(self, value: 'float'):
        self.wrapped.AngleOfFirstMaxDeviationFromRound = float(value) if value else 0.0

    @property
    def number_of_lobes(self) -> 'int':
        '''int: 'NumberOfLobes' is the original name of this property.'''

        return self.wrapped.NumberOfLobes

    @number_of_lobes.setter
    def number_of_lobes(self, value: 'int'):
        self.wrapped.NumberOfLobes = int(value) if value else 0

    @property
    def specification_type(self) -> '_1580.RoundnessSpecificationType':
        '''RoundnessSpecificationType: 'SpecificationType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SpecificationType)
        return constructor.new(_1580.RoundnessSpecificationType)(value) if value else None

    @specification_type.setter
    def specification_type(self, value: '_1580.RoundnessSpecificationType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpecificationType = value

    @property
    def roundness_distribution(self) -> 'List[_1577.RaceRoundnessAtAngle]':
        '''List[RaceRoundnessAtAngle]: 'RoundnessDistribution' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RoundnessDistribution, constructor.new(_1577.RaceRoundnessAtAngle))
        return value
