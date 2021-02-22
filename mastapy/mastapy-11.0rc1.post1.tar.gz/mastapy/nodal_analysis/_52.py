'''_52.py

DiagonalNonlinearStiffness
'''


from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DIAGONAL_NONLINEAR_STIFFNESS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'DiagonalNonlinearStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('DiagonalNonlinearStiffness',)


class DiagonalNonlinearStiffness(_0.APIBase):
    '''DiagonalNonlinearStiffness

    This is a mastapy class.
    '''

    TYPE = _DIAGONAL_NONLINEAR_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DiagonalNonlinearStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
