'''_1457.py

FrictionNodalComponent
'''


from mastapy.nodal_analysis.nodal_entities import _1463
from mastapy._internal.python_net import python_net_import

_FRICTION_NODAL_COMPONENT = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'FrictionNodalComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('FrictionNodalComponent',)


class FrictionNodalComponent(_1463.NodalComponent):
    '''FrictionNodalComponent

    This is a mastapy class.
    '''

    TYPE = _FRICTION_NODAL_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FrictionNodalComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
