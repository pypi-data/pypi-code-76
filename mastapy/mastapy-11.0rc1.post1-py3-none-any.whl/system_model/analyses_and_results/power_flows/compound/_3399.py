'''_3399.py

BevelDifferentialPlanetGearCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3396
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BevelDifferentialPlanetGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCompoundPowerFlow',)


class BevelDifferentialPlanetGearCompoundPowerFlow(_3396.BevelDifferentialGearCompoundPowerFlow):
    '''BevelDifferentialPlanetGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
