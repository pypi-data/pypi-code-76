'''_1487.py

ElementPropertiesShell
'''


from mastapy.fe_tools.vis_tools_global.vis_tools_global_enums import _969
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _1490
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_SHELL = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesShell')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesShell',)


class ElementPropertiesShell(_1490.ElementPropertiesWithMaterial):
    '''ElementPropertiesShell

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_PROPERTIES_SHELL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementPropertiesShell.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def wall_type(self) -> '_969.ElementPropertiesShellWallType':
        '''ElementPropertiesShellWallType: 'WallType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.WallType)
        return constructor.new(_969.ElementPropertiesShellWallType)(value) if value else None

    @property
    def thickness(self) -> 'float':
        '''float: 'Thickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Thickness

    @property
    def number_of_layers(self) -> 'int':
        '''int: 'NumberOfLayers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfLayers

    @property
    def layer_thicknesses(self) -> 'str':
        '''str: 'LayerThicknesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LayerThicknesses

    @property
    def effective_shear_ratio(self) -> 'float':
        '''float: 'EffectiveShearRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EffectiveShearRatio
