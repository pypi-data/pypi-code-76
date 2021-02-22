'''_3738.py

PartCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6562
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PartCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundParametricStudyTool',)


class PartCompoundParametricStudyTool(_6562.PartCompoundAnalysis):
    '''PartCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
