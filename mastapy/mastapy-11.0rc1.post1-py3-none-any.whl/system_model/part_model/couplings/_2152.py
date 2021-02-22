'''_2152.py

RollingRing
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _133
from mastapy.system_model.part_model.couplings import _2141
from mastapy._internal.python_net import python_net_import

_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRing',)


class RollingRing(_2141.CouplingHalf):
    '''RollingRing

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_diameter(self) -> 'float':
        '''float: 'AverageDiameter' is the original name of this property.'''

        return self.wrapped.AverageDiameter

    @average_diameter.setter
    def average_diameter(self, value: 'float'):
        self.wrapped.AverageDiameter = float(value) if value else 0.0

    @property
    def largest_end(self) -> '_133.Hand':
        '''Hand: 'LargestEnd' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.LargestEnd)
        return constructor.new(_133.Hand)(value) if value else None

    @largest_end.setter
    def largest_end(self, value: '_133.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LargestEnd = value

    @property
    def width(self) -> 'float':
        '''float: 'Width' is the original name of this property.'''

        return self.wrapped.Width

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0

    @property
    def is_internal(self) -> 'bool':
        '''bool: 'IsInternal' is the original name of this property.'''

        return self.wrapped.IsInternal

    @is_internal.setter
    def is_internal(self, value: 'bool'):
        self.wrapped.IsInternal = bool(value) if value else False
