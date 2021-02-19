'''_3947.py

VirtualComponentCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3902
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'VirtualComponentCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundPowerFlow',)


class VirtualComponentCompoundPowerFlow(_3902.MountableComponentCompoundPowerFlow):
    '''VirtualComponentCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
