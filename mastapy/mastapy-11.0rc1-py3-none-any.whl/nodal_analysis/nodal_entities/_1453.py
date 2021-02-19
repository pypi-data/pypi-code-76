'''_1453.py

CMSNodalComponent
'''


from mastapy.nodal_analysis.nodal_entities import _1447
from mastapy._internal.python_net import python_net_import

_CMS_NODAL_COMPONENT = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'CMSNodalComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('CMSNodalComponent',)


class CMSNodalComponent(_1447.ArbitraryNodalComponent):
    '''CMSNodalComponent

    This is a mastapy class.
    '''

    TYPE = _CMS_NODAL_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CMSNodalComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
