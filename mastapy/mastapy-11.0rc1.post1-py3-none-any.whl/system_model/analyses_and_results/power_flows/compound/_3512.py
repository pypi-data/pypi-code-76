'''_3512.py

SynchroniserPartCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3442
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PART_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SynchroniserPartCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserPartCompoundPowerFlow',)


class SynchroniserPartCompoundPowerFlow(_3442.CouplingHalfCompoundPowerFlow):
    '''SynchroniserPartCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_PART_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserPartCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
