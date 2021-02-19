'''_2492.py

PartCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6562
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PartCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundSystemDeflection',)


class PartCompoundSystemDeflection(_6562.PartCompoundAnalysis):
    '''PartCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
