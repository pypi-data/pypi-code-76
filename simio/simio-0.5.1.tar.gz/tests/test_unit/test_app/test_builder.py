import asyncio
from unittest.mock import Mock

import pytest
from more_itertools import first

from simio import Application
from simio.job import async_worker, async_cron
from simio.utils import deep_merge_dicts
from simio.app.default_config import get_default_config
from tests.conftest import TEST_APP_CONFIG


@pytest.mark.parametrize(
    "lhs, rhs, expected_result",
    (
        (
            {"key": {"key1": 2, "key2": 3,}, "key1": 1,},
            {"key": {"key1": 0, "key3": 4}, "key1": 2, "key2": 3,},
            {"key": {"key1": 0, "key2": 3, "key3": 4,}, "key1": 2, "key2": 3,},
        ),
    ),
)
def test_merge_configs(lhs, rhs, expected_result):
    result = deep_merge_dicts(lhs, rhs)
    assert result == expected_result


class TestAppBuilder:
    def test_initiated_app_config(self, app):
        assert app["config"] == deep_merge_dicts(get_default_config(), TEST_APP_CONFIG)

    def test_routes(self, app: Application):
        aiohttp_routes = app.app.router.routes()
        routes = set()

        for route in aiohttp_routes:
            routes.add((route.name, route.method))

        assert routes == {
            ("sample_handler_get", "GET"),
            ("sample_handler_post", "POST"),
            ("sample_handler_three_get", "GET"),
            ("sample_handler_two_get", "GET"),
        }

    @pytest.mark.asyncio
    async def test_created_async_workers(self, app):
        tasks = async_worker._running_tasks

        assert len(tasks) == 1

        task = first(tasks)
        result = await asyncio.gather(task)
        assert result[0] == 5

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_created_async_crons(self, app, builder_injector):
        crons = async_cron._running_tasks
        assert len(crons) == 1

        cron = first(crons)

        await cron.next()
        mock = builder_injector._deps_container.get(Mock)()
        mock.check.assert_called_with(alive=True)
