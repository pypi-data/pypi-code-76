'''_5471.py

FEMeshNodeLocationSelection
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _5477
from mastapy._internal.python_net import python_net_import

_FE_MESH_NODE_LOCATION_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'FEMeshNodeLocationSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEMeshNodeLocationSelection',)


class FEMeshNodeLocationSelection(_5477.ResultNodeSelection):
    '''FEMeshNodeLocationSelection

    This is a mastapy class.
    '''

    TYPE = _FE_MESH_NODE_LOCATION_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEMeshNodeLocationSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
