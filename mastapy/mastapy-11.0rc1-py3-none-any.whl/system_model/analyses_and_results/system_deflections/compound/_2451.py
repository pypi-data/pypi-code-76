'''_2451.py

ConnectionCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6555
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundSystemDeflection',)


class ConnectionCompoundSystemDeflection(_6555.ConnectionCompoundAnalysis):
    '''ConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
