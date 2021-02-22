'''_6957.py

ExternalCADModelAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2125
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6513
from mastapy.system_model.analyses_and_results.system_deflections import _2414
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6928
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ExternalCADModelAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelAdvancedSystemDeflection',)


class ExternalCADModelAdvancedSystemDeflection(_6928.ComponentAdvancedSystemDeflection):
    '''ExternalCADModelAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2125.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2125.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6513.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6513.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2414.ExternalCADModelSystemDeflection]':
        '''List[ExternalCADModelSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2414.ExternalCADModelSystemDeflection))
        return value
