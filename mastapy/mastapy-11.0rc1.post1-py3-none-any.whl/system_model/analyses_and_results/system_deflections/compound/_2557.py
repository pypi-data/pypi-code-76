'''_2557.py

CycloidalDiscCentralBearingConnectionCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2537
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CycloidalDiscCentralBearingConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionCompoundSystemDeflection',)


class CycloidalDiscCentralBearingConnectionCompoundSystemDeflection(_2537.CoaxialConnectionCompoundSystemDeflection):
    '''CycloidalDiscCentralBearingConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
