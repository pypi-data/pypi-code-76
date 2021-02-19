'''_138.py

NodalComposite
'''


from mastapy.nodal_analysis.nodal_entities import _139
from mastapy._internal.python_net import python_net_import

_NODAL_COMPOSITE = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'NodalComposite')


__docformat__ = 'restructuredtext en'
__all__ = ('NodalComposite',)


class NodalComposite(_139.NodalEntity):
    '''NodalComposite

    This is a mastapy class.
    '''

    TYPE = _NODAL_COMPOSITE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodalComposite.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
