'''_2463.py

ShaftHubConnectionSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2269
from mastapy.system_model.analyses_and_results.static_loads import _6578
from mastapy.system_model.analyses_and_results.power_flows import _3790
from mastapy.detailed_rigid_connectors.rating import _1199
from mastapy.detailed_rigid_connectors.splines.ratings import (
    _1187, _1189, _1191, _1193,
    _1195
)
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.keyed_joints.rating import _1205
from mastapy.detailed_rigid_connectors.interference_fits.rating import _1212
from mastapy.bearings.bearing_results import _1643
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2512
from mastapy.system_model.analyses_and_results.system_deflections import _2392
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ShaftHubConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionSystemDeflection',)


class ShaftHubConnectionSystemDeflection(_2392.ConnectorSystemDeflection):
    '''ShaftHubConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node_pair_separations(self) -> 'List[float]':
        '''List[float]: 'NodePairSeparations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NodePairSeparations)
        return value

    @property
    def number_of_teeth_in_contact(self) -> 'int':
        '''int: 'NumberOfTeethInContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfTeethInContact

    @property
    def number_of_major_diameter_contacts(self) -> 'int':
        '''int: 'NumberOfMajorDiameterContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfMajorDiameterContacts

    @property
    def normal_deflection_right_flank(self) -> 'List[float]':
        '''List[float]: 'NormalDeflectionRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalDeflectionRightFlank)
        return value

    @property
    def normal_deflection_left_flank(self) -> 'List[float]':
        '''List[float]: 'NormalDeflectionLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalDeflectionLeftFlank)
        return value

    @property
    def normal_deflection_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'NormalDeflectionToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalDeflectionToothCentre)
        return value

    @property
    def normal_stiffness_right_flank(self) -> 'List[float]':
        '''List[float]: 'NormalStiffnessRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalStiffnessRightFlank)
        return value

    @property
    def normal_stiffness_left_flank(self) -> 'List[float]':
        '''List[float]: 'NormalStiffnessLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalStiffnessLeftFlank)
        return value

    @property
    def normal_stiffness_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'NormalStiffnessToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalStiffnessToothCentre)
        return value

    @property
    def normal_force_right_flank(self) -> 'List[float]':
        '''List[float]: 'NormalForceRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalForceRightFlank)
        return value

    @property
    def normal_force_left_flank(self) -> 'List[float]':
        '''List[float]: 'NormalForceLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalForceLeftFlank)
        return value

    @property
    def normal_force_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'NormalForceToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NormalForceToothCentre)
        return value

    @property
    def tangential_force_right_flank(self) -> 'List[float]':
        '''List[float]: 'TangentialForceRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TangentialForceRightFlank)
        return value

    @property
    def tangential_force_left_flank(self) -> 'List[float]':
        '''List[float]: 'TangentialForceLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TangentialForceLeftFlank)
        return value

    @property
    def tangential_force_tooth_centre(self) -> 'List[float]':
        '''List[float]: 'TangentialForceToothCentre' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TangentialForceToothCentre)
        return value

    @property
    def node_radial_forces_on_inner(self) -> 'List[float]':
        '''List[float]: 'NodeRadialForcesOnInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NodeRadialForcesOnInner)
        return value

    @property
    def tangential_force_on_spline(self) -> 'float':
        '''float: 'TangentialForceOnSpline' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TangentialForceOnSpline

    @property
    def limiting_friction(self) -> 'float':
        '''float: 'LimitingFriction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LimitingFriction

    @property
    def will_spline_slip(self) -> 'bool':
        '''bool: 'WillSplineSlip' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WillSplineSlip

    @property
    def component_design(self) -> '_2269.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2269.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6578.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6578.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3790.ShaftHubConnectionPowerFlow':
        '''ShaftHubConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3790.ShaftHubConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_1199.ShaftHubConnectionRating':
        '''ShaftHubConnectionRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1199.ShaftHubConnectionRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to ShaftHubConnectionRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_agma6123_spline_joint_rating(self) -> '_1187.AGMA6123SplineJointRating':
        '''AGMA6123SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1187.AGMA6123SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to AGMA6123SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_din5466_spline_rating(self) -> '_1189.DIN5466SplineRating':
        '''DIN5466SplineRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1189.DIN5466SplineRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to DIN5466SplineRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_gbt17855_spline_joint_rating(self) -> '_1191.GBT17855SplineJointRating':
        '''GBT17855SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1191.GBT17855SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to GBT17855SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_sae_spline_joint_rating(self) -> '_1193.SAESplineJointRating':
        '''SAESplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1193.SAESplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SAESplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spline_joint_rating(self) -> '_1195.SplineJointRating':
        '''SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1195.SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_keyway_rating(self) -> '_1205.KeywayRating':
        '''KeywayRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1205.KeywayRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to KeywayRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_interference_fit_rating(self) -> '_1212.InterferenceFitRating':
        '''InterferenceFitRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1212.InterferenceFitRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to InterferenceFitRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def stiffness_matrix_in_local_coordinate_system(self) -> '_1643.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'StiffnessMatrixInLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1643.BearingStiffnessMatrixReporter)(self.wrapped.StiffnessMatrixInLocalCoordinateSystem) if self.wrapped.StiffnessMatrixInLocalCoordinateSystem else None

    @property
    def stiffness_matrix_in_unrotated_coordinate_system(self) -> '_1643.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'StiffnessMatrixInUnrotatedCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1643.BearingStiffnessMatrixReporter)(self.wrapped.StiffnessMatrixInUnrotatedCoordinateSystem) if self.wrapped.StiffnessMatrixInUnrotatedCoordinateSystem else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionSystemDeflection))
        return value

    @property
    def left_flank_contacts(self) -> 'List[_2512.SplineFlankContactReporting]':
        '''List[SplineFlankContactReporting]: 'LeftFlankContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LeftFlankContacts, constructor.new(_2512.SplineFlankContactReporting))
        return value

    @property
    def right_flank_contacts(self) -> 'List[_2512.SplineFlankContactReporting]':
        '''List[SplineFlankContactReporting]: 'RightFlankContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RightFlankContacts, constructor.new(_2512.SplineFlankContactReporting))
        return value

    @property
    def tip_contacts(self) -> 'List[_2512.SplineFlankContactReporting]':
        '''List[SplineFlankContactReporting]: 'TipContacts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TipContacts, constructor.new(_2512.SplineFlankContactReporting))
        return value
