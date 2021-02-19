'''_458.py

SafetyFactorOptimisationResults
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy.gears.rating.cylindrical.optimisation import _459
from mastapy._internal.python_net import python_net_import

_SAFETY_FACTOR_OPTIMISATION_RESULTS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation', 'SafetyFactorOptimisationResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SafetyFactorOptimisationResults',)


T = TypeVar('T', bound='_459.SafetyFactorOptimisationStepResult')


class SafetyFactorOptimisationResults(_0.APIBase, Generic[T]):
    '''SafetyFactorOptimisationResults

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _SAFETY_FACTOR_OPTIMISATION_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SafetyFactorOptimisationResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def values(self) -> 'List[T]':
        '''List[T]: 'Values' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Values, constructor.new(T))
        return value
