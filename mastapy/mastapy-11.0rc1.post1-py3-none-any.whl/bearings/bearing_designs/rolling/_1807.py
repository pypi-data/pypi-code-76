'''_1807.py

ToroidalRollerBearing
'''


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1782
from mastapy._internal.python_net import python_net_import

_TOROIDAL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'ToroidalRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ToroidalRollerBearing',)


class ToroidalRollerBearing(_1782.BarrelRollerBearing):
    '''ToroidalRollerBearing

    This is a mastapy class.
    '''

    TYPE = _TOROIDAL_ROLLER_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ToroidalRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def snap_ring_width(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SnapRingWidth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SnapRingWidth) if self.wrapped.SnapRingWidth else None

    @snap_ring_width.setter
    def snap_ring_width(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SnapRingWidth = value

    @property
    def snap_ring_offset_from_element(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SnapRingOffsetFromElement' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SnapRingOffsetFromElement) if self.wrapped.SnapRingOffsetFromElement else None

    @snap_ring_offset_from_element.setter
    def snap_ring_offset_from_element(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SnapRingOffsetFromElement = value

    @property
    def axial_displacement_capability(self) -> 'float':
        '''float: 'AxialDisplacementCapability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialDisplacementCapability

    @property
    def axial_displacement_capability_towards_snap_ring(self) -> 'float':
        '''float: 'AxialDisplacementCapabilityTowardsSnapRing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialDisplacementCapabilityTowardsSnapRing
