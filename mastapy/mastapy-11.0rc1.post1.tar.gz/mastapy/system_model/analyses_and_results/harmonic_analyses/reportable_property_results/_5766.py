'''_5766.py

HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5771, _5765
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_NODE_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic',)


class HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic(_5765.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic):
    '''HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_NODE_WITHIN_A_HARMONIC

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node_name(self) -> 'str':
        '''str: 'NodeName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NodeName

    @property
    def displacement(self) -> '_5771.ResultsForResponseOfANodeOnAHarmonic':
        '''ResultsForResponseOfANodeOnAHarmonic: 'Displacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5771.ResultsForResponseOfANodeOnAHarmonic)(self.wrapped.Displacement) if self.wrapped.Displacement else None

    @property
    def velocity(self) -> '_5771.ResultsForResponseOfANodeOnAHarmonic':
        '''ResultsForResponseOfANodeOnAHarmonic: 'Velocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5771.ResultsForResponseOfANodeOnAHarmonic)(self.wrapped.Velocity) if self.wrapped.Velocity else None

    @property
    def acceleration(self) -> '_5771.ResultsForResponseOfANodeOnAHarmonic':
        '''ResultsForResponseOfANodeOnAHarmonic: 'Acceleration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5771.ResultsForResponseOfANodeOnAHarmonic)(self.wrapped.Acceleration) if self.wrapped.Acceleration else None

    @property
    def force(self) -> '_5771.ResultsForResponseOfANodeOnAHarmonic':
        '''ResultsForResponseOfANodeOnAHarmonic: 'Force' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5771.ResultsForResponseOfANodeOnAHarmonic)(self.wrapped.Force) if self.wrapped.Force else None
