'''_791.py

CylindricalGearLoadDistributionAnalysis
'''


from mastapy.gears.rating.cylindrical import _417
from mastapy._internal import constructor
from mastapy.gears.gear_two_d_fe_analysis import _831
from mastapy.gears.ltca import _777
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLoadDistributionAnalysis',)


class CylindricalGearLoadDistributionAnalysis(_777.GearLoadDistributionAnalysis):
    '''CylindricalGearLoadDistributionAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_LOAD_DISTRIBUTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> '_417.CylindricalGearRating':
        '''CylindricalGearRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_417.CylindricalGearRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def tiff_analysis(self) -> '_831.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'TIFFAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_831.CylindricalGearTIFFAnalysis)(self.wrapped.TIFFAnalysis) if self.wrapped.TIFFAnalysis else None
