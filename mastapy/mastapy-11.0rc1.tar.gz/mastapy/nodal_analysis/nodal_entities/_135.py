'''_135.py

GearMeshSingleFlankContact
'''


from mastapy.nodal_analysis.nodal_entities import _138
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_SINGLE_FLANK_CONTACT = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'GearMeshSingleFlankContact')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshSingleFlankContact',)


class GearMeshSingleFlankContact(_138.NodalComposite):
    '''GearMeshSingleFlankContact

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_SINGLE_FLANK_CONTACT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshSingleFlankContact.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
