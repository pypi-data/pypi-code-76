'''_5875.py

FlexiblePinAnalysisManufactureLevel
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3972
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _5871
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisManufactureLevel')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisManufactureLevel',)


class FlexiblePinAnalysisManufactureLevel(_5871.FlexiblePinAnalysis):
    '''FlexiblePinAnalysisManufactureLevel

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisManufactureLevel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_sharing_factors(self) -> 'List[float]':
        '''List[float]: 'LoadSharingFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.LoadSharingFactors)
        return value

    @property
    def planetary_mesh_analysis(self) -> '_3972.CylindricalGearMeshParametricStudyTool':
        '''CylindricalGearMeshParametricStudyTool: 'PlanetaryMeshAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3972.CylindricalGearMeshParametricStudyTool)(self.wrapped.PlanetaryMeshAnalysis) if self.wrapped.PlanetaryMeshAnalysis else None
