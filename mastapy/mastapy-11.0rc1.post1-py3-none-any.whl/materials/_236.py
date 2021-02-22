'''_236.py

MaterialsSettings
'''


from mastapy.utility import _1348
from mastapy._internal.python_net import python_net_import

_MATERIALS_SETTINGS = python_net_import('SMT.MastaAPI.Materials', 'MaterialsSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MaterialsSettings',)


class MaterialsSettings(_1348.PerMachineSettings):
    '''MaterialsSettings

    This is a mastapy class.
    '''

    TYPE = _MATERIALS_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MaterialsSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
