'''_7044.py

BearingCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6911
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7072
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'BearingCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundAdvancedSystemDeflection',)


class BearingCompoundAdvancedSystemDeflection(_7072.ConnectorCompoundAdvancedSystemDeflection):
    '''BearingCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2114.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6911.BearingAdvancedSystemDeflection]':
        '''List[BearingAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6911.BearingAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6911.BearingAdvancedSystemDeflection]':
        '''List[BearingAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6911.BearingAdvancedSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundAdvancedSystemDeflection]':
        '''List[BearingCompoundAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundAdvancedSystemDeflection))
        return value
