'''_708.py

DesignConstraint
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.utility.model_validation import _1315
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINT = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraint')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraint',)


class DesignConstraint(_0.APIBase):
    '''DesignConstraint

    This is a mastapy class.
    '''

    TYPE = _DESIGN_CONSTRAINT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignConstraint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def type_(self) -> 'str':
        '''str: 'Type' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Type

    @property
    def severity(self) -> 'enum_with_selected_value.EnumWithSelectedValue_Severity':
        '''enum_with_selected_value.EnumWithSelectedValue_Severity: 'Severity' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_Severity.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.Severity, value) if self.wrapped.Severity else None

    @severity.setter
    def severity(self, value: 'enum_with_selected_value.EnumWithSelectedValue_Severity.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_Severity.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Severity = value

    @property
    def property_(self) -> 'str':
        '''str: 'Property' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Property

    @property
    def unit(self) -> 'str':
        '''str: 'Unit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Unit
