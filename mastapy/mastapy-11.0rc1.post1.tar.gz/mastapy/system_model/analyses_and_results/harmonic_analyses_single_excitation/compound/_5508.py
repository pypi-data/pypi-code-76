'''_5508.py

CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5378
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5519
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation',)


class CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation(_5519.GearMeshCompoundHarmonicAnalysisOfSingleExcitation):
    '''CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1985.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1985.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5378.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearMeshHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5378.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def connection_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5378.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearMeshHarmonicAnalysisOfSingleExcitation]: 'ConnectionHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5378.CylindricalGearMeshHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value
