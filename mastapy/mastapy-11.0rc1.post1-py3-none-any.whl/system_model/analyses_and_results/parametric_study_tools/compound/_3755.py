'''_3755.py

SpecialisedAssemblyCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3665
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'SpecialisedAssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundParametricStudyTool',)


class SpecialisedAssemblyCompoundParametricStudyTool(_3665.AbstractAssemblyCompoundParametricStudyTool):
    '''SpecialisedAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
