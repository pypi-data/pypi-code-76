"""
python object serialization for boiler models, mostly for debugging and
console logging purposes.  If you find yourself writing tools to parse
these, we should stop and evaluate why.
"""
from typing import Any, Callable, Dict, List

from boiler.models import Activity, Actor, Box, Detection


def deserialize_keyframes(detections: List[Dict[str, Any]]) -> List[Detection]:
    keyframes = [deserialize_detection(d) for d in detections if d['keyframe']]
    return sorted(keyframes, key=lambda d: d.frame)


def deserialize_detection(detection: Dict[str, Any]) -> Detection:
    box = Box(
        left=detection['left'],
        right=detection['right'],
        top=detection['top'],
        bottom=detection['bottom'],
    )
    return Detection(frame=detection['frame'], box=box, keyframe=detection['keyframe'])


def serialize_detection(detection: Detection):
    d = {
        'frame': detection.frame,
        'top': detection.box.top,
        'left': detection.box.left,
        'bottom': detection.box.bottom,
        'right': detection.box.right,
    }
    if detection.keyframe:
        d['keyframe'] = True
    return d


# DANGER: this function cannot be changed without a json-sche
def serialize_actor(actor: Actor, detection_serializer: Callable = serialize_detection):
    return {
        'type': actor.actor_type,
        'range': [actor.begin, actor.end],
        'detections': [detection_serializer(d) for d in actor.detections],
    }


def serialize_activity(
    activity: Activity,
    actor_serializer: Callable = serialize_actor,
    detection_serializer: Callable = serialize_detection,
):
    return {
        'type': activity.activity_type,
        'range': [activity.begin, activity.end],
        'actors': [
            actor_serializer(a, detection_serializer=serialize_detection) for a in activity.actors
        ],
    }
