'''_1126.py

OnedimensionalFunctionLookupTable
'''


from mastapy.math_utility.measured_data import _1125
from mastapy._internal.python_net import python_net_import

_ONEDIMENSIONAL_FUNCTION_LOOKUP_TABLE = python_net_import('SMT.MastaAPI.MathUtility.MeasuredData', 'OnedimensionalFunctionLookupTable')


__docformat__ = 'restructuredtext en'
__all__ = ('OnedimensionalFunctionLookupTable',)


class OnedimensionalFunctionLookupTable(_1125.LookupTableBase['OnedimensionalFunctionLookupTable']):
    '''OnedimensionalFunctionLookupTable

    This is a mastapy class.
    '''

    TYPE = _ONEDIMENSIONAL_FUNCTION_LOOKUP_TABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OnedimensionalFunctionLookupTable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
