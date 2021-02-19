'''_2071.py

GearWithDuplicatedMeshesFELink
'''


from mastapy.system_model.fe.links import _2076
from mastapy._internal.python_net import python_net_import

_GEAR_WITH_DUPLICATED_MESHES_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'GearWithDuplicatedMeshesFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWithDuplicatedMeshesFELink',)


class GearWithDuplicatedMeshesFELink(_2076.PlanetBasedFELink):
    '''GearWithDuplicatedMeshesFELink

    This is a mastapy class.
    '''

    TYPE = _GEAR_WITH_DUPLICATED_MESHES_FE_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWithDuplicatedMeshesFELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
