'''_2551.py

CouplingConnectionCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2579
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CouplingConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundSystemDeflection',)


class CouplingConnectionCompoundSystemDeflection(_2579.InterMountableComponentConnectionCompoundSystemDeflection):
    '''CouplingConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
