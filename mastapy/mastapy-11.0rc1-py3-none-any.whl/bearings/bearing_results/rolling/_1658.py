'''_1658.py

LoadedCylindricalRollerBearingResults
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1720, _1673
from mastapy._internal.python_net import python_net_import

_LOADED_CYLINDRICAL_ROLLER_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCylindricalRollerBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCylindricalRollerBearingResults',)


class LoadedCylindricalRollerBearingResults(_1673.LoadedNonBarrelRollerBearingResults):
    '''LoadedCylindricalRollerBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_CYLINDRICAL_ROLLER_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedCylindricalRollerBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_load_dependent_moment(self) -> 'float':
        '''float: 'AxialLoadDependentMoment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialLoadDependentMoment

    @property
    def skf_maximal_constantly_acting_axial_load(self) -> '_1720.SKFMaximalConstantlyActingAxialLoadResults':
        '''SKFMaximalConstantlyActingAxialLoadResults: 'SKFMaximalConstantlyActingAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1720.SKFMaximalConstantlyActingAxialLoadResults)(self.wrapped.SKFMaximalConstantlyActingAxialLoad) if self.wrapped.SKFMaximalConstantlyActingAxialLoad else None
