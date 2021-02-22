'''_118.py

SpaceClaimDimensions
'''


from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SPACE_CLAIM_DIMENSIONS = python_net_import('SMT.MastaAPI.NodalAnalysis.SpaceClaimLink', 'SpaceClaimDimensions')


__docformat__ = 'restructuredtext en'
__all__ = ('SpaceClaimDimensions',)


class SpaceClaimDimensions(_0.APIBase):
    '''SpaceClaimDimensions

    This is a mastapy class.
    '''

    TYPE = _SPACE_CLAIM_DIMENSIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpaceClaimDimensions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
