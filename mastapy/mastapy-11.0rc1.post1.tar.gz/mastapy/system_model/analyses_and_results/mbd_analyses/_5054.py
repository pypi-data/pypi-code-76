'''_5054.py

ClutchMultibodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2249
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6466
from mastapy.system_model.analyses_and_results.mbd_analyses import _5052, _5071
from mastapy._internal.python_net import python_net_import

_CLUTCH_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ClutchMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchMultibodyDynamicsAnalysis',)


class ClutchMultibodyDynamicsAnalysis(_5071.CouplingMultibodyDynamicsAnalysis):
    '''ClutchMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2249.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2249.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6466.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6466.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def clutch_connection(self) -> '_5052.ClutchConnectionMultibodyDynamicsAnalysis':
        '''ClutchConnectionMultibodyDynamicsAnalysis: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5052.ClutchConnectionMultibodyDynamicsAnalysis)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None
