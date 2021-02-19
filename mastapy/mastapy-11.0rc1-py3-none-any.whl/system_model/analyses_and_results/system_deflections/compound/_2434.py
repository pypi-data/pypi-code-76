'''_2434.py

BevelGearSetCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2422
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BevelGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearSetCompoundSystemDeflection',)


class BevelGearSetCompoundSystemDeflection(_2422.AGMAGleasonConicalGearSetCompoundSystemDeflection):
    '''BevelGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
