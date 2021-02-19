'''_2379.py

AbstractAssemblyCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2453
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AbstractAssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundSystemDeflection',)


class AbstractAssemblyCompoundSystemDeflection(_2453.PartCompoundSystemDeflection):
    '''AbstractAssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
