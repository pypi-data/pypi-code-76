'''_948.py

GearLTCAContactCharts
'''


from mastapy.scripting import _6555
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_LTCA_CONTACT_CHARTS = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'GearLTCAContactCharts')


__docformat__ = 'restructuredtext en'
__all__ = ('GearLTCAContactCharts',)


class GearLTCAContactCharts(_0.APIBase):
    '''GearLTCAContactCharts

    This is a mastapy class.
    '''

    TYPE = _GEAR_LTCA_CONTACT_CHARTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearLTCAContactCharts.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def max_pressure(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'MaxPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.MaxPressure) if self.wrapped.MaxPressure else None

    @property
    def force_per_unit_length(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'ForcePerUnitLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.ForcePerUnitLength) if self.wrapped.ForcePerUnitLength else None

    @property
    def hertzian_contact_half_width(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'HertzianContactHalfWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.HertzianContactHalfWidth) if self.wrapped.HertzianContactHalfWidth else None

    @property
    def max_shear_stress(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'MaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.MaxShearStress) if self.wrapped.MaxShearStress else None

    @property
    def depth_of_max_shear_stress(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'DepthOfMaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.DepthOfMaxShearStress) if self.wrapped.DepthOfMaxShearStress else None

    @property
    def total_deflection_for_mesh(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'TotalDeflectionForMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.TotalDeflectionForMesh) if self.wrapped.TotalDeflectionForMesh else None

    @property
    def gap_between_loaded_flanks_transverse(self) -> '_6555.SMTBitmap':
        '''SMTBitmap: 'GapBetweenLoadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.SMTBitmap)(self.wrapped.GapBetweenLoadedFlanksTransverse) if self.wrapped.GapBetweenLoadedFlanksTransverse else None
