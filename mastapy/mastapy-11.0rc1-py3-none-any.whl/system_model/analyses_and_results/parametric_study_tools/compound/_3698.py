'''_3698.py

ConnectionCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6555
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundParametricStudyTool',)


class ConnectionCompoundParametricStudyTool(_6555.ConnectionCompoundAnalysis):
    '''ConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
