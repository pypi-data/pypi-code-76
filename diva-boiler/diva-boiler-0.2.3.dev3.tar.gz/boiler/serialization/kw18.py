"""
KW18 is a csv-type format consisting of 3 files.
A row schema for each file is defined below.
[?] indicates an un-used row field.

file.txt: contains activity information.
[?] [1:ACTIVITY_TYPE_CODE] [2:ACTIVITY_ID] [?] [4:BEGIN]
[?] [6:END] [?] [?] [?] [?] [?] [12:N_PARTICIPANTS]
[ACTOR1_ID] [ACTOR2_ID] ...
[?] [ACTOR1_BEIGN] [?] [ACTOR1_END] [?] [ACTOR2_BEIGN] [?] [ACTOR2_END] ...

file.kw18: contains geometry information
[0:actor_id] [1:actor_track_length] [2:frame]
[?] [?] [?] [?] [?] [?] [9:top_left_x] [10:top_left_y] [11:bottom_right_x] [12:bottom_right_y]

file.kw18.types: contains actor type information
[0:ACTOR_ID] [1:ACTOR_TYPE]

file.kw18.regions: contains keyframe information
[0:actor_id] [1:frame] [2:is_keyframe] [?] ...
"""
from collections import defaultdict
import csv
import enum
from pathlib import Path
import re
from typing import Any, Dict, IO, Iterator, List, NamedTuple, Optional, Set

from boiler import BoilerError, BoilerSession
from boiler.definitions import ActivityType, ActorType, all_activity_codes
from boiler.models import Activity, ActivityList, Actor, Box, Detection
from boiler.serialization import error_handler, ParseError


ActivityMapType = Dict[int, Activity]
ActorMapType = Dict[int, Actor]

comment_re = re.compile('#.*$')


class ActivityRow(enum.IntEnum):
    TYPE = 1
    ID = 2
    BEGIN = 4
    END = 6
    ACTOR_COUNT = 12
    ACTOR_LIST_START = 13


class ActivityActorDetail(enum.IntEnum):
    BEGIN = 1
    END = 3


class GeomRow(enum.IntEnum):
    ACTOR_ID = 0
    ACTOR_TRACK_LENGTH = 1
    FRAME = 2
    LEFT = 9
    TOP = 10
    RIGHT = 11
    BOTTOM = 12


class RegionsRow(enum.IntEnum):
    ACTOR_ID = 0
    FRAME = 1
    KEYFRAME = 2


class TypesRow(enum.IntEnum):
    ID = 0
    TYPE = 1


class KW18FileSet(NamedTuple):
    txt: Optional[IO[str]] = None
    types: Optional[IO[str]] = None
    kw18: Optional[IO[str]] = None
    regions: Optional[IO[str]] = None

    def read(self) -> ActivityList:
        activities: List[Activity] = []
        if self.txt is not None:
            detection_map = self.read_detections()
            actor_type_map = self.read_actor_types()
            for row in self._read_file(self.txt):
                activities.append(self._parse_activity_row(row, actor_type_map, detection_map))

        return ActivityList.create_from_activity_list(activities)

    def _upload_file(self, file: Optional[IO[str]], session: BoilerSession) -> Optional[str]:
        if file is None:
            return None
        file.seek(0)
        r = session.post('upload', files={'file': file})
        if r.status_code not in (409, 201):
            raise Exception(f'Could not upload {file.name}')
        return r.json()['id']

    def upload(self, session: BoilerSession) -> Dict[str, Any]:
        """Upload a file set as a KW18FileUpload resource."""
        data = {
            'kw18_id': self._upload_file(self.kw18, session),
            'txt_id': self._upload_file(self.txt, session),
            'types_id': self._upload_file(self.types, session),
            'regions_id': self._upload_file(self.regions, session),
        }
        r = session.get('kw18-file-upload', json=data)
        if r.status_code == 200:
            values = r.json()
            if values:
                return values[0]

        r = session.post('kw18-file-upload', json=data)
        if r.status_code != 201:
            raise Exception('Could not upload KW18')
        return r.json()

    @classmethod
    def write(cls, base_name: str, activities: ActivityList):
        serialize_to_files(base_name, activities)

    @classmethod
    def create_from_path(cls, path: Path) -> 'KW18FileSet':
        """Create a KW18FileSet from a path on disk.

        This assumes there is *exactly* one *.kw18 file in the directory and
        that the other files have the same base name.
        """
        candidates = list(path.glob('*.kw18'))
        if len(candidates) > 1:
            raise FileNotFoundError('Provided path contains more than one kw18 file')
        elif not candidates:
            raise FileNotFoundError('Provided path does not contain any kw18 files')

        prefix = candidates[0].stem
        kw18 = candidates[0].open('r')
        return cls(
            kw18=kw18,
            txt=cls._maybe_open_file(path / (prefix + '.txt')),
            types=cls._maybe_open_file(path / (prefix + '.kw18.types')),
            regions=cls._maybe_open_file(path / (prefix + '.kw18.regions')),
        )

    @classmethod
    def _maybe_open_file(cls, path: Path) -> Optional[IO[str]]:
        if path.is_file():
            return path.open('r')

        return None

    @classmethod
    @error_handler('Could not parse activity from the *.txt file')
    def _parse_activity_row(
        cls,
        row: List[str],
        actor_type_map: Dict[int, ActorType],
        detection_map: Dict[int, List[Detection]],
    ) -> Activity:
        type_id = int(row[ActivityRow.TYPE])
        if type_id not in all_activity_codes:
            raise ParseError('Unknown activity type id "{type_id}"')

        activity_type = all_activity_codes[type_id]
        activity_id = int(row[ActivityRow.ID])
        begin = int(row[ActivityRow.BEGIN])
        end = int(row[ActivityRow.END])
        actor_count = int(row[ActivityRow.ACTOR_COUNT])

        actors = []
        for actor_index in range(actor_count):
            actor_id = int(row[ActivityRow.ACTOR_LIST_START + actor_index])
            start_index = ActivityRow.ACTOR_LIST_START + actor_count + actor_index * 4

            if actor_count == 1:
                actor_begin = begin
                actor_end = end
            else:
                actor_begin = int(row[start_index + ActivityActorDetail.BEGIN])
                actor_end = int(row[start_index + ActivityActorDetail.END])

            detections = [d for d in detection_map[actor_id]]
            if actor_id not in actor_type_map:
                raise ParseError(f'Unknown actor_id={actor_id} in activity file')

            actors.append(
                Actor(
                    actor_id=actor_id,
                    actor_type=actor_type_map[actor_id],
                    begin=actor_begin,
                    end=actor_end,
                    detections=detections,
                )
            )

        return Activity(
            activity_id=activity_id,
            activity_type=activity_type,
            begin=begin,
            end=end,
            actors=actors,
        )

    @classmethod
    def _get_file_lines(cls, f: IO[str]) -> Iterator[str]:
        for line in f:
            line = comment_re.sub('', line).strip()
            if line:
                yield line

    @classmethod
    def _read_file(cls, f: IO[str]) -> Iterator[List[str]]:
        for row in csv.reader(cls._get_file_lines(f), delimiter=' '):
            yield row

    @error_handler('Could not parse actors from the *.types file')
    def read_actor_types(self) -> Dict[int, ActorType]:
        if self.types is None:
            return {}
        rows = self._read_file(self.types)
        return {int(row[TypesRow.ID]): ActorType.from_string(row[TypesRow.TYPE]) for row in rows}

    @error_handler('Could not parse interpolated frames from the *.regions file')
    def read_interpolated_frames(self) -> Dict[int, Set[int]]:
        interpolated_frames: Dict[int, Set[int]] = defaultdict(set)

        if self.regions is not None:
            for row in self._read_file(self.regions):
                if row[RegionsRow.KEYFRAME] == '0':
                    actor_id = int(row[RegionsRow.ACTOR_ID])
                    frame = int(row[RegionsRow.FRAME])
                    interpolated_frames[actor_id].add(frame)

        return interpolated_frames

    @error_handler('Could not parse detections from the *.kw18 file')
    def read_detections(self) -> Dict[int, List[Detection]]:
        detections: Dict[int, List[Detection]] = defaultdict(list)
        if self.kw18 is None:
            return detections

        interpolated_frames = self.read_interpolated_frames()
        for row in self._read_file(self.kw18):
            frame = int(row[GeomRow.FRAME])
            actor_id = int(row[GeomRow.ACTOR_ID])
            if frame not in interpolated_frames[actor_id]:
                detections[actor_id].append(
                    Detection(
                        frame=frame,
                        box=Box(
                            left=int(row[GeomRow.LEFT]),
                            right=int(row[GeomRow.RIGHT]),
                            top=int(row[GeomRow.TOP]),
                            bottom=int(row[GeomRow.BOTTOM]),
                        ),
                        keyframe=True,
                    )
                )
        return detections


def find_activity_code(activity_type: ActivityType):
    for code, activity in all_activity_codes.items():
        if activity == activity_type:
            return code
    raise BoilerError(f'no numerical code exists for {activity_type.value}')


def serialize_types(actor_map: Dict[int, Actor]):
    for actor_id, actor in actor_map.items():
        row = [actor_id, actor.actor_type.value]
        yield ' '.join([str(d) for d in row]) + '\n'


def serialize_activities(
    activity_map: Dict[int, Activity], actor_map: Dict[int, Actor], filler_char
):
    inverse_actor_map = {actor: actor_id for actor_id, actor in actor_map.items()}
    for activity_id, activity in activity_map.items():
        row = [
            filler_char,
            find_activity_code(activity.activity_type),
            activity_id,
            filler_char,
            activity.begin,
            filler_char,
            activity.end,
            filler_char,
            filler_char,
            filler_char,
            filler_char,
            filler_char,
            len(activity.actors),
        ]
        for actor in activity.actors:
            actor_id = inverse_actor_map[actor]
            row.append(str(actor_id))

        if len(activity.actors) > 1:
            for actor in activity.actors:
                row += [filler_char, actor.begin, filler_char, actor.end]

        yield ' '.join([str(d) for d in row]) + '\n'


def serialize_geom(actor_map: Dict[int, Actor], filler_char):
    for actor_id, actor in actor_map.items():
        for detection in actor.detections:
            if detection.keyframe:
                row = [
                    actor_id,
                    actor.end - actor.begin,
                    detection.frame,
                    filler_char,
                    filler_char,
                    filler_char,
                    filler_char,
                    filler_char,
                    filler_char,
                ]
                row += list(detection.box)
                yield ' '.join([str(d) for d in row]) + '\n'


def serialize_to_files(
    output_basename: str, activity_list: ActivityList, filler_char='0',
):
    actor_map = activity_list.actor_map
    activity_map = activity_list.activity_map

    with open(output_basename + '.txt', 'w', encoding='utf-8') as yamlfile:
        for line in serialize_activities(activity_map, actor_map, filler_char):
            yamlfile.write(line)
    with open(output_basename + '.kw18.types', 'w', encoding='utf-8') as yamlfile:
        for line in serialize_types(actor_map):
            yamlfile.write(line)
    with open(output_basename + '.kw18', 'w', encoding='utf-8') as yamlfile:
        for line in serialize_geom(actor_map, filler_char):
            yamlfile.write(line)
