'''_3826.py

AbstractShaftCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3827
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AbstractShaftCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftCompoundPowerFlow',)


class AbstractShaftCompoundPowerFlow(_3827.AbstractShaftOrHousingCompoundPowerFlow):
    '''AbstractShaftCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
