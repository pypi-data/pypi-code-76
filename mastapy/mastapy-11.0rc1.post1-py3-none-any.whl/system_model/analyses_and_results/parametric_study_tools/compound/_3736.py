'''_3736.py

MountableComponentCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3688
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'MountableComponentCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundParametricStudyTool',)


class MountableComponentCompoundParametricStudyTool(_3688.ComponentCompoundParametricStudyTool):
    '''MountableComponentCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
