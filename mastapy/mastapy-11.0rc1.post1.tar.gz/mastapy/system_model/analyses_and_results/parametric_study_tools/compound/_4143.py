'''_4143.py

CVTPulleyCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4189
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CVTPulleyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundParametricStudyTool',)


class CVTPulleyCompoundParametricStudyTool(_4189.PulleyCompoundParametricStudyTool):
    '''CVTPulleyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
