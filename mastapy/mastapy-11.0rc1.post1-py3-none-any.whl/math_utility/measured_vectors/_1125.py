'''_1125.py

VectorWithLinearAndAngularComponents
'''


from mastapy._internal import constructor, conversion
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_VECTOR_WITH_LINEAR_AND_ANGULAR_COMPONENTS = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'VectorWithLinearAndAngularComponents')


__docformat__ = 'restructuredtext en'
__all__ = ('VectorWithLinearAndAngularComponents',)


class VectorWithLinearAndAngularComponents(_0.APIBase):
    '''VectorWithLinearAndAngularComponents

    This is a mastapy class.
    '''

    TYPE = _VECTOR_WITH_LINEAR_AND_ANGULAR_COMPONENTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VectorWithLinearAndAngularComponents.TYPE'):
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
    def linear(self) -> 'Vector3D':
        '''Vector3D: 'Linear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Linear)
        return value

    @property
    def angular(self) -> 'Vector3D':
        '''Vector3D: 'Angular' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Angular)
        return value
