'''_4119.py

BevelGearSetCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4107
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BevelGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearSetCompoundParametricStudyTool',)


class BevelGearSetCompoundParametricStudyTool(_4107.AGMAGleasonConicalGearSetCompoundParametricStudyTool):
    '''BevelGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
