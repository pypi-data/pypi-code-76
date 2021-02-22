'''_3700.py

CouplingCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3755
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CouplingCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundParametricStudyTool',)


class CouplingCompoundParametricStudyTool(_3755.SpecialisedAssemblyCompoundParametricStudyTool):
    '''CouplingCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
