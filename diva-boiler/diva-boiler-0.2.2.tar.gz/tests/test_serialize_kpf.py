# type: ignore
import pytest

from boiler.definitions import ActivityType, ActorType
from boiler.models import Activity, Actor, Box, Detection
from boiler.serialization import kpf


@pytest.mark.skip('Fix immutable models')
def test_serialize_types():
    actor1 = Actor(clip_id=1, actor_type=ActorType.VEHICLE)
    actor2 = Actor(clip_id=2, actor_type=ActorType.PERSON)
    actor3 = Actor(clip_id=3, actor_type=ActorType.PERSON)
    string_gen = kpf.serialize_types([actor1, actor2, actor3])
    produced = [s for s in string_gen]
    expected = [
        '- {types: {cset3: {Vehicle: 1.0}, id1: 1}}\n',
        '- {types: {cset3: {Person: 1.0}, id1: 2}}\n',
        '- {types: {cset3: {Person: 1.0}, id1: 3}}\n',
    ]
    assert produced == expected


@pytest.mark.skip('Fix immutable models')
def test_serialize_geom():
    b1 = Box(left=0, top=1, right=2, bottom=3)
    b2 = Box(left=2, top=4, right=6, bottom=8)
    b3 = Box(left=5, top=4, right=7, bottom=8)
    d1 = Detection(frame=0, box=b1, keyframe=True)
    d2 = Detection(frame=1, box=b2, keyframe=False)
    d3 = Detection(frame=2, box=b3, keyframe=True)
    actor1 = Actor(clip_id=1, actor_type=ActorType.VEHICLE, detections=[d1, d2, d3])
    actor2 = Actor(clip_id=2, actor_type=ActorType.PERSON, detections=[d1, d3])
    string_gen = kpf.serialize_geom([actor1, actor2])
    produced = [s for s in string_gen]
    expected = [
        '- {geom: {g0: 0 1 2 3, id0: 1, id1: 1, keyframe: true, ts0: 0}}\n',
        '- {geom: {g0: 2 4 6 8, id0: 2, id1: 1, ts0: 1}}\n',
        '- {geom: {g0: 5 4 7 8, id0: 3, id1: 1, keyframe: true, ts0: 2}}\n',
        '- {geom: {g0: 0 1 2 3, id0: 4, id1: 2, keyframe: true, ts0: 0}}\n',
        '- {geom: {g0: 5 4 7 8, id0: 5, id1: 2, keyframe: true, ts0: 2}}\n',
    ]
    assert produced == expected


@pytest.mark.skip('Fix immutable models')
def test_serialize_activities_no_id():
    actor1 = Actor(begin=0, end=2)
    actor2 = Actor(begin=1, end=2)
    actor3 = Actor(begin=3, end=4)
    activity1 = Activity(
        activity_type=ActivityType.PEOPLE_TALKING, begin=0, end=2, actors=[actor1, actor2],
    )
    activity2 = Activity(
        activity_type=ActivityType.PURCHASING, begin=3, end=4, status='foo', actors=[actor3],
    )
    # activity_map, _ = assign_entity_ids([activity1, activity2])
    activity_map = {0: activity1, 1: activity2}
    string_gen = kpf.serialize_activities(activity_map.values())
    produced = [s for s in string_gen]
    expected = [
        '- {act: {act2: {People_Talking: 1.0}, actors: [{id1: 1, timespan: [{tsr0: [0, 2]}]}, {id1: 2, timespan: [{tsr0: [1, 2]}]}], id2: 1, timespan: [{tsr0: [0, 2]}]}}\n',  # noqa: E501
        '- {act: {act2: {Purchasing: 1.0}, actors: [{id1: 3, timespan: [{tsr0: [3, 4]}]}], id2: 2, src_status: foo, timespan: [{tsr0: [3, 4]}]}}\n',  # noqa: E501
    ]
    assert produced == expected
