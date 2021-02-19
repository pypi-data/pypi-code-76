'''_226.py

ISO10300RateableMesh
'''


from typing import Generic, TypeVar

from mastapy.gears.rating.conical import _330
from mastapy.gears.rating.virtual_cylindrical_gears import _188
from mastapy._internal.python_net import python_net_import

_ISO10300_RATEABLE_MESH = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'ISO10300RateableMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO10300RateableMesh',)


T = TypeVar('T', bound='_188.VirtualCylindricalGearBasic')


class ISO10300RateableMesh(_330.ConicalRateableMesh, Generic[T]):
    '''ISO10300RateableMesh

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _ISO10300_RATEABLE_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO10300RateableMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
