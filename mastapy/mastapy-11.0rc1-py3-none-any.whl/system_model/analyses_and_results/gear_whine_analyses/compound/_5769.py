'''_5769.py

ConnectorCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5806
from mastapy._internal.python_net import python_net_import

_CONNECTOR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ConnectorCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorCompoundGearWhineAnalysis',)


class ConnectorCompoundGearWhineAnalysis(_5806.MountableComponentCompoundGearWhineAnalysis):
    '''ConnectorCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
