'''_2191.py

BearingDetailConfiguration
'''


from mastapy.system_model.part_model.configurations import _2193, _2192
from mastapy.system_model.part_model import _2026
from mastapy.bearings.bearing_designs import _1769
from mastapy._internal.python_net import python_net_import

_BEARING_DETAIL_CONFIGURATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'BearingDetailConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDetailConfiguration',)


class BearingDetailConfiguration(_2193.PartDetailConfiguration['_2192.BearingDetailSelection', '_2026.Bearing', '_1769.BearingDesign']):
    '''BearingDetailConfiguration

    This is a mastapy class.
    '''

    TYPE = _BEARING_DETAIL_CONFIGURATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingDetailConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
