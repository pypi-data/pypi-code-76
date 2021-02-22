'''_7127.py

RollingRingAssemblyCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2268
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6998
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7134
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'RollingRingAssemblyCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyCompoundAdvancedSystemDeflection',)


class RollingRingAssemblyCompoundAdvancedSystemDeflection(_7134.SpecialisedAssemblyCompoundAdvancedSystemDeflection):
    '''RollingRingAssemblyCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2268.RollingRingAssembly':
        '''RollingRingAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2268.RollingRingAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2268.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2268.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6998.RollingRingAssemblyAdvancedSystemDeflection]':
        '''List[RollingRingAssemblyAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6998.RollingRingAssemblyAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_6998.RollingRingAssemblyAdvancedSystemDeflection]':
        '''List[RollingRingAssemblyAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_6998.RollingRingAssemblyAdvancedSystemDeflection))
        return value
