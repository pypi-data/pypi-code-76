'''_5514.py

FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1987
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5384
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5519
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation',)


class FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation(_5519.GearMeshCompoundHarmonicAnalysisOfSingleExcitation):
    '''FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1987.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.FaceGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1987.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5384.FaceGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearMeshHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5384.FaceGearMeshHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def connection_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5384.FaceGearMeshHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearMeshHarmonicAnalysisOfSingleExcitation]: 'ConnectionHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5384.FaceGearMeshHarmonicAnalysisOfSingleExcitation))
        return value
