'''_4220.py

TorqueConverterPumpCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2279
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4091
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4140
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'TorqueConverterPumpCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundParametricStudyTool',)


class TorqueConverterPumpCompoundParametricStudyTool(_4140.CouplingHalfCompoundParametricStudyTool):
    '''TorqueConverterPumpCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2279.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2279.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4091.TorqueConverterPumpParametricStudyTool]':
        '''List[TorqueConverterPumpParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4091.TorqueConverterPumpParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_4091.TorqueConverterPumpParametricStudyTool]':
        '''List[TorqueConverterPumpParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_4091.TorqueConverterPumpParametricStudyTool))
        return value
