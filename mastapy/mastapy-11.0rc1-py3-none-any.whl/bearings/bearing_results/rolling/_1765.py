'''_1765.py

SKFMaximalConstantlyActingAxialLoadResults
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SKF_MAXIMAL_CONSTANTLY_ACTING_AXIAL_LOAD_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'SKFMaximalConstantlyActingAxialLoadResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SKFMaximalConstantlyActingAxialLoadResults',)


class SKFMaximalConstantlyActingAxialLoadResults(_0.APIBase):
    '''SKFMaximalConstantlyActingAxialLoadResults

    This is a mastapy class.
    '''

    TYPE = _SKF_MAXIMAL_CONSTANTLY_ACTING_AXIAL_LOAD_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SKFMaximalConstantlyActingAxialLoadResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def limiting_axial_load_as_a_function_of_diameter(self) -> 'float':
        '''float: 'LimitingAxialLoadAsAFunctionOfDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LimitingAxialLoadAsAFunctionOfDiameter

    @property
    def axial_load(self) -> 'float':
        '''float: 'AxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialLoad

    @property
    def safety_factor(self) -> 'float':
        '''float: 'SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SafetyFactor
