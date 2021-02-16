from pathlib import Path

import pytest

from boiler.serialization.refiner import deserialize_answer
from boiler.validate import validate_activity

HERE = Path(__file__).parent


@pytest.fixture
def refiner_answer():
    with (HERE / 'refiner_answer.json').open('r') as f:
        yield f.read()


def test_parse_answer(refiner_answer):
    activity = deserialize_answer(refiner_answer)
    validate_activity(activity)
    assert len(activity.actors) == 1
