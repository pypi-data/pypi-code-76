'''_799.py

FinishStockSpecification
'''


from mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash import _839
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import (
    _834, _792, _794, _821
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_FINISH_STOCK_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'FinishStockSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('FinishStockSpecification',)


class FinishStockSpecification(_821.RelativeValuesSpecification['FinishStockSpecification']):
    '''FinishStockSpecification

    This is a mastapy class.
    '''

    TYPE = _FINISH_STOCK_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FinishStockSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def finish_stock_rough_thickness_specification_method(self) -> '_839.FinishStockType':
        '''FinishStockType: 'FinishStockRoughThicknessSpecificationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FinishStockRoughThicknessSpecificationMethod)
        return constructor.new(_839.FinishStockType)(value) if value else None

    @finish_stock_rough_thickness_specification_method.setter
    def finish_stock_rough_thickness_specification_method(self, value: '_839.FinishStockType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FinishStockRoughThicknessSpecificationMethod = value

    @property
    def normal(self) -> '_834.TolerancedValueSpecification[FinishStockSpecification]':
        '''TolerancedValueSpecification[FinishStockSpecification]: 'Normal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _834.TolerancedValueSpecification[FinishStockSpecification].TYPE not in self.wrapped.Normal.__class__.__mro__:
            raise CastException('Failed to cast normal to TolerancedValueSpecification[FinishStockSpecification]. Expected: {}.'.format(self.wrapped.Normal.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Normal.__class__)(self.wrapped.Normal) if self.wrapped.Normal else None

    @property
    def tangent_to_reference_circle(self) -> '_834.TolerancedValueSpecification[FinishStockSpecification]':
        '''TolerancedValueSpecification[FinishStockSpecification]: 'TangentToReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _834.TolerancedValueSpecification[FinishStockSpecification].TYPE not in self.wrapped.TangentToReferenceCircle.__class__.__mro__:
            raise CastException('Failed to cast tangent_to_reference_circle to TolerancedValueSpecification[FinishStockSpecification]. Expected: {}.'.format(self.wrapped.TangentToReferenceCircle.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TangentToReferenceCircle.__class__)(self.wrapped.TangentToReferenceCircle) if self.wrapped.TangentToReferenceCircle else None
