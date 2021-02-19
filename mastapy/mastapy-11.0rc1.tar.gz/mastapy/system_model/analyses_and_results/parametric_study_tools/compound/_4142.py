'''_4142.py

CVTCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4111
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CVTCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundParametricStudyTool',)


class CVTCompoundParametricStudyTool(_4111.BeltDriveCompoundParametricStudyTool):
    '''CVTCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
