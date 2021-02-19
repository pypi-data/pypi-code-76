'''_6594.py

MomentInputOptions
'''


from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6596
from mastapy._internal.python_net import python_net_import

_MOMENT_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'MomentInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('MomentInputOptions',)


class MomentInputOptions(_6596.PointLoadInputOptions):
    '''MomentInputOptions

    This is a mastapy class.
    '''

    TYPE = _MOMENT_INPUT_OPTIONS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MomentInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
