'''_7039.py

AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection
'''


from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7071
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection',)


class AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection(_7071.ConnectionCompoundAdvancedSystemDeflection):
    '''AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
