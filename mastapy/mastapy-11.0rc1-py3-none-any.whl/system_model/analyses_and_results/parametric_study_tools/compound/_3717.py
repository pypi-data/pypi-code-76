'''_3717.py

GearMeshCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3724
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearMeshCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundParametricStudyTool',)


class GearMeshCompoundParametricStudyTool(_3724.InterMountableComponentConnectionCompoundParametricStudyTool):
    '''GearMeshCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
