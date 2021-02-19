'''_771.py

CylindricalGearAbstractRack
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.cylindrical import _775, _796
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _514
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_ABSTRACT_RACK = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearAbstractRack')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearAbstractRack',)


class CylindricalGearAbstractRack(_0.APIBase):
    '''CylindricalGearAbstractRack

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_ABSTRACT_RACK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearAbstractRack.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def basic_rack_addendum_factor(self) -> 'float':
        '''float: 'BasicRackAddendumFactor' is the original name of this property.'''

        return self.wrapped.BasicRackAddendumFactor

    @basic_rack_addendum_factor.setter
    def basic_rack_addendum_factor(self, value: 'float'):
        self.wrapped.BasicRackAddendumFactor = float(value) if value else 0.0

    @property
    def basic_rack_dedendum_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'BasicRackDedendumFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.BasicRackDedendumFactor) if self.wrapped.BasicRackDedendumFactor else None

    @basic_rack_dedendum_factor.setter
    def basic_rack_dedendum_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.BasicRackDedendumFactor = value

    @property
    def residual_fillet_undercut(self) -> 'float':
        '''float: 'ResidualFilletUndercut' is the original name of this property.'''

        return self.wrapped.ResidualFilletUndercut

    @residual_fillet_undercut.setter
    def residual_fillet_undercut(self, value: 'float'):
        self.wrapped.ResidualFilletUndercut = float(value) if value else 0.0

    @property
    def rough_protuberance(self) -> 'float':
        '''float: 'RoughProtuberance' is the original name of this property.'''

        return self.wrapped.RoughProtuberance

    @rough_protuberance.setter
    def rough_protuberance(self, value: 'float'):
        self.wrapped.RoughProtuberance = float(value) if value else 0.0

    @property
    def residual_fillet_undercut_factor(self) -> 'float':
        '''float: 'ResidualFilletUndercutFactor' is the original name of this property.'''

        return self.wrapped.ResidualFilletUndercutFactor

    @residual_fillet_undercut_factor.setter
    def residual_fillet_undercut_factor(self, value: 'float'):
        self.wrapped.ResidualFilletUndercutFactor = float(value) if value else 0.0

    @property
    def rough_protuberance_factor(self) -> 'float':
        '''float: 'RoughProtuberanceFactor' is the original name of this property.'''

        return self.wrapped.RoughProtuberanceFactor

    @rough_protuberance_factor.setter
    def rough_protuberance_factor(self, value: 'float'):
        self.wrapped.RoughProtuberanceFactor = float(value) if value else 0.0

    @property
    def edge_radius_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'EdgeRadiusFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.EdgeRadiusFactor) if self.wrapped.EdgeRadiusFactor else None

    @edge_radius_factor.setter
    def edge_radius_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.EdgeRadiusFactor = value

    @property
    def use_maximum_edge_radius(self) -> 'bool':
        '''bool: 'UseMaximumEdgeRadius' is the original name of this property.'''

        return self.wrapped.UseMaximumEdgeRadius

    @use_maximum_edge_radius.setter
    def use_maximum_edge_radius(self, value: 'bool'):
        self.wrapped.UseMaximumEdgeRadius = bool(value) if value else False

    @property
    def protuberance_specification(self) -> 'CylindricalGearAbstractRack.ProtuberanceSpecificationMethod':
        '''ProtuberanceSpecificationMethod: 'ProtuberanceSpecification' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ProtuberanceSpecification)
        return constructor.new(CylindricalGearAbstractRack.ProtuberanceSpecificationMethod)(value) if value else None

    @protuberance_specification.setter
    def protuberance_specification(self, value: 'CylindricalGearAbstractRack.ProtuberanceSpecificationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProtuberanceSpecification = value

    @property
    def protuberance_height_factor(self) -> 'float':
        '''float: 'ProtuberanceHeightFactor' is the original name of this property.'''

        return self.wrapped.ProtuberanceHeightFactor

    @protuberance_height_factor.setter
    def protuberance_height_factor(self, value: 'float'):
        self.wrapped.ProtuberanceHeightFactor = float(value) if value else 0.0

    @property
    def protuberance_height(self) -> 'float':
        '''float: 'ProtuberanceHeight' is the original name of this property.'''

        return self.wrapped.ProtuberanceHeight

    @protuberance_height.setter
    def protuberance_height(self, value: 'float'):
        self.wrapped.ProtuberanceHeight = float(value) if value else 0.0

    @property
    def protuberance_angle(self) -> 'float':
        '''float: 'ProtuberanceAngle' is the original name of this property.'''

        return self.wrapped.ProtuberanceAngle

    @protuberance_angle.setter
    def protuberance_angle(self, value: 'float'):
        self.wrapped.ProtuberanceAngle = float(value) if value else 0.0

    @property
    def maximum_possible_cutter_edge_radius(self) -> 'float':
        '''float: 'MaximumPossibleCutterEdgeRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumPossibleCutterEdgeRadius

    @property
    def rack_undercut_clearance_normal_module(self) -> 'float':
        '''float: 'RackUndercutClearanceNormalModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RackUndercutClearanceNormalModule

    @property
    def rack_undercut_clearance(self) -> 'float':
        '''float: 'RackUndercutClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RackUndercutClearance

    @property
    def basic_rack_tip_thickness(self) -> 'float':
        '''float: 'BasicRackTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BasicRackTipThickness

    @property
    def cutter_tip_width_normal_module(self) -> 'float':
        '''float: 'CutterTipWidthNormalModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterTipWidthNormalModule

    @property
    def radial_chamfer_height_factor(self) -> 'float':
        '''float: 'RadialChamferHeightFactor' is the original name of this property.'''

        return self.wrapped.RadialChamferHeightFactor

    @radial_chamfer_height_factor.setter
    def radial_chamfer_height_factor(self, value: 'float'):
        self.wrapped.RadialChamferHeightFactor = float(value) if value else 0.0

    @property
    def radial_chamfer_height(self) -> 'float':
        '''float: 'RadialChamferHeight' is the original name of this property.'''

        return self.wrapped.RadialChamferHeight

    @radial_chamfer_height.setter
    def radial_chamfer_height(self, value: 'float'):
        self.wrapped.RadialChamferHeight = float(value) if value else 0.0

    @property
    def diameter_chamfer_height(self) -> 'float':
        '''float: 'DiameterChamferHeight' is the original name of this property.'''

        return self.wrapped.DiameterChamferHeight

    @diameter_chamfer_height.setter
    def diameter_chamfer_height(self, value: 'float'):
        self.wrapped.DiameterChamferHeight = float(value) if value else 0.0

    @property
    def chamfer_angle(self) -> 'float':
        '''float: 'ChamferAngle' is the original name of this property.'''

        return self.wrapped.ChamferAngle

    @chamfer_angle.setter
    def chamfer_angle(self, value: 'float'):
        self.wrapped.ChamferAngle = float(value) if value else 0.0

    @property
    def chamfer_angle_in_transverse_plane(self) -> 'float':
        '''float: 'ChamferAngleInTransversePlane' is the original name of this property.'''

        return self.wrapped.ChamferAngleInTransversePlane

    @chamfer_angle_in_transverse_plane.setter
    def chamfer_angle_in_transverse_plane(self, value: 'float'):
        self.wrapped.ChamferAngleInTransversePlane = float(value) if value else 0.0

    @property
    def edge_radius(self) -> 'float':
        '''float: 'EdgeRadius' is the original name of this property.'''

        return self.wrapped.EdgeRadius

    @edge_radius.setter
    def edge_radius(self, value: 'float'):
        self.wrapped.EdgeRadius = float(value) if value else 0.0

    @property
    def gear(self) -> '_775.CylindricalGearDesign':
        '''CylindricalGearDesign: 'Gear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _775.CylindricalGearDesign.TYPE not in self.wrapped.Gear.__class__.__mro__:
            raise CastException('Failed to cast gear to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.Gear.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Gear.__class__)(self.wrapped.Gear) if self.wrapped.Gear else None

    @property
    def shaper_for_agma_rating(self) -> '_514.CylindricalGearShaper':
        '''CylindricalGearShaper: 'ShaperForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_514.CylindricalGearShaper)(self.wrapped.ShaperForAGMARating) if self.wrapped.ShaperForAGMARating else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
