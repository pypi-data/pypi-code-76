'''_2535.py

ClutchConnectionCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2018
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2375
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2551
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ClutchConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundSystemDeflection',)


class ClutchConnectionCompoundSystemDeflection(_2551.CouplingConnectionCompoundSystemDeflection):
    '''ClutchConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2375.ClutchConnectionSystemDeflection]':
        '''List[ClutchConnectionSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2375.ClutchConnectionSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2375.ClutchConnectionSystemDeflection]':
        '''List[ClutchConnectionSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2375.ClutchConnectionSystemDeflection))
        return value
