'''_2452.py

ConnectorCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2490
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConnectorCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundSystemDeflection',)


class ConnectorCompoundSystemDeflection(_2490.MountableComponentCompoundSystemDeflection):
    '''ConnectorCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
