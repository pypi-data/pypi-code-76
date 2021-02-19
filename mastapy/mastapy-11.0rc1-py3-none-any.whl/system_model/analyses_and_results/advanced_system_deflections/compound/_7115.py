'''_7115.py

PartCompoundAdvancedSystemDeflection
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7176
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'PartCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundAdvancedSystemDeflection',)


class PartCompoundAdvancedSystemDeflection(_7176.PartCompoundAnalysis):
    '''PartCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
