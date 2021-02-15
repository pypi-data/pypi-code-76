from typing import Dict

import pytest

from boiler import BoilerError
from boiler.definitions import ActorType
from boiler.models import Activity, Actor, Box
from boiler.serialization import kpf


def test_deserialize_types_ex1():
    actor_map_ex1: Dict[int, Actor] = {}
    input_ex1 = """
    - { meta: 'foo' }
    - { meta: { team: 'Kitware' } }
    """
    kpf.deserialize_types(input_ex1, actor_map_ex1)
    assert len(actor_map_ex1.values()) == 0


@pytest.mark.skip('Fix immmutable models')
def test_deserialize_types_ex2():
    actor_map_ex2: Dict[int, Actor] = {}
    input_ex2 = """
    - { types: { id1: 1, cset3: { Person: 1.0 } } }
    - { types: { id1: 2, cset3: { Vehicle: 1.0 } } }
    - { types: { id1: 2, cset3: { Horse: 1.0 } } }
    """
    kpf.deserialize_types(input_ex2, actor_map_ex2)
    assert len(actor_map_ex2.values()) == 2
    assert 1 in actor_map_ex2 and 2 in actor_map_ex2
    assert actor_map_ex2[1].actor_type == ActorType.PERSON.value  # type: ignore


def test_deserialize_types_ex3():
    actor_map_ex3: Dict[int, Actor] = {}
    input_ex3 = """
    - { types: { id1: 18, cset3: { Bag: 0.5, Person: 0.5 } } }
    """
    with pytest.raises(BoilerError) as err:
        kpf.deserialize_types(input_ex3, actor_map_ex3)
    assert 'cset3' in str(err.value)


@pytest.mark.skip('Fix immmutable models')
def test_deserialize_geom():
    actor_map_ex1: Dict[int, Actor] = {}
    input_ex1 = """
    - { meta: '2018-05-18.13-05-03.13-10-02.school.G336' }
    - { meta: { team: 'Kitware' } }
    - { geom: {id1: 1, ts0: 2, g0: 615 575 943 703, keyframe: true } }
    - { geom: {id1: 1, ts0: 1, g0: 20 897 934 510 } }
    - { foo: 'bar' }
    - { geom: {id1: 2, ts0: 2, g0: 70 865 926 530 } }
    - { geom: {id1: 2, ts0: 3, g0: 119 832 917 550 } }
    - { }
    - { geom: {id1: 2, ts0: 1, g0: 515 574 850 710, keyframe: true } }
    """
    kpf.deserialize_geom(input_ex1, actor_map_ex1)
    assert len(actor_map_ex1.values()) == 2
    assert 1 in actor_map_ex1 and 2 in actor_map_ex1
    assert len(actor_map_ex1[1].detections) == 2
    assert len(actor_map_ex1[2].detections) == 3
    assert actor_map_ex1[1].detections[0].frame == 1
    assert actor_map_ex1[2].detections[0].keyframe is True
    assert actor_map_ex1[1].detections[0].box == Box(left=20, top=897, right=934, bottom=510)


@pytest.mark.skip('Fix immmutable models')
def test_deserialize_activities():
    actor_map_ex1: Dict[int, Actor] = {}
    activity_map_ex1: Dict[int, Activity] = {}
    input_ex1 = (
        '- {act: {act2: {Vehicle_Moving: 1.0}, id2: 1, timespan: [{tsr0: [1, 100]}], actors: [{id1: 1, timespan: [{tsr0: [2508, 2751]}]}] } }\n'  # noqa: E501
        '- {meta: "Vehicle_PicksUp_Person 1 instances"}\n'
        '- {act: {act2: {Vehicle_Moving: 1.0}, id2: 2, timespan: [{tsr0: [200, 300]}], src_status: audited, actors: [{id1: 2, timespan: [{tsr0: [2869, 3015]}]}]}}'  # noqa: E501
    )
    kpf.deserialize_activities(input_ex1, activity_map_ex1, actor_map_ex1)
    assert len(activity_map_ex1.values()) == 2
    assert len(activity_map_ex1[1].actors) == 1
    assert activity_map_ex1[1].begin == 1
    assert activity_map_ex1[2].end == 300
