'''_1013.py

DIN5466SplineHalfRating
'''


from mastapy.detailed_rigid_connectors.splines.ratings import _1019
from mastapy._internal.python_net import python_net_import

_DIN5466_SPLINE_HALF_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings', 'DIN5466SplineHalfRating')


__docformat__ = 'restructuredtext en'
__all__ = ('DIN5466SplineHalfRating',)


class DIN5466SplineHalfRating(_1019.SplineHalfRating):
    '''DIN5466SplineHalfRating

    This is a mastapy class.
    '''

    TYPE = _DIN5466_SPLINE_HALF_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DIN5466SplineHalfRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
