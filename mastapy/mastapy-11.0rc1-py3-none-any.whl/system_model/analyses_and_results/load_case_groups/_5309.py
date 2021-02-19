'''_5309.py

SystemOptimisationGearSet
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SYSTEM_OPTIMISATION_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'SystemOptimisationGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemOptimisationGearSet',)


class SystemOptimisationGearSet(_0.APIBase):
    '''SystemOptimisationGearSet

    This is a mastapy class.
    '''

    TYPE = _SYSTEM_OPTIMISATION_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SystemOptimisationGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def number_of_candidate_designs(self) -> 'int':
        '''int: 'NumberOfCandidateDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfCandidateDesigns

    @property
    def design_with_highest_number_of_pinion_teeth(self) -> 'str':
        '''str: 'DesignWithHighestNumberOfPinionTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DesignWithHighestNumberOfPinionTeeth

    @property
    def design_with_lowest_number_of_pinion_teeth(self) -> 'str':
        '''str: 'DesignWithLowestNumberOfPinionTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DesignWithLowestNumberOfPinionTeeth

    @property
    def create_designs(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateDesigns

    @property
    def create_designs_dont_attempt_to_fix(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateDesignsDontAttemptToFix' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateDesignsDontAttemptToFix
