'''_1599.py

BearingStiffnessMatrixReporter
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results import _1619
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEARING_STIFFNESS_MATRIX_REPORTER = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'BearingStiffnessMatrixReporter')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingStiffnessMatrixReporter',)


class BearingStiffnessMatrixReporter(_0.APIBase):
    '''BearingStiffnessMatrixReporter

    This is a mastapy class.
    '''

    TYPE = _BEARING_STIFFNESS_MATRIX_REPORTER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingStiffnessMatrixReporter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_radial_stiffness(self) -> 'float':
        '''float: 'MaximumRadialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumRadialStiffness

    @property
    def maximum_tilt_stiffness(self) -> 'float':
        '''float: 'MaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumTiltStiffness

    @property
    def axial_stiffness(self) -> 'float':
        '''float: 'AxialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialStiffness

    @property
    def stiffness_xx(self) -> 'float':
        '''float: 'StiffnessXX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessXX

    @property
    def stiffness_xy(self) -> 'float':
        '''float: 'StiffnessXY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessXY

    @property
    def stiffness_xz(self) -> 'float':
        '''float: 'StiffnessXZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessXZ

    @property
    def stiffness_yx(self) -> 'float':
        '''float: 'StiffnessYX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessYX

    @property
    def stiffness_yy(self) -> 'float':
        '''float: 'StiffnessYY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessYY

    @property
    def stiffness_yz(self) -> 'float':
        '''float: 'StiffnessYZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessYZ

    @property
    def stiffness_zx(self) -> 'float':
        '''float: 'StiffnessZX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessZX

    @property
    def stiffness_zy(self) -> 'float':
        '''float: 'StiffnessZY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessZY

    @property
    def stiffness_zz(self) -> 'float':
        '''float: 'StiffnessZZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StiffnessZZ

    @property
    def rows(self) -> 'List[_1619.StiffnessRow]':
        '''List[StiffnessRow]: 'Rows' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Rows, constructor.new(_1619.StiffnessRow))
        return value
