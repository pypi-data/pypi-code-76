'''_7095.py

GearMeshCompoundAdvancedSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7101
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'GearMeshCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundAdvancedSystemDeflection',)


class GearMeshCompoundAdvancedSystemDeflection(_7101.InterMountableComponentConnectionCompoundAdvancedSystemDeflection):
    '''GearMeshCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_separation_left_flank(self) -> 'float':
        '''float: 'MinimumSeparationLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumSeparationLeftFlank

    @property
    def minimum_separation_right_flank(self) -> 'float':
        '''float: 'MinimumSeparationRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumSeparationRightFlank
