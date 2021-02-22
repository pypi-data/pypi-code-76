'''_4223.py

VirtualComponentCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4178
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'VirtualComponentCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundParametricStudyTool',)


class VirtualComponentCompoundParametricStudyTool(_4178.MountableComponentCompoundParametricStudyTool):
    '''VirtualComponentCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
