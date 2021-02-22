'''_3444.py

CVTCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3413
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CVTCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundPowerFlow',)


class CVTCompoundPowerFlow(_3413.BeltDriveCompoundPowerFlow):
    '''CVTCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
