'''_3379.py

BevelDifferentialSunGearCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3375
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BevelDifferentialSunGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearCompoundPowerFlow',)


class BevelDifferentialSunGearCompoundPowerFlow(_3375.BevelDifferentialGearCompoundPowerFlow):
    '''BevelDifferentialSunGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
