'''_4166.py

InterMountableComponentConnectionCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4136
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'InterMountableComponentConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionCompoundParametricStudyTool',)


class InterMountableComponentConnectionCompoundParametricStudyTool(_4136.ConnectionCompoundParametricStudyTool):
    '''InterMountableComponentConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
