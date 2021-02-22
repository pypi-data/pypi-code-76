'''_4126.py

ComponentCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4180
from mastapy._internal.python_net import python_net_import

_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ComponentCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentCompoundParametricStudyTool',)


class ComponentCompoundParametricStudyTool(_4180.PartCompoundParametricStudyTool):
    '''ComponentCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
