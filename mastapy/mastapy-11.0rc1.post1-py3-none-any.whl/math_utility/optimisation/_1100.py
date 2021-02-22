'''_1100.py

Optimisable
'''


from mastapy.math_utility.optimisation import _1096
from mastapy._internal.python_net import python_net_import

_OPTIMISABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'Optimisable')


__docformat__ = 'restructuredtext en'
__all__ = ('Optimisable',)


class Optimisable(_1096.AbstractOptimisable):
    '''Optimisable

    This is a mastapy class.
    '''

    TYPE = _OPTIMISABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Optimisable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
