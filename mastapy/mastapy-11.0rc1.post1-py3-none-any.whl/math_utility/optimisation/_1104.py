'''_1104.py

ParetoOptimisationFilter
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_FILTER = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationFilter')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationFilter',)


class ParetoOptimisationFilter(_0.APIBase):
    '''ParetoOptimisationFilter

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_FILTER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationFilter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def property_(self) -> 'str':
        '''str: 'Property' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Property
