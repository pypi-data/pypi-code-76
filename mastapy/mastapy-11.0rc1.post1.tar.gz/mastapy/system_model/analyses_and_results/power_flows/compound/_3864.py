'''_3864.py

CouplingHalfCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3902
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CouplingHalfCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundPowerFlow',)


class CouplingHalfCompoundPowerFlow(_3902.MountableComponentCompoundPowerFlow):
    '''CouplingHalfCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
