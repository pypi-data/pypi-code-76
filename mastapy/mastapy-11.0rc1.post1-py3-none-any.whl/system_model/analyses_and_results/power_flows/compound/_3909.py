'''_3909.py

PlanetaryGearSetCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3874
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PlanetaryGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetCompoundPowerFlow',)


class PlanetaryGearSetCompoundPowerFlow(_3874.CylindricalGearSetCompoundPowerFlow):
    '''PlanetaryGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
