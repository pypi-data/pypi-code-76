'''_7154.py

TorqueConverterConnectionCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7024
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7074
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'TorqueConverterConnectionCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundAdvancedSystemDeflection',)


class TorqueConverterConnectionCompoundAdvancedSystemDeflection(_7074.CouplingConnectionCompoundAdvancedSystemDeflection):
    '''TorqueConverterConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_7024.TorqueConverterConnectionAdvancedSystemDeflection]':
        '''List[TorqueConverterConnectionAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_7024.TorqueConverterConnectionAdvancedSystemDeflection))
        return value

    @property
    def connection_advanced_system_deflection_load_cases(self) -> 'List[_7024.TorqueConverterConnectionAdvancedSystemDeflection]':
        '''List[TorqueConverterConnectionAdvancedSystemDeflection]: 'ConnectionAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedSystemDeflectionLoadCases, constructor.new(_7024.TorqueConverterConnectionAdvancedSystemDeflection))
        return value
