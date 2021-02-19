'''_2231.py

RotorSpeedInputOptions
'''


from mastapy.utility_gui import _1571
from mastapy._internal.python_net import python_net_import

_ROTOR_SPEED_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet', 'RotorSpeedInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('RotorSpeedInputOptions',)


class RotorSpeedInputOptions(_1571.ColumnInputOptions):
    '''RotorSpeedInputOptions

    This is a mastapy class.
    '''

    TYPE = _ROTOR_SPEED_INPUT_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RotorSpeedInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
