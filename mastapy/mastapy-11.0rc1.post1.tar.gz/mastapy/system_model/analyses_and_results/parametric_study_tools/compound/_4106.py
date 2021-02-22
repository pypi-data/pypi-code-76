'''_4106.py

AGMAGleasonConicalGearMeshCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4134
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'AGMAGleasonConicalGearMeshCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshCompoundParametricStudyTool',)


class AGMAGleasonConicalGearMeshCompoundParametricStudyTool(_4134.ConicalGearMeshCompoundParametricStudyTool):
    '''AGMAGleasonConicalGearMeshCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
