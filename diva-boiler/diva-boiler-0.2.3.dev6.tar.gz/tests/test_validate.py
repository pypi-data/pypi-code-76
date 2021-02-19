from unittest import mock

import pytest

from boiler import fakes
from boiler.definitions import ActivityType, ActorType
from boiler.models import ActivityList
from boiler.validate import (
    validate_activities,
    validate_activity,
    validate_activity_actor_types,
    validate_actor,
)

negative_tests = [
    ('v', ActivityType.PERSON_TALKS_TO_PERSON),
    ('', ActivityType.PERSON_TALKS_TO_PERSON),
    ('voo', ActivityType.VEHICLE_PICKS_UP_PERSON),
    ('p', ActivityType.PERSON_STEALS_OBJECT),
    ('poo', ActivityType.PERSON_UNLOADS_VEHICLE),
    ('bvb', ActivityType.PERSON_UNLOADS_VEHICLE),
]

positive_tests = [
    ('p', ActivityType.PERSON_TALKS_ON_PHONE),
    ('bopo', ActivityType.PERSON_STEALS_OBJECT),
    ('po', ActivityType.PERSON_STEALS_OBJECT),
    ('p', ActivityType.PERSON_ENTERS_SCENE_THROUGH_STRUCTURE),
    ('vp', ActivityType.PERSON_UNLOADS_VEHICLE),
    ('voooooooopooooooo', ActivityType.PERSON_UNLOADS_VEHICLE),
    ('DEADBEEF', ActivityType.CARRY_IN_HANDS),
]


@pytest.mark.parametrize('input_str,input_type', negative_tests)
def test_validate_activity_actor_string_negative(input_str, input_type):
    warnings, _ = validate_activity_actor_types(input_str, input_type, -1)
    assert len(warnings) == 1


@pytest.mark.parametrize('input_str,input_type', positive_tests)
def test_validate_activity_actor_string_positive(input_str, input_type):
    warnings, errors = validate_activity_actor_types(input_str, input_type, -1)

    assert not warnings
    assert not errors


def test_activity_invalid_combination():
    # incorrect combination of actors
    actor1 = fakes.ActorFactory(begin=0, end=5, actor_type=ActorType.BIKE, detections=[])
    actor2 = fakes.ActorFactory(begin=0, end=10, actor_type=ActorType.PERSON, detections=[])
    activity = fakes.ActivityFactory(
        begin=0,
        end=10,
        activity_type=ActivityType.PERSON_TRANSFERS_OBJECT,
        actors=[actor1, actor2],
    )
    with mock.patch('boiler.validate.validate_actor') as m:
        m.return_value = [], []
        warnings, _ = validate_activity(activity)

    assert 'spec' in str(warnings[0])


def test_validate_actor():
    # valid activity
    d0 = fakes.DetectionFactory(frame=12, keyframe=True)
    d1 = fakes.DetectionFactory(frame=24, keyframe=True)
    actor = fakes.ActorFactory(begin=12, end=24, actor_type=ActorType.VEHICLE, detections=[d0, d1])
    with mock.patch('boiler.validate.validate_detection') as m:
        m.return_value = [], []
        warnings, errors = validate_actor(actor, -1, -1)
        assert not warnings
        assert not errors


def test_valid_actor_detections_outside_activity_range():
    # detection out of range allowed
    d0 = fakes.DetectionFactory(frame=12, keyframe=True)
    d1 = fakes.DetectionFactory(frame=25, keyframe=True)
    actor = fakes.ActorFactory(begin=12, end=24, actor_type=ActorType.VEHICLE, detections=[d0, d1])
    with mock.patch('boiler.validate.validate_detection') as m:
        m.return_value = [], []
        warnings, errors = validate_actor(actor, -1, -1)
        assert not warnings
        assert not errors


def test_valid_actor_detections_outside_activity_range_no_keyframe():
    # detection out of range rejected if not keyframe
    d0 = fakes.DetectionFactory(frame=12, keyframe=True)
    d1 = fakes.DetectionFactory(frame=25, keyframe=False)
    actor = fakes.ActorFactory(begin=12, end=24, actor_type=ActorType.VEHICLE, detections=[d0, d1])
    with mock.patch('boiler.validate.validate_detection') as m:
        m.return_value = [], []
        warnings, errors = validate_actor(actor, -1, -1)
        assert 'last detection must be keyframe' in str(errors[0])


def test_valid_actor_non_monotomic_increasing_detections():
    d0 = fakes.DetectionFactory(frame=12)
    d1 = fakes.DetectionFactory(frame=12)
    actor = fakes.ActorFactory(begin=12, end=12, actor_type=ActorType.VEHICLE, detections=[d0, d1])
    with mock.patch('boiler.validate.validate_detection') as m:
        m.return_value = [], []
        warnings, errors = validate_actor(actor, -1, -1)
        assert 'was not greater than' in str(errors[0])


def test_keyframe_density_too_high():
    detections = [fakes.DetectionFactory(frame=frame, keyframe=True) for frame in range(12, 25)]
    actor = fakes.ActorFactory(
        begin=12, end=24, actor_type=ActorType.VEHICLE, detections=detections
    )
    with mock.patch('boiler.validate.validate_detection') as m:
        m.return_value = [], []
        warnings, errors = validate_actor(actor, -1, -1)
        assert 'keyframe density' in str(warnings[0])


def test_empty_activity_list():
    validate_activities(ActivityList(activity_map={}, actor_map={}))


@pytest.mark.parametrize('begin,end', [(5, 10), (35, 40), (25, 27),])
def test_invalid_actor_frame_range(begin, end):
    actor = fakes.ActorFactory(begin=begin, end=end, actor_type=ActorType.PERSON)
    activity = fakes.ActivityFactory(
        begin=20, end=30, actors=[actor], activity_type=ActivityType.PERSON_TALKS_ON_PHONE
    )
    with mock.patch('boiler.validate.validate_detection') as m:
        with mock.patch('boiler.validate.validate_actor') as m2:
            m.return_value, m2.return_value = ([], []), ([], [])
            warnings, errors = validate_activity(activity)
