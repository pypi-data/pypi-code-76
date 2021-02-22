'''_3861.py

ConnectorCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3902
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ConnectorCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundPowerFlow',)


class ConnectorCompoundPowerFlow(_3902.MountableComponentCompoundPowerFlow):
    '''ConnectorCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
