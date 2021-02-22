'''_743.py

HypoidAdvancedLibrary
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_HYPOID_ADVANCED_LIBRARY = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'HypoidAdvancedLibrary')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidAdvancedLibrary',)


class HypoidAdvancedLibrary(_0.APIBase):
    '''HypoidAdvancedLibrary

    This is a mastapy class.
    '''

    TYPE = _HYPOID_ADVANCED_LIBRARY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidAdvancedLibrary.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def wheel_inner_blade_angle_convex(self) -> 'float':
        '''float: 'WheelInnerBladeAngleConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelInnerBladeAngleConvex

    @property
    def wheel_outer_blade_angle_concave(self) -> 'float':
        '''float: 'WheelOuterBladeAngleConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelOuterBladeAngleConcave
