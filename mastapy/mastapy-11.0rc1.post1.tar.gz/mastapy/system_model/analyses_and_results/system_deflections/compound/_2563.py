'''_2563.py

CylindricalPlanetGearCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2560
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CylindricalPlanetGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearCompoundSystemDeflection',)


class CylindricalPlanetGearCompoundSystemDeflection(_2560.CylindricalGearCompoundSystemDeflection):
    '''CylindricalPlanetGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
