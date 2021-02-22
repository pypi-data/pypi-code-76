'''_1734.py

LoadedSphericalRollerRadialBearingResults
'''


from mastapy.bearings.bearing_results.rolling import _1723
from mastapy._internal.python_net import python_net_import

_LOADED_SPHERICAL_ROLLER_RADIAL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedSphericalRollerRadialBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedSphericalRollerRadialBearingResults',)


class LoadedSphericalRollerRadialBearingResults(_1723.LoadedRollerBearingResults):
    '''LoadedSphericalRollerRadialBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_SPHERICAL_ROLLER_RADIAL_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedSphericalRollerRadialBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
