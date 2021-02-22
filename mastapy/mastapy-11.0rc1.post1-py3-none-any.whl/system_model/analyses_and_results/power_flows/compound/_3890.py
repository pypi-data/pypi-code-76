'''_3890.py

InterMountableComponentConnectionCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3860
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'InterMountableComponentConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionCompoundPowerFlow',)


class InterMountableComponentConnectionCompoundPowerFlow(_3860.ConnectionCompoundPowerFlow):
    '''InterMountableComponentConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
