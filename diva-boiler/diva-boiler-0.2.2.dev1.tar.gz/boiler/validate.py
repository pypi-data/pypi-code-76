from math import inf
import re
from typing import List, Tuple

from boiler import BoilerError, BoilerWarning
from boiler.definitions import activity_spec, ActivityType, actor_codes
from boiler.models import Activity, ActivityList, Actor, Detection

# Ideally, we set this higher, but theoretically there could be a 3 frame track...
MAX_KEYFRAME_RATIO = 0.75

PROBLEMS = Tuple[List[BoilerWarning], List[BoilerError]]


def validate_activity_actor_types(
    actor_string: str, activity_type: ActivityType, activity_id: int
) -> PROBLEMS:
    warnings: List[BoilerWarning] = []
    errors: List[BoilerError] = []
    pattern = activity_spec.get(activity_type)
    if pattern is not None:
        sorted_actor_string = ''.join(sorted(actor_string))
        pattern = f'^{pattern}$'
        result = re.match(pattern, sorted_actor_string)
        if result is None:
            warnings.append(
                BoilerWarning(
                    f'activity_id={activity_id} activity spec validation failed for {activity_type.value}:'  # noqa:E501
                    f' {sorted_actor_string} found, {activity_spec[activity_type]} expected'
                )
            )

    return warnings, errors


def validate_detection(detection: Detection, activity_id: int, frame: int) -> PROBLEMS:
    """
    * detections have 4 int corners
    * detection: top < bottom, left < right
    """
    warnings: List[BoilerWarning] = []
    errors: List[BoilerError] = []
    prefix = f'activity_id={activity_id} detection_frame={frame}'
    box = detection.box
    if not (box.left < box.right):
        errors.append(BoilerError(f'{prefix} left ({box.left}) should be < right ({box.right})'))
    if not (box.top < box.bottom):
        errors.append(BoilerError(f'{prefix} top ({box.top}) should be < bottom ({box.bottom})'))
    return warnings, errors


def validate_actor(actor: Actor, activity_id: int, actor_id: int) -> PROBLEMS:
    warnings: List[BoilerWarning] = []
    errors: List[BoilerError] = []
    prefix = f'activity_id={activity_id} actor_id={actor_id}'
    keyframe_count = 0
    last = None
    for detection in actor.detections:
        if last and detection.frame <= last.frame:  # type: ignore
            errors.append(  # type: ignore
                BoilerError(
                    f'{prefix} detection_frame={detection.frame} was not greater than {last.frame}'
                )
            )
        last = detection
        detection_warnings, detection_errors = validate_detection(
            detection, activity_id, detection.frame
        )
        if detection.keyframe:
            keyframe_count += 1

    if not (len(actor.detections) >= 2):
        errors.append(BoilerError(f'{prefix} actor must have at least a start and end frame'))
        return warnings, errors

    if not actor.detections[0].frame <= actor.begin:
        errors.append(BoilerError(f"{prefix} actor's first detection must be <= actor begin frame"))
    if not (actor.detections[0].keyframe):
        errors.append(BoilerError(f'{prefix} first detection must be keyframe'))
    if not (actor.detections[-1].frame >= actor.end):
        errors.append(
            BoilerError(f"{prefix} actor's final detection must must be >= actor end frame")
        )
    if not (actor.detections[-1].keyframe):
        errors.append(BoilerError(f'{prefix} last detection must be keyframe'))

    total_frames = actor.detections[-1].frame - actor.detections[0].frame + 1
    if not (keyframe_count <= MAX_KEYFRAME_RATIO * total_frames):
        warnings.append(
            BoilerWarning(
                f'{prefix} keyframe density {round(keyframe_count / total_frames * 100)}%'
                f' higher than {round(MAX_KEYFRAME_RATIO * 100)}%'
            )
        )

    return warnings, errors


def validate_activity(activity: Activity) -> PROBLEMS:
    """
    * actors involved are appropriate for activity type
    * actors framerange is within activity framerange
    """
    warnings: List[BoilerWarning] = []
    errors: List[BoilerError] = []
    actor_string = ''
    activity_type = ActivityType(activity.activity_type)
    first_actor_frame = inf
    last_actor_frame = 0
    activity_id = activity.activity_id
    for actor in activity.actors:
        actor_warnings, actor_errors = validate_actor(actor, activity.activity_id, actor.actor_id)
        warnings += actor_warnings
        errors += actor_errors
        actor_type = actor.actor_type
        actor_string += actor_codes[actor_type]
        first_actor_frame = min(first_actor_frame, actor.begin)
        last_actor_frame = max(last_actor_frame, actor.end)
        if actor.begin > activity.end:
            errors.append(
                BoilerError(
                    f'activity_id={activity_id} actor track must begin before activity ends'
                )
            )
        if actor.end < activity.begin:
            errors.append(
                BoilerError(f'activity_id={activity_id} actor track must end after activity begins')
            )
    if first_actor_frame > activity.begin:
        errors.append(
            BoilerError(
                f'activity_id={activity_id} there must be an actor at the first frame of an activity'  # noqa:E501
            )
        )
    if last_actor_frame < activity.end:
        errors.append(
            BoilerError(
                f'activity_id={activity_id} there must be an actor at the last frame of an activity'
            )
        )
    at_warnings, at_errors = validate_activity_actor_types(actor_string, activity_type, activity_id)
    return warnings + at_warnings, errors + at_errors


def validate_activities(activity_list: ActivityList) -> PROBLEMS:
    warnings: List[BoilerWarning] = []
    errors: List[BoilerError] = []
    for activity in activity_list:
        activity_warnings, activity_errors = validate_activity(activity)
        warnings += activity_warnings
        errors += activity_errors
    return warnings, errors
