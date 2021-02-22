'''_2402.py

AGMAGleasonConicalGearCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2430
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AGMAGleasonConicalGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearCompoundSystemDeflection',)


class AGMAGleasonConicalGearCompoundSystemDeflection(_2430.ConicalGearCompoundSystemDeflection):
    '''AGMAGleasonConicalGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
