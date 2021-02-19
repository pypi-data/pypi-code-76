'''_113.py

EntityVectorState
'''


from mastapy._internal import constructor
from mastapy.math_utility import (
    _1287, _1271, _1285, _1296,
    _1297, _1298
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ENTITY_VECTOR_STATE = python_net_import('SMT.MastaAPI.NodalAnalysis.States', 'EntityVectorState')


__docformat__ = 'restructuredtext en'
__all__ = ('EntityVectorState',)


class EntityVectorState(_0.APIBase):
    '''EntityVectorState

    This is a mastapy class.
    '''

    TYPE = _ENTITY_VECTOR_STATE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'EntityVectorState.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def degrees_of_freedom_per_entity(self) -> 'int':
        '''int: 'DegreesOfFreedomPerEntity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DegreesOfFreedomPerEntity

    @property
    def number_of_entities(self) -> 'int':
        '''int: 'NumberOfEntities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfEntities

    @property
    def vector(self) -> '_1287.RealVector':
        '''RealVector: 'Vector' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1287.RealVector.TYPE not in self.wrapped.Vector.__class__.__mro__:
            raise CastException('Failed to cast vector to RealVector. Expected: {}.'.format(self.wrapped.Vector.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Vector.__class__)(self.wrapped.Vector) if self.wrapped.Vector else None
