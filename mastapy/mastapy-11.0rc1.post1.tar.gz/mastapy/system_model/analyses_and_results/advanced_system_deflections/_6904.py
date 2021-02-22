'''_6904.py

AdvancedSystemDeflection
'''


from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6905
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _7180
from mastapy._internal.python_net import python_net_import

_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'AdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflection',)


class AdvancedSystemDeflection(_7180.StaticLoadAnalysisCase):
    '''AdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def advanced_system_deflection_options(self) -> '_6905.AdvancedSystemDeflectionOptions':
        '''AdvancedSystemDeflectionOptions: 'AdvancedSystemDeflectionOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6905.AdvancedSystemDeflectionOptions)(self.wrapped.AdvancedSystemDeflectionOptions) if self.wrapped.AdvancedSystemDeflectionOptions else None
