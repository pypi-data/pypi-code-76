'''_142.py

SimpleBar
'''


from mastapy.nodal_analysis.nodal_entities import _146
from mastapy._internal.python_net import python_net_import

_SIMPLE_BAR = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'SimpleBar')


__docformat__ = 'restructuredtext en'
__all__ = ('SimpleBar',)


class SimpleBar(_146.TwoBodyConnectionNodalComponent):
    '''SimpleBar

    This is a mastapy class.
    '''

    TYPE = _SIMPLE_BAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SimpleBar.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
