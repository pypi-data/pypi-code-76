"""pytest file to store fixtures."""
import os

from ps.basic import DEV_STAGES

import pytest


@pytest.fixture(scope="module", params=DEV_STAGES.keys())
def dev_allowed_stages(request):
    os.environ["DEV_STAGE"] = request.param
    return request.param


@pytest.fixture(scope="module", params=["IMPOSSIBLE", "None", "EMPTY"])
def dev_wrong_stages(request):
    print("JUHU" + request.param)
    if request.param == "IMPOSSIBLE":
        os.environ["DEV_STAGE"] = request.param
    elif request.param == "None":
        os.environ.pop("DEV_STAGE")
    elif request.param == "EMPTY":
        os.environ["DEV_STAGE"] = ""
    else:
        raise
    return request.param
