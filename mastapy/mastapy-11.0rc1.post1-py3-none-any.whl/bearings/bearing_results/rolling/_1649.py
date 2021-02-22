'''_1649.py

LoadedBallBearingElement
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import _1622, _1663
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingElement',)


class LoadedBallBearingElement(_1663.LoadedElement):
    '''LoadedBallBearingElement

    This is a mastapy class.
    '''

    TYPE = _LOADED_BALL_BEARING_ELEMENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_angle_outer(self) -> 'float':
        '''float: 'ContactAngleOuter' is the original name of this property.'''

        return self.wrapped.ContactAngleOuter

    @contact_angle_outer.setter
    def contact_angle_outer(self, value: 'float'):
        self.wrapped.ContactAngleOuter = float(value) if value else 0.0

    @property
    def contact_angle_inner(self) -> 'float':
        '''float: 'ContactAngleInner' is the original name of this property.'''

        return self.wrapped.ContactAngleInner

    @contact_angle_inner.setter
    def contact_angle_inner(self, value: 'float'):
        self.wrapped.ContactAngleInner = float(value) if value else 0.0

    @property
    def maximum_normal_stress_inner(self) -> 'float':
        '''float: 'MaximumNormalStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalStressInner

    @property
    def maximum_normal_stress_outer(self) -> 'float':
        '''float: 'MaximumNormalStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalStressOuter

    @property
    def maximum_shear_stress_inner(self) -> 'float':
        '''float: 'MaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressInner

    @property
    def maximum_shear_stress_outer(self) -> 'float':
        '''float: 'MaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressOuter

    @property
    def depth_of_maximum_shear_stress_inner(self) -> 'float':
        '''float: 'DepthOfMaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DepthOfMaximumShearStressInner

    @property
    def depth_of_maximum_shear_stress_outer(self) -> 'float':
        '''float: 'DepthOfMaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DepthOfMaximumShearStressOuter

    @property
    def spinto_roll_ratio_inner(self) -> 'float':
        '''float: 'SpintoRollRatioInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpintoRollRatioInner

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_left(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerLeft

    @property
    def arc_distance_of_inner_raceway_left_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfInnerRacewayLeftEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfInnerRacewayLeftEdgeToHertzianContact

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_right(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerRight

    @property
    def arc_distance_of_inner_raceway_right_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfInnerRacewayRightEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfInnerRacewayRightEdgeToHertzianContact

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_left(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterLeft

    @property
    def arc_distance_of_outer_raceway_left_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfOuterRacewayLeftEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfOuterRacewayLeftEdgeToHertzianContact

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_right(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterRight

    @property
    def arc_distance_of_outer_raceway_right_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfOuterRacewayRightEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfOuterRacewayRightEdgeToHertzianContact

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_race_outer_edge(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationOuterRaceOuterEdge' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterRaceOuterEdge

    @property
    def arc_distance_of_outer_raceway_outer_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfOuterRacewayOuterEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfOuterRacewayOuterEdgeToHertzianContact

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_race_inner_edge(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationOuterRaceInnerEdge' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterRaceInnerEdge

    @property
    def arc_distance_of_outer_raceway_inner_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfOuterRacewayInnerEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfOuterRacewayInnerEdgeToHertzianContact

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_race_outer_edge(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationInnerRaceOuterEdge' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerRaceOuterEdge

    @property
    def arc_distance_of_inner_raceway_outer_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfInnerRacewayOuterEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfInnerRacewayOuterEdgeToHertzianContact

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_race_inner_edge(self) -> 'float':
        '''float: 'HertzianEllipseMajor2bTrackTruncationInnerRaceInnerEdge' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerRaceInnerEdge

    @property
    def arc_distance_of_inner_raceway_inner_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'ArcDistanceOfInnerRacewayInnerEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ArcDistanceOfInnerRacewayInnerEdgeToHertzianContact

    @property
    def worst_hertzian_ellipse_major_2b_track_truncation(self) -> 'float':
        '''float: 'WorstHertzianEllipseMajor2bTrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorstHertzianEllipseMajor2bTrackTruncation

    @property
    def smallest_arc_distance_of_raceway_edge_to_hertzian_contact(self) -> 'float':
        '''float: 'SmallestArcDistanceOfRacewayEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestArcDistanceOfRacewayEdgeToHertzianContact

    @property
    def track_truncation_occurring_beyond_permissible_limit(self) -> 'bool':
        '''bool: 'TrackTruncationOccurringBeyondPermissibleLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TrackTruncationOccurringBeyondPermissibleLimit

    @property
    def gyroscopic_moment(self) -> 'float':
        '''float: 'GyroscopicMoment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GyroscopicMoment

    @property
    def number_of_contact_points(self) -> 'int':
        '''int: 'NumberOfContactPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfContactPoints

    @property
    def inner_race_contact_geometries(self) -> 'List[_1622.BallBearingRaceContactGeometry]':
        '''List[BallBearingRaceContactGeometry]: 'InnerRaceContactGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.InnerRaceContactGeometries, constructor.new(_1622.BallBearingRaceContactGeometry))
        return value

    @property
    def outer_race_contact_geometries(self) -> 'List[_1622.BallBearingRaceContactGeometry]':
        '''List[BallBearingRaceContactGeometry]: 'OuterRaceContactGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OuterRaceContactGeometries, constructor.new(_1622.BallBearingRaceContactGeometry))
        return value
