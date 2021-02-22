'''_6521.py

PartAnalysisCase
'''


from mastapy.scripting import _6534
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results import _2206
from mastapy._internal.python_net import python_net_import

_PART_ANALYSIS_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'PartAnalysisCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PartAnalysisCase',)


class PartAnalysisCase(_2206.PartAnalysis):
    '''PartAnalysisCase

    This is a mastapy class.
    '''

    TYPE = _PART_ANALYSIS_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartAnalysisCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def three_d_isometric_view(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDIsometricView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDIsometricView) if self.wrapped.ThreeDIsometricView else None

    @property
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_out_of_the_screen(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDViewOrientatedInXyPlaneWithZAxisPointingOutOfTheScreen' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDViewOrientatedInXyPlaneWithZAxisPointingOutOfTheScreen) if self.wrapped.ThreeDViewOrientatedInXyPlaneWithZAxisPointingOutOfTheScreen else None

    @property
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_into_the_screen(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDViewOrientatedInXyPlaneWithZAxisPointingIntoTheScreen' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDViewOrientatedInXyPlaneWithZAxisPointingIntoTheScreen) if self.wrapped.ThreeDViewOrientatedInXyPlaneWithZAxisPointingIntoTheScreen else None

    @property
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_into_the_screen(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDViewOrientatedInYzPlaneWithXAxisPointingIntoTheScreen' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDViewOrientatedInYzPlaneWithXAxisPointingIntoTheScreen) if self.wrapped.ThreeDViewOrientatedInYzPlaneWithXAxisPointingIntoTheScreen else None

    @property
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_out_of_the_screen(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDViewOrientatedInYzPlaneWithXAxisPointingOutOfTheScreen' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDViewOrientatedInYzPlaneWithXAxisPointingOutOfTheScreen) if self.wrapped.ThreeDViewOrientatedInYzPlaneWithXAxisPointingOutOfTheScreen else None

    @property
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_into_the_screen(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDViewOrientatedInXzPlaneWithYAxisPointingIntoTheScreen' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDViewOrientatedInXzPlaneWithYAxisPointingIntoTheScreen) if self.wrapped.ThreeDViewOrientatedInXzPlaneWithYAxisPointingIntoTheScreen else None

    @property
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_out_of_the_screen(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDViewOrientatedInXzPlaneWithYAxisPointingOutOfTheScreen' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDViewOrientatedInXzPlaneWithYAxisPointingOutOfTheScreen) if self.wrapped.ThreeDViewOrientatedInXzPlaneWithYAxisPointingOutOfTheScreen else None

    @property
    def three_d_view(self) -> '_6534.SMTBitmap':
        '''SMTBitmap: 'ThreeDView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6534.SMTBitmap)(self.wrapped.ThreeDView) if self.wrapped.ThreeDView else None
