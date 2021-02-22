'''_2607.py

RollingRingConnectionCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2460
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2579
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'RollingRingConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionCompoundSystemDeflection',)


class RollingRingConnectionCompoundSystemDeflection(_2579.InterMountableComponentConnectionCompoundSystemDeflection):
    '''RollingRingConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1968.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2460.RollingRingConnectionSystemDeflection]':
        '''List[RollingRingConnectionSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2460.RollingRingConnectionSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2460.RollingRingConnectionSystemDeflection]':
        '''List[RollingRingConnectionSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2460.RollingRingConnectionSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingConnectionCompoundSystemDeflection]':
        '''List[RollingRingConnectionCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionCompoundSystemDeflection))
        return value
