from typing import cast, Dict

from boiler import fakes
from boiler.definitions import ActorType
from boiler.models import Actor
from boiler.serialization import kw18


def test_serialize_types():
    actors = cast(
        Dict[int, Actor],
        {
            1: fakes.ActorFactory(actor_type=ActorType.VEHICLE, begin=0, end=10, detections=[]),
            2: fakes.ActorFactory(actor_type=ActorType.PERSON, begin=5, end=15, detections=[]),
            3: fakes.ActorFactory(actor_type=ActorType.PERSON, begin=2, end=9, detections=[]),
        },
    )
    string_gen = kw18.serialize_types(actors)
    produced = [s for s in string_gen]
    expected = ['1 vehicle\n', '2 person\n', '3 person\n']
    assert produced == expected


def test_serialize_geom():
    b1 = fakes.BoxFactory(left=0, top=1, right=2, bottom=3)
    b2 = fakes.BoxFactory(left=2, top=4, right=6, bottom=8)
    b3 = fakes.BoxFactory(left=5, top=4, right=7, bottom=8)
    d1 = fakes.DetectionFactory(frame=0, box=b1, keyframe=True)
    d2 = fakes.DetectionFactory(frame=1, box=b2, keyframe=False)
    d3 = fakes.DetectionFactory(frame=2, box=b3, keyframe=True)
    actor1 = fakes.ActorFactory(
        actor_type=ActorType.VEHICLE, detections=[d1, d2, d3], begin=0, end=2
    )
    actor2 = fakes.ActorFactory(actor_type=ActorType.PERSON, detections=[d1, d3], begin=0, end=0)
    string_gen = kw18.serialize_geom({1: actor1, 2: actor2}, '=')
    produced = [s for s in string_gen]
    expected = [
        '1 2 0 = = = = = = 0 1 2 3\n',
        '1 2 2 = = = = = = 5 4 7 8\n',
        '2 0 0 = = = = = = 0 1 2 3\n',
        '2 0 2 = = = = = = 5 4 7 8\n',
    ]
    assert produced == expected
