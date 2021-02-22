'''_2008.py

ImportedFEWithSelectionForHarmonicAnalysis
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses import _1483
from mastapy.system_model.imported_fes import _2016, _2006
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_WITH_SELECTION_FOR_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEWithSelectionForHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEWithSelectionForHarmonicAnalysis',)


class ImportedFEWithSelectionForHarmonicAnalysis(_2006.ImportedFEWithSelection):
    '''ImportedFEWithSelectionForHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_WITH_SELECTION_FOR_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEWithSelectionForHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def frequency(self) -> 'float':
        '''float: 'Frequency' is the original name of this property.'''

        return self.wrapped.Frequency

    @frequency.setter
    def frequency(self, value: 'float'):
        self.wrapped.Frequency = float(value) if value else 0.0

    @property
    def alpha_damping_value(self) -> 'float':
        '''float: 'AlphaDampingValue' is the original name of this property.'''

        return self.wrapped.AlphaDampingValue

    @alpha_damping_value.setter
    def alpha_damping_value(self, value: 'float'):
        self.wrapped.AlphaDampingValue = float(value) if value else 0.0

    @property
    def beta_damping_value(self) -> 'float':
        '''float: 'BetaDampingValue' is the original name of this property.'''

        return self.wrapped.BetaDampingValue

    @beta_damping_value.setter
    def beta_damping_value(self, value: 'float'):
        self.wrapped.BetaDampingValue = float(value) if value else 0.0

    @property
    def solve_for_current_inputs(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SolveForCurrentInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SolveForCurrentInputs

    @property
    def export_velocity_to_file(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ExportVelocityToFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportVelocityToFile

    @property
    def harmonic_draw_style(self) -> '_1483.FEModelHarmonicAnalysisDrawStyle':
        '''FEModelHarmonicAnalysisDrawStyle: 'HarmonicDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1483.FEModelHarmonicAnalysisDrawStyle)(self.wrapped.HarmonicDrawStyle) if self.wrapped.HarmonicDrawStyle else None

    @property
    def boundary_conditions_all_nodes(self) -> 'List[_2016.NodeBoundaryConditionStaticAnalysis]':
        '''List[NodeBoundaryConditionStaticAnalysis]: 'BoundaryConditionsAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoundaryConditionsAllNodes, constructor.new(_2016.NodeBoundaryConditionStaticAnalysis))
        return value
