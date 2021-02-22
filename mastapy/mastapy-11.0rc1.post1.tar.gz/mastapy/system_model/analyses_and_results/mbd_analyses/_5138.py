'''_5138.py

ShaftMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2154
from mastapy.system_model.analyses_and_results.static_loads import _6579
from mastapy.system_model.analyses_and_results.mbd_analyses import _5030
from mastapy._internal.python_net import python_net_import

_SHAFT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ShaftMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftMultibodyDynamicsAnalysis',)


class ShaftMultibodyDynamicsAnalysis(_5030.AbstractShaftMultibodyDynamicsAnalysis):
    '''ShaftMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def elastic_radial_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticRadialDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticRadialDeflections)
        return value

    @property
    def elastic_local_x_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalXDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalXDeflections)
        return value

    @property
    def elastic_local_y_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalYDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalYDeflections)
        return value

    @property
    def elastic_local_z_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalZDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalZDeflections)
        return value

    @property
    def elastic_local_theta_x_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalThetaXDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalThetaXDeflections)
        return value

    @property
    def elastic_local_theta_y_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalThetaYDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalThetaYDeflections)
        return value

    @property
    def angular_velocities(self) -> 'List[float]':
        '''List[float]: 'AngularVelocities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.AngularVelocities)
        return value

    @property
    def elastic_twists(self) -> 'List[float]':
        '''List[float]: 'ElasticTwists' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticTwists)
        return value

    @property
    def component_design(self) -> '_2154.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6579.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6579.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftMultibodyDynamicsAnalysis]':
        '''List[ShaftMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftMultibodyDynamicsAnalysis))
        return value
