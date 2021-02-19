'''_2045.py

BoltedJoint
'''


from mastapy.bolts import _1052
from mastapy._internal import constructor
from mastapy.system_model.part_model import _2076
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJoint',)


class BoltedJoint(_2076.SpecialisedAssembly):
    '''BoltedJoint

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJoint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def detailed_bolted_joint(self) -> '_1052.DetailedBoltedJointDesign':
        '''DetailedBoltedJointDesign: 'DetailedBoltedJoint' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1052.DetailedBoltedJointDesign)(self.wrapped.DetailedBoltedJoint) if self.wrapped.DetailedBoltedJoint else None
