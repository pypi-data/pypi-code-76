'''_2478.py

InterMountableComponentConnectionCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2451
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'InterMountableComponentConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionCompoundSystemDeflection',)


class InterMountableComponentConnectionCompoundSystemDeflection(_2451.ConnectionCompoundSystemDeflection):
    '''InterMountableComponentConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
