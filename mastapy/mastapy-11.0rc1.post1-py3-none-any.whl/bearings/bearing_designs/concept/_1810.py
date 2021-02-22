'''_1810.py

ConceptRadialClearanceBearing
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_designs.concept import _1809
from mastapy._internal.python_net import python_net_import

_CONCEPT_RADIAL_CLEARANCE_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Concept', 'ConceptRadialClearanceBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptRadialClearanceBearing',)


class ConceptRadialClearanceBearing(_1809.ConceptClearanceBearing):
    '''ConceptRadialClearanceBearing

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_RADIAL_CLEARANCE_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptRadialClearanceBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_angle(self) -> 'float':
        '''float: 'ContactAngle' is the original name of this property.'''

        return self.wrapped.ContactAngle

    @contact_angle.setter
    def contact_angle(self, value: 'float'):
        self.wrapped.ContactAngle = float(value) if value else 0.0

    @property
    def outer_diameter(self) -> 'float':
        '''float: 'OuterDiameter' is the original name of this property.'''

        return self.wrapped.OuterDiameter

    @outer_diameter.setter
    def outer_diameter(self, value: 'float'):
        self.wrapped.OuterDiameter = float(value) if value else 0.0

    @property
    def bore(self) -> 'float':
        '''float: 'Bore' is the original name of this property.'''

        return self.wrapped.Bore

    @bore.setter
    def bore(self, value: 'float'):
        self.wrapped.Bore = float(value) if value else 0.0

    @property
    def start_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'StartAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.StartAngle) if self.wrapped.StartAngle else None

    @start_angle.setter
    def start_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.StartAngle = value

    @property
    def end_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'EndAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.EndAngle) if self.wrapped.EndAngle else None

    @end_angle.setter
    def end_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.EndAngle = value
