'''_1061.py

Vector2D
'''


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_VECTOR_2D = python_net_import('SMT.MastaAPI.MathUtility', 'Vector2D')


__docformat__ = 'restructuredtext en'
__all__ = ('Vector2D',)


class Vector2D:
    '''Vector2D

    This is a mastapy class.
    '''

    TYPE = _VECTOR_2D

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Vector2D.TYPE'):
        self.wrapped = instance_to_wrap
        self._freeze()

    __frozen = False

    def __setattr__(self, attr, value):
        prop = getattr(self.__class__, attr, None)
        if isinstance(prop, property):
            prop.fset(self, value)
        else:
            if self.__frozen and attr not in self.__dict__:
                raise AttributeError((
                    'Attempted to set unknown '
                    'attribute: \'{}\''.format(attr))) from None

            super().__setattr__(attr, value)

    def __delattr__(self, name):
        raise AttributeError(
            'Cannot delete the attributes of a mastapy object.') from None

    def _freeze(self):
        self.__frozen = True

    @staticmethod
    def op_subtraction(a: 'Vector2D', b: 'Vector2D') -> 'Vector2D':
        ''' 'op_Subtraction' is the original name of this method.

        Args:
            a (mastapy.math_utility.Vector2D)
            b (mastapy.math_utility.Vector2D)

        Returns:
            mastapy.math_utility.Vector2D
        '''

        method_result = Vector2D.TYPE.op_Subtraction(a.wrapped if a else None, b.wrapped if b else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    @staticmethod
    def op_addition(a: 'Vector2D', b: 'Vector2D') -> 'Vector2D':
        ''' 'op_Addition' is the original name of this method.

        Args:
            a (mastapy.math_utility.Vector2D)
            b (mastapy.math_utility.Vector2D)

        Returns:
            mastapy.math_utility.Vector2D
        '''

        method_result = Vector2D.TYPE.op_Addition(a.wrapped if a else None, b.wrapped if b else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def magnitude(self) -> 'float':
        ''' 'Magnitude' is the original name of this method.

        Returns:
            float
        '''

        method_result = self.wrapped.Magnitude()
        return method_result
