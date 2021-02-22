'''_2167.py

ActiveImportedFESelectionGroup
'''


from mastapy.system_model.part_model.configurations import _2172, _2166
from mastapy.system_model.part_model import _2021
from mastapy.system_model.imported_fes import _1955
from mastapy._internal.python_net import python_net_import

_ACTIVE_IMPORTED_FE_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveImportedFESelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveImportedFESelectionGroup',)


class ActiveImportedFESelectionGroup(_2172.PartDetailConfiguration['_2166.ActiveImportedFESelection', '_2021.ImportedFEComponent', '_1955.ImportedFE']):
    '''ActiveImportedFESelectionGroup

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_IMPORTED_FE_SELECTION_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveImportedFESelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
