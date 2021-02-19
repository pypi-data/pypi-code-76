'''_3476.py

MountableComponentCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3428
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'MountableComponentCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundPowerFlow',)


class MountableComponentCompoundPowerFlow(_3428.ComponentCompoundPowerFlow):
    '''MountableComponentCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
