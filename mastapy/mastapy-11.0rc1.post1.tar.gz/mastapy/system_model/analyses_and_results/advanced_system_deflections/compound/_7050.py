'''_7050.py

BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection
'''


from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7047
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection',)


class BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection(_7047.BevelDifferentialGearCompoundAdvancedSystemDeflection):
    '''BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
