'''_3646.py

AbstractAssemblyCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3719
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'AbstractAssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundParametricStudyTool',)


class AbstractAssemblyCompoundParametricStudyTool(_3719.PartCompoundParametricStudyTool):
    '''AbstractAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
