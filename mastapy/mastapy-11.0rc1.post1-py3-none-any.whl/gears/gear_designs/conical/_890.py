'''_890.py

ConicalGearDesign
'''


from mastapy.gears import _132
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _829
from mastapy.gears.manufacturing.bevel import _578
from mastapy.gears.gear_designs import _712
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearDesign',)


class ConicalGearDesign(_712.GearDesign):
    '''ConicalGearDesign

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hand(self) -> '_132.Hand':
        '''Hand: 'Hand' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Hand)
        return constructor.new(_132.Hand)(value) if value else None

    @hand.setter
    def hand(self, value: '_132.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Hand = value

    @property
    def straddle_mounted(self) -> 'bool':
        '''bool: 'StraddleMounted' is the original name of this property.'''

        return self.wrapped.StraddleMounted

    @straddle_mounted.setter
    def straddle_mounted(self, value: 'bool'):
        self.wrapped.StraddleMounted = bool(value) if value else False

    @property
    def face_angle(self) -> 'float':
        '''float: 'FaceAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceAngle

    @property
    def inner_tip_diameter(self) -> 'float':
        '''float: 'InnerTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerTipDiameter

    @property
    def outer_root_diameter(self) -> 'float':
        '''float: 'OuterRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRootDiameter

    @property
    def inner_root_diameter(self) -> 'float':
        '''float: 'InnerRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerRootDiameter

    @property
    def cutter_edge_radius_concave(self) -> 'float':
        '''float: 'CutterEdgeRadiusConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterEdgeRadiusConcave

    @property
    def cutter_edge_radius_convex(self) -> 'float':
        '''float: 'CutterEdgeRadiusConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CutterEdgeRadiusConvex

    @property
    def root_angle(self) -> 'float':
        '''float: 'RootAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RootAngle

    @property
    def use_cutter_tilt(self) -> 'bool':
        '''bool: 'UseCutterTilt' is the original name of this property.'''

        return self.wrapped.UseCutterTilt

    @use_cutter_tilt.setter
    def use_cutter_tilt(self, value: 'bool'):
        self.wrapped.UseCutterTilt = bool(value) if value else False

    @property
    def surface_roughness(self) -> '_829.SurfaceRoughness':
        '''SurfaceRoughness: 'SurfaceRoughness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_829.SurfaceRoughness)(self.wrapped.SurfaceRoughness) if self.wrapped.SurfaceRoughness else None

    @property
    def flank_measurement_border(self) -> '_578.FlankMeasurementBorder':
        '''FlankMeasurementBorder: 'FlankMeasurementBorder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_578.FlankMeasurementBorder)(self.wrapped.FlankMeasurementBorder) if self.wrapped.FlankMeasurementBorder else None
