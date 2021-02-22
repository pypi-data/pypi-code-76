'''_3428.py

ComponentCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3478
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ComponentCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundPowerFlow',)


class ComponentCompoundPowerFlow(_3478.PartCompoundPowerFlow):
    '''ComponentCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
