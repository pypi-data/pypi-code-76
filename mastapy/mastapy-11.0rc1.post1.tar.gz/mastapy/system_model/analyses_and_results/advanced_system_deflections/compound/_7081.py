'''_7081.py

CycloidalDiscCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2240
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6948
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7037
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'CycloidalDiscCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundAdvancedSystemDeflection',)


class CycloidalDiscCompoundAdvancedSystemDeflection(_7037.AbstractShaftCompoundAdvancedSystemDeflection):
    '''CycloidalDiscCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2240.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6948.CycloidalDiscAdvancedSystemDeflection]':
        '''List[CycloidalDiscAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6948.CycloidalDiscAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6948.CycloidalDiscAdvancedSystemDeflection]':
        '''List[CycloidalDiscAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6948.CycloidalDiscAdvancedSystemDeflection))
        return value
