'''_575.py

GearManufacturingConfigurationViewModelPlaceholder
'''


from mastapy.gears.manufacturing.cylindrical import _574
from mastapy._internal.python_net import python_net_import

_GEAR_MANUFACTURING_CONFIGURATION_VIEW_MODEL_PLACEHOLDER = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'GearManufacturingConfigurationViewModelPlaceholder')


__docformat__ = 'restructuredtext en'
__all__ = ('GearManufacturingConfigurationViewModelPlaceholder',)


class GearManufacturingConfigurationViewModelPlaceholder(_574.GearManufacturingConfigurationViewModel):
    '''GearManufacturingConfigurationViewModelPlaceholder

    This is a mastapy class.
    '''

    TYPE = _GEAR_MANUFACTURING_CONFIGURATION_VIEW_MODEL_PLACEHOLDER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearManufacturingConfigurationViewModelPlaceholder.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
