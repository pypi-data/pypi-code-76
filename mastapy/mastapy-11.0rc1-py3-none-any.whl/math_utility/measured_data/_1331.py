'''_1331.py

TwodimensionalFunctionLookupTable
'''


from mastapy.math_utility.measured_data import _1329
from mastapy._internal.python_net import python_net_import

_TWODIMENSIONAL_FUNCTION_LOOKUP_TABLE = python_net_import('SMT.MastaAPI.MathUtility.MeasuredData', 'TwodimensionalFunctionLookupTable')


__docformat__ = 'restructuredtext en'
__all__ = ('TwodimensionalFunctionLookupTable',)


class TwodimensionalFunctionLookupTable(_1329.LookupTableBase['TwodimensionalFunctionLookupTable']):
    '''TwodimensionalFunctionLookupTable

    This is a mastapy class.
    '''

    TYPE = _TWODIMENSIONAL_FUNCTION_LOOKUP_TABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TwodimensionalFunctionLookupTable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
