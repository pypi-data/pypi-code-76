'''_2453.py

CouplingCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2510
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CouplingCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundSystemDeflection',)


class CouplingCompoundSystemDeflection(_2510.SpecialisedAssemblyCompoundSystemDeflection):
    '''CouplingCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
