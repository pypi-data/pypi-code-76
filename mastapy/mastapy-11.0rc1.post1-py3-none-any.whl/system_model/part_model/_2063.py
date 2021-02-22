'''_2063.py

MeasurementComponent
'''


from mastapy.system_model.part_model import _2078
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponent',)


class MeasurementComponent(_2078.VirtualComponent):
    '''MeasurementComponent

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
