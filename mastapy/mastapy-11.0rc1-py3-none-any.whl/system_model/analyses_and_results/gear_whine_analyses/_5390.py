'''_5390.py

GearWhineAnalysis
'''


from typing import List

from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5569
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.analysis_cases import _6553
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysis',)


class GearWhineAnalysis(_6553.CompoundAnalysisCase):
    '''GearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def single_mesh_whine_analyses(self) -> 'List[_5569.SingleMeshWhineAnalysis]':
        '''List[SingleMeshWhineAnalysis]: 'SingleMeshWhineAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SingleMeshWhineAnalyses, constructor.new(_5569.SingleMeshWhineAnalysis))
        return value
