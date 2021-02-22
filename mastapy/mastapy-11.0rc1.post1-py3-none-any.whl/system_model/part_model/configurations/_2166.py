'''_2166.py

ActiveImportedFESelection
'''


from mastapy.system_model.part_model.configurations import _2173
from mastapy.system_model.part_model import _2021
from mastapy.system_model.imported_fes import _1955
from mastapy._internal.python_net import python_net_import

_ACTIVE_IMPORTED_FE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveImportedFESelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveImportedFESelection',)


class ActiveImportedFESelection(_2173.PartDetailSelection['_2021.ImportedFEComponent', '_1955.ImportedFE']):
    '''ActiveImportedFESelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_IMPORTED_FE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveImportedFESelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
