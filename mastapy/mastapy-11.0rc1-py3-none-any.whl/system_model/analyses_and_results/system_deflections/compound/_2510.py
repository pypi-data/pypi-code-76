'''_2510.py

SpecialisedAssemblyCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2418
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SpecialisedAssemblyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundSystemDeflection',)


class SpecialisedAssemblyCompoundSystemDeflection(_2418.AbstractAssemblyCompoundSystemDeflection):
    '''SpecialisedAssemblyCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
