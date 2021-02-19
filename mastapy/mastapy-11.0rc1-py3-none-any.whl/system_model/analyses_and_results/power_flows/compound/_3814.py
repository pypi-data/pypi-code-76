'''_3814.py

BevelGearSetCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3802
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BevelGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearSetCompoundPowerFlow',)


class BevelGearSetCompoundPowerFlow(_3802.AGMAGleasonConicalGearSetCompoundPowerFlow):
    '''BevelGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
