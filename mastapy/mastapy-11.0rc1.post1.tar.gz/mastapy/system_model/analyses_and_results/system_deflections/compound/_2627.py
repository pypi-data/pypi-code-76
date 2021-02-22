'''_2627.py

StraightBevelSunGearCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2620
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'StraightBevelSunGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearCompoundSystemDeflection',)


class StraightBevelSunGearCompoundSystemDeflection(_2620.StraightBevelDiffGearCompoundSystemDeflection):
    '''StraightBevelSunGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
