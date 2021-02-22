'''_7089.py

FaceGearCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6958
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7094
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'FaceGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundAdvancedSystemDeflection',)


class FaceGearCompoundAdvancedSystemDeflection(_7094.GearCompoundAdvancedSystemDeflection):
    '''FaceGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2199.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2199.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6958.FaceGearAdvancedSystemDeflection]':
        '''List[FaceGearAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6958.FaceGearAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6958.FaceGearAdvancedSystemDeflection]':
        '''List[FaceGearAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6958.FaceGearAdvancedSystemDeflection))
        return value
