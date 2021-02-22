'''_4145.py

CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool
'''


from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4125
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool',)


class CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool(_4125.CoaxialConnectionCompoundParametricStudyTool):
    '''CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
