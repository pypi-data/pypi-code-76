'''_4055.py

PlanetaryConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1963
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6561
from mastapy.system_model.analyses_and_results.system_deflections import _2451
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4069
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'PlanetaryConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionParametricStudyTool',)


class PlanetaryConnectionParametricStudyTool(_4069.ShaftToMountableComponentConnectionParametricStudyTool):
    '''PlanetaryConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1963.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6561.PlanetaryConnectionLoadCase':
        '''PlanetaryConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6561.PlanetaryConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2451.PlanetaryConnectionSystemDeflection]':
        '''List[PlanetaryConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2451.PlanetaryConnectionSystemDeflection))
        return value
