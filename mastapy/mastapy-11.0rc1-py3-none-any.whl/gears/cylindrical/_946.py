'''_946.py

GearLTCAContactChartDataAsTextFile
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'GearLTCAContactChartDataAsTextFile')


__docformat__ = 'restructuredtext en'
__all__ = ('GearLTCAContactChartDataAsTextFile',)


class GearLTCAContactChartDataAsTextFile(_0.APIBase):
    '''GearLTCAContactChartDataAsTextFile

    This is a mastapy class.
    '''

    TYPE = _GEAR_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearLTCAContactChartDataAsTextFile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def max_pressure(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'MaxPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaxPressure

    @property
    def force_per_unit_length(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ForcePerUnitLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForcePerUnitLength

    @property
    def hertzian_contact_half_width(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'HertzianContactHalfWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactHalfWidth

    @property
    def max_shear_stress(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'MaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaxShearStress

    @property
    def depth_of_max_shear_stress(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'DepthOfMaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DepthOfMaxShearStress

    @property
    def total_deflection_for_mesh(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'TotalDeflectionForMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalDeflectionForMesh

    @property
    def gap_between_loaded_flanks_transverse(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'GapBetweenLoadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GapBetweenLoadedFlanksTransverse
