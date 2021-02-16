"""
Refiner answer deserialization into boiler models.
"""
from itertools import groupby
import json
from typing import Any, Dict, List, Optional, Union

from intervals import IntInterval

from boiler import activity_migration, definitions, models
from boiler import BoilerError


def invert_type_mapping(map: Dict[str, int]) -> Dict[int, str]:
    """Invert a refiner type mapping."""
    # For some reason, refiner answers provide the inverse of what you actually
    # need....
    return {v: k for k, v in map.items()}


def is_keyframe(detection: Dict[str, Any]) -> bool:
    # TODO: do we want to handle other types?
    return detection['src'] in ('ground-truth', 'truth')


def deserialize_detection(detection: Dict[str, Any]) -> models.Detection:
    box = detection['bbox']
    # refiner doesn't reliably send bounding boxes coordinates in the correct order
    return models.Detection(
        frame=detection['frame'],
        box=models.Box(
            left=min(box[0], box[2]),
            top=min(box[1], box[3]),
            right=max(box[0] + 1, box[2]),  # also protect against zero area boxes
            bottom=max(box[1] + 1, box[3]),
        ),
        keyframe=is_keyframe(detection),
    )


def deserialize_answers(answer_string: Union[str, Dict[str, Any]]) -> List[models.Activity]:
    if isinstance(answer_string, str):
        answer = json.loads(answer_string)
    else:
        answer = answer_string

    if 'types' not in answer or 'activities' not in answer or 'detections' not in answer:
        raise BoilerError('answer did not contain all required keys')

    types = answer['types']
    activities: List[models.Activity] = []
    for activity_id, activity in enumerate(answer['activities']):
        flat_detections = sorted(answer['detections'], key=lambda d: d['id1'])

        actor_type_map: Dict[int, definitions.ActorType] = {}
        for actor_type in types:
            actor_type_string = list(actor_type['cset3'].keys())[0].lower()
            actor_type_map[actor_type['id1']] = definitions.ActorType.from_string(actor_type_string)

        actor_map = {actor['id1']: actor for actor in activity.get('actors', [])}
        detection_map = groupby(flat_detections, lambda d: d['id1'])
        actors: List[models.Actor] = []

        for actor_id, detection_iterator in detection_map:
            answer_actor = actor_map[actor_id]
            actor_type = actor_type_map[actor_id]
            time_range: Optional[IntInterval] = None
            if 'timespan' in answer_actor:
                timespan = answer_actor['timespan']

                # sometimes refiner returns a dict rather than a list for the
                # actor's timespan /shrug
                if isinstance(timespan, dict):
                    timespan = [timespan['0']]
                time_range = IntInterval(timespan[0]['tsr0'])

            detections = [deserialize_detection(d) for d in detection_iterator]

            # sometimes the actor is missing a time range entirely, so
            # we fall back to deriving it from the detections
            if time_range is None:
                time_range = IntInterval([detections[0].frame, detections[-1].frame])

            actor = models.Actor(
                actor_id=actor_id,
                begin=time_range.lower,
                end=time_range.upper,
                actor_type=actor_type,
                detections=detections,
            )
            actors.append(actor)

        activity_id = activity['id2']
        activity_type_map = invert_type_mapping(activity['act2'])
        activity_type_name = activity_type_map[activity_id]
        if activity_type_name in activity_migration.activity_type_mapping:
            activity_type = activity_migration.activity_type_mapping[activity_type_name]
        else:
            activity_type = definitions.ActivityType(activity_type_map[activity_id])
        frame_range = IntInterval(activity['timespan'][0]['tsr0'])

        activities.append(
            models.Activity(
                activity_id=activity_id,
                activity_type=activity_type,
                begin=frame_range.lower,
                end=frame_range.upper,
                actors=actors,
            )
        )
    return activities


def deserialize_answer(answer_string: Union[str, Dict[str, Any]]) -> models.Activity:
    activities = deserialize_answers(answer_string)
    if len(activities) != 1:
        raise BoilerError('answer should contain exactly 1 activity')
    return activities[0]
