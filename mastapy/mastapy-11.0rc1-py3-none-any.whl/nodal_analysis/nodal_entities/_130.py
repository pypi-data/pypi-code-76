'''_130.py

DistributedRigidBarCoupling
'''


from mastapy.nodal_analysis.nodal_entities import _137
from mastapy._internal.python_net import python_net_import

_DISTRIBUTED_RIGID_BAR_COUPLING = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'DistributedRigidBarCoupling')


__docformat__ = 'restructuredtext en'
__all__ = ('DistributedRigidBarCoupling',)


class DistributedRigidBarCoupling(_137.NodalComponent):
    '''DistributedRigidBarCoupling

    This is a mastapy class.
    '''

    TYPE = _DISTRIBUTED_RIGID_BAR_COUPLING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DistributedRigidBarCoupling.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
