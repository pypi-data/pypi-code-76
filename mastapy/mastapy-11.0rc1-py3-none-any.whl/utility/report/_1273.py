'''_1273.py

AdHocCustomTable
'''


from mastapy.utility.report import _1287
from mastapy._internal.python_net import python_net_import

_AD_HOC_CUSTOM_TABLE = python_net_import('SMT.MastaAPI.Utility.Report', 'AdHocCustomTable')


__docformat__ = 'restructuredtext en'
__all__ = ('AdHocCustomTable',)


class AdHocCustomTable(_1287.CustomReportDefinitionItem):
    '''AdHocCustomTable

    This is a mastapy class.
    '''

    TYPE = _AD_HOC_CUSTOM_TABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdHocCustomTable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
