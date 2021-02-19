'''_1609.py

LoadedConceptRadialClearanceBearingResults
'''


from mastapy.bearings.bearing_results import _1608
from mastapy._internal.python_net import python_net_import

_LOADED_CONCEPT_RADIAL_CLEARANCE_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedConceptRadialClearanceBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedConceptRadialClearanceBearingResults',)


class LoadedConceptRadialClearanceBearingResults(_1608.LoadedConceptClearanceBearingResults):
    '''LoadedConceptRadialClearanceBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_CONCEPT_RADIAL_CLEARANCE_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedConceptRadialClearanceBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
