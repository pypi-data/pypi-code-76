'''_755.py

PinionMachineSettingsSMT
'''


from mastapy.gears.manufacturing.bevel import _752
from mastapy._internal.python_net import python_net_import

_PINION_MACHINE_SETTINGS_SMT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionMachineSettingsSMT')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionMachineSettingsSMT',)


class PinionMachineSettingsSMT(_752.PinionFinishMachineSettings):
    '''PinionMachineSettingsSMT

    This is a mastapy class.
    '''

    TYPE = _PINION_MACHINE_SETTINGS_SMT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PinionMachineSettingsSMT.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
