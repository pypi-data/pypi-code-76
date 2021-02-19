'''_416.py

MicroGeometryInputsLead
'''


from mastapy.math_utility import _1063
from mastapy._internal import constructor
from mastapy.math_utility.measured_ranges import _1138
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical import _415, _414
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_INPUTS_LEAD = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'MicroGeometryInputsLead')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryInputsLead',)


class MicroGeometryInputsLead(_415.MicroGeometryInputs['_414.LeadModificationSegment']):
    '''MicroGeometryInputsLead

    This is a mastapy class.
    '''

    TYPE = _MICRO_GEOMETRY_INPUTS_LEAD

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryInputsLead.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lead_micro_geometry_range(self) -> '_1063.Range':
        '''Range: 'LeadMicroGeometryRange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1063.Range.TYPE not in self.wrapped.LeadMicroGeometryRange.__class__.__mro__:
            raise CastException('Failed to cast lead_micro_geometry_range to Range. Expected: {}.'.format(self.wrapped.LeadMicroGeometryRange.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LeadMicroGeometryRange.__class__)(self.wrapped.LeadMicroGeometryRange) if self.wrapped.LeadMicroGeometryRange else None

    @property
    def number_of_lead_segments(self) -> 'int':
        '''int: 'NumberOfLeadSegments' is the original name of this property.'''

        return self.wrapped.NumberOfLeadSegments

    @number_of_lead_segments.setter
    def number_of_lead_segments(self, value: 'int'):
        self.wrapped.NumberOfLeadSegments = int(value) if value else 0
