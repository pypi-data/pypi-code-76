import json
from unittest.mock import MagicMock, Mock

import pytest
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_response import Response

from tests.application import sample_handler_post


def coroutine_mock(return_value):
    async def _mock():
        return return_value

    return _mock


@pytest.mark.asyncio
async def test_handler_injection(builder_injector):
    handler = builder_injector._deps_container.get(sample_handler_post)
    injected_client = builder_injector._deps_container.get(Mock)()

    request_data = {
        "arg_one": "1",
        "arg_two": 1,
        "arg_three": False,
    }

    request = MagicMock()
    request.json = coroutine_mock(request_data)

    await handler(request=request)
    injected_client.handler.assert_called_with(injected=True)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_data, query, match_info, expected_result",
    (
        (
            {"arg_one": "1", "arg_two": 1, "arg_three": False,},
            {"query": "1"},
            {"user_id": "312"},
            {
                "user_id": 312,
                "data": {"arg_one": "1", "arg_two": 1, "arg_three": False,},
                "q": 1,
            },
        ),
        (
            {"arg_one": "1", "arg_two": 1, "arg_three": False,},
            {},
            {"user_id": "not_int"},
            {"error": "Cannot convert 'not_int' to <class 'int'>."},
        ),
        (
            {"arg_one": "1", "arg_two": 1, "arg_three": False,},
            {"query": "not"},
            {"user_id": "12"},
            {"error": "Cannot convert 'not' to <class 'int'>."},
        ),
        (
            {"arg_one": "1", "arg_two": "nooo", "arg_three": False,},
            {"query": "12"},
            {"user_id": "12"},
            {"error": {"arg_two": "value can't be converted to int"}},
        ),
    ),
    ids=[
        "success request",
        "incorrect match info",
        "incorrect query",
        "incorrect body",
    ],
)
async def test_request_validator(
    builder_injector, request_data, query, match_info, expected_result
):
    handler = builder_injector._deps_container.get(sample_handler_post)

    request = MagicMock()
    request.json = coroutine_mock(request_data)
    request.query = query
    request.match_info = match_info

    try:
        result: Response = await handler(request=request)
        assert json.loads(result.body) == expected_result
    except HTTPBadRequest as e:
        assert json.loads(e.body) == expected_result
