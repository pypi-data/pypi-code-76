from . import holistic
from . import temporal


BUILTIN_FEATURES = {
    'duration': holistic.duration,
    'length': holistic.length,
    'start': holistic.start,
    'end': holistic.end,
    'velocity': [
        temporal.velocity,
        {'prepend_name': False},
    ],
    'acceleration': [
        temporal.acceleration,
        {'prepend_name': False},
    ],
    'jerk': [
        temporal.jerk,
        {'prepend_name': False},
    ],
    'angular_velocity': [
        temporal.angular_velocity,
        {'prepend_name': False},
    ],
    'angular_acceleration': [
        temporal.angular_acceleration,
        {'prepend_name': False},
    ],
}
