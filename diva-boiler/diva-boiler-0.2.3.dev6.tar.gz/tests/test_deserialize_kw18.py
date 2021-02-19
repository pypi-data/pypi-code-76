from io import StringIO
from typing import Dict, List

import pytest

from boiler.definitions import ActorType
from boiler.models import Box, Detection
from boiler.serialization import ParseError
from boiler.serialization.kw18 import KW18FileSet


@pytest.fixture
def kw18():
    kw18_file = StringIO(
        """#
1 1037 4800 0 0 0 0 304 525 288 489 320 561 -1 444 444 0 2400 -1
1 1037 5836 0 0 0 0 1895 357.5 1881 331 1909 384 -1 444 444 0 2918 -1
2 94 5593 0 0 0 0 1325.5 1059.5 1216 1048 1435 1071 -1 444 444 0 2796.5 -1
2 94 5686 0 0 0 0 1345.5 1050.5 1235 1030 1456 1071 -1 444 444 0 2843 -1
3 75 5712 0 0 0 0 1360.5 1051.5 1234 1031 1487 1072 -1 444 444 0 2856 -1
3 75 5786 0 0 0 0 1216.5 1064.5 1090 1058 1343 1071 -1 444 444 0 2893 -1
"""
    )
    types_file = StringIO(
        """#
1 Person
2 Vehicle
3 Vehicle
"""
    )
    txt_file = StringIO(
        """#
0 8 144 -1.00000000000000005250e+300 4800 -1.00000000000000005250e+300 5836 1.0000000000e+000 1.000000e+000 1.000000e+000 0.000000e+000 0.000000e+000 1 1
0 10 145 -1.00000000000000005250e+300 5593 -1.00000000000000005250e+300 5686 1.0000000000e+000 1.000000e+000 1.000000e+000 0.000000e+000 0.000000e+000 1 2
0 44 146 -1.00000000000000005250e+300 5712 -1.00000000000000005250e+300 5786 1.0000000000e+000 1.000000e+000 1.000000e+000 0.000000e+000 0.000000e+000 1 3
"""  # noqa
    )
    yield {
        'kw18': kw18_file,
        'regions': None,
        'types': types_file,
        'txt': txt_file,
    }


@pytest.fixture
def geom_input():
    return StringIO(
        (
            '210 85 6813 0 0 0 DEADBEEF FEEDF00D 0 457 569 478 612\n'
            '210 85 6871 0 0 0 0 0 0 414 581 435 624\n'
            '210 85 6898 0 0 0 0 0 0 404 591 425 634\n'
            '211 107 7152 0 0 0 x 0 0 461 571 482 614\n'
            '211 107 7175 0 0 nonsense x 0 0 440 572 461 615\n'
            '211 107 7259 0 0 x x 0 0 402 592 423 635\n'
        )
    )


@pytest.fixture
def comment_input():
    return StringIO('# comment row \n')


def test_deserialize_types_ex1(comment_input):
    kw18 = KW18FileSet(types=comment_input)
    actor_map = kw18.read_actor_types()
    assert len(actor_map.values()) == 0


def test_deserialize_types_ex2():
    sinput = StringIO('1 Vehicle\n2 Vehicle\n1 Person\n')
    kw18 = KW18FileSet(types=sinput)
    actor_map = kw18.read_actor_types()
    assert len(actor_map.values()) == 2
    assert 1 in actor_map and 2 in actor_map
    assert 0 not in actor_map
    assert actor_map[1] == ActorType.PERSON
    assert actor_map[2] == ActorType.VEHICLE


def test_deserialize_geom_ex2(geom_input):
    kw18 = KW18FileSet(types=StringIO(''), kw18=geom_input)
    actor_map = kw18.read_detections()
    assert len(actor_map.values()) == 2
    assert 210 in actor_map and 211 in actor_map
    assert len(actor_map[210]) == 3
    assert len(actor_map[211]) == 3
    assert actor_map[210][0].frame == 6813
    assert actor_map[210][0].keyframe is True
    assert actor_map[210][0].box == Box(left=457, top=569, right=478, bottom=612)


def test_malformed_activities():
    actor_type_map = {0: ActorType.PERSON}
    detection_map: Dict[int, List[Detection]] = {0: []}
    kw18 = KW18FileSet()
    with pytest.raises(ParseError) as err:
        kw18._parse_activity_row(
            '0 24 144 0 4238 4312 0 0 0 0 0 1 216'.split(' '), actor_type_map, detection_map
        )
    assert 'Could not parse activity from the *.txt file' in str(err)


def test_deserialize_activities_ex1(kw18):
    kw18 = KW18FileSet(**kw18)
    activity_map = kw18.read().activity_map
    assert len(activity_map.values()) == 3
    assert len(activity_map[144].actors) == 1
    assert activity_map[144].begin == 4800
    assert activity_map[144].end == 5836
    assert activity_map[145].begin == 5593
    assert activity_map[145].end == 5686


# TODO: test multi-actor activity


def test_deserialize_regions(geom_input):
    sinput = StringIO(
        (
            '# [0:actor_id] [1:frame] [2:is_keyframe] [?] ...\n'
            '0 0 1 nonsense\n'
            '210 6813 0\n'
            '210 6898 400\n'
        )
    )
    kw18 = KW18FileSet(regions=sinput)
    interpolated_frames = kw18.read_interpolated_frames()
    assert len(interpolated_frames.values()) == 1
    assert {210} == set(interpolated_frames.keys())
    assert interpolated_frames[210] == {6813}
