'''_4000.py

CycloidalDiscPlanetaryBearingConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2014
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6491
from mastapy.system_model.analyses_and_results.system_deflections import _2401
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3957
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CycloidalDiscPlanetaryBearingConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionParametricStudyTool',)


class CycloidalDiscPlanetaryBearingConnectionParametricStudyTool(_3957.AbstractShaftToMountableComponentConnectionParametricStudyTool):
    '''CycloidalDiscPlanetaryBearingConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2014.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6491.CycloidalDiscPlanetaryBearingConnectionLoadCase':
        '''CycloidalDiscPlanetaryBearingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6491.CycloidalDiscPlanetaryBearingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2401.CycloidalDiscPlanetaryBearingConnectionSystemDeflection]':
        '''List[CycloidalDiscPlanetaryBearingConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2401.CycloidalDiscPlanetaryBearingConnectionSystemDeflection))
        return value
