'''_352.py

BiasModification
'''


from mastapy._internal import constructor
from mastapy.gears.micro_geometry import _361
from mastapy._internal.python_net import python_net_import

_BIAS_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'BiasModification')


__docformat__ = 'restructuredtext en'
__all__ = ('BiasModification',)


class BiasModification(_361.Modification):
    '''BiasModification

    This is a mastapy class.
    '''

    TYPE = _BIAS_MODIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BiasModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lead_evaluation_upper_limit_factor(self) -> 'float':
        '''float: 'LeadEvaluationUpperLimitFactor' is the original name of this property.'''

        return self.wrapped.LeadEvaluationUpperLimitFactor

    @lead_evaluation_upper_limit_factor.setter
    def lead_evaluation_upper_limit_factor(self, value: 'float'):
        self.wrapped.LeadEvaluationUpperLimitFactor = float(value) if value else 0.0

    @property
    def lead_evaluation_lower_limit_factor(self) -> 'float':
        '''float: 'LeadEvaluationLowerLimitFactor' is the original name of this property.'''

        return self.wrapped.LeadEvaluationLowerLimitFactor

    @lead_evaluation_lower_limit_factor.setter
    def lead_evaluation_lower_limit_factor(self, value: 'float'):
        self.wrapped.LeadEvaluationLowerLimitFactor = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_factor(self) -> 'float':
        '''float: 'ProfileEvaluationUpperLimitFactor' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationUpperLimitFactor

    @profile_evaluation_upper_limit_factor.setter
    def profile_evaluation_upper_limit_factor(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitFactor = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_factor(self) -> 'float':
        '''float: 'ProfileEvaluationLowerLimitFactor' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationLowerLimitFactor

    @profile_evaluation_lower_limit_factor.setter
    def profile_evaluation_lower_limit_factor(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitFactor = float(value) if value else 0.0

    @property
    def relief_at_upper_limit(self) -> 'float':
        '''float: 'ReliefAtUpperLimit' is the original name of this property.'''

        return self.wrapped.ReliefAtUpperLimit

    @relief_at_upper_limit.setter
    def relief_at_upper_limit(self, value: 'float'):
        self.wrapped.ReliefAtUpperLimit = float(value) if value else 0.0

    @property
    def relief_at_lower_limit(self) -> 'float':
        '''float: 'ReliefAtLowerLimit' is the original name of this property.'''

        return self.wrapped.ReliefAtLowerLimit

    @relief_at_lower_limit.setter
    def relief_at_lower_limit(self, value: 'float'):
        self.wrapped.ReliefAtLowerLimit = float(value) if value else 0.0

    @property
    def profile_factor_for_0_bias_relief(self) -> 'float':
        '''float: 'ProfileFactorFor0BiasRelief' is the original name of this property.'''

        return self.wrapped.ProfileFactorFor0BiasRelief

    @profile_factor_for_0_bias_relief.setter
    def profile_factor_for_0_bias_relief(self, value: 'float'):
        self.wrapped.ProfileFactorFor0BiasRelief = float(value) if value else 0.0
