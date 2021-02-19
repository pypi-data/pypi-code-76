'''_6429.py

BoltedJointLoadCase
'''


from mastapy.system_model.part_model import _2092
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6548
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BoltedJointLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointLoadCase',)


class BoltedJointLoadCase(_6548.SpecialisedAssemblyLoadCase):
    '''BoltedJointLoadCase

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2092.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2092.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
