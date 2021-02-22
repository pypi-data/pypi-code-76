'''_2611.py

ShaftHubConnectionCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2269
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2463
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2549
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'ShaftHubConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundSystemDeflection',)


class ShaftHubConnectionCompoundSystemDeflection(_2549.ConnectorCompoundSystemDeflection):
    '''ShaftHubConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2269.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2269.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2463.ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2463.ShaftHubConnectionSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2463.ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2463.ShaftHubConnectionSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundSystemDeflection]':
        '''List[ShaftHubConnectionCompoundSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundSystemDeflection))
        return value
