'''_687.py

CutterShapeDefinition
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutters import (
    _677, _671, _672, _673,
    _674, _676, _678, _679,
    _682
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _693
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CUTTER_SHAPE_DEFINITION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles', 'CutterShapeDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterShapeDefinition',)


class CutterShapeDefinition(_0.APIBase):
    '''CutterShapeDefinition

    This is a mastapy class.
    '''

    TYPE = _CUTTER_SHAPE_DEFINITION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CutterShapeDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def normal_pitch(self) -> 'float':
        '''float: 'NormalPitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalPitch

    @property
    def normal_module(self) -> 'float':
        '''float: 'NormalModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalModule

    @property
    def normal_pressure_angle(self) -> 'float':
        '''float: 'NormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalPressureAngle

    @property
    def design(self) -> '_677.CylindricalGearRealCutterDesign':
        '''CylindricalGearRealCutterDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _677.CylindricalGearRealCutterDesign.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearRealCutterDesign. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_form_grinding_wheel(self) -> '_671.CylindricalGearFormGrindingWheel':
        '''CylindricalGearFormGrindingWheel: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _671.CylindricalGearFormGrindingWheel.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearFormGrindingWheel. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_grinding_worm(self) -> '_672.CylindricalGearGrindingWorm':
        '''CylindricalGearGrindingWorm: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _672.CylindricalGearGrindingWorm.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearGrindingWorm. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_hob_design(self) -> '_673.CylindricalGearHobDesign':
        '''CylindricalGearHobDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _673.CylindricalGearHobDesign.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearHobDesign. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_plunge_shaver(self) -> '_674.CylindricalGearPlungeShaver':
        '''CylindricalGearPlungeShaver: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _674.CylindricalGearPlungeShaver.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearPlungeShaver. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_rack_design(self) -> '_676.CylindricalGearRackDesign':
        '''CylindricalGearRackDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _676.CylindricalGearRackDesign.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearRackDesign. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_shaper(self) -> '_678.CylindricalGearShaper':
        '''CylindricalGearShaper: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _678.CylindricalGearShaper.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearShaper. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_shaver(self) -> '_679.CylindricalGearShaver':
        '''CylindricalGearShaver: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _679.CylindricalGearShaver.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_involute_cutter_design(self) -> '_682.InvoluteCutterDesign':
        '''InvoluteCutterDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _682.InvoluteCutterDesign.TYPE not in self.wrapped.Design.__class__.__mro__:
            raise CastException('Failed to cast design to InvoluteCutterDesign. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Design.__class__)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def fillet_points(self) -> 'List[_693.NamedPoint]':
        '''List[NamedPoint]: 'FilletPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FilletPoints, constructor.new(_693.NamedPoint))
        return value

    @property
    def main_blade_points(self) -> 'List[_693.NamedPoint]':
        '''List[NamedPoint]: 'MainBladePoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MainBladePoints, constructor.new(_693.NamedPoint))
        return value
