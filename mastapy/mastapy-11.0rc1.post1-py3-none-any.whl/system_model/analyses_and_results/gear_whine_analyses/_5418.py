'''_5418.py

PeriodicExcitationWithReferenceShaft
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5319
from mastapy._internal.python_net import python_net_import

_PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'PeriodicExcitationWithReferenceShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('PeriodicExcitationWithReferenceShaft',)


class PeriodicExcitationWithReferenceShaft(_5319.AbstractPeriodicExcitationDetail):
    '''PeriodicExcitationWithReferenceShaft

    This is a mastapy class.
    '''

    TYPE = _PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PeriodicExcitationWithReferenceShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
