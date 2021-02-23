import asyncio
import json
from asyncio import AbstractEventLoop
from typing import List, Optional as Opt, Dict, Any, Iterable

from aiohttp import web
from simio_di import (
    DependencyInjector,
    DependenciesContainerProtocol,
    SingletoneDependenciesContainer,
)
from swagger_ui import aiohttp_api_doc

from simio.app.default_config import get_default_config
from simio.app.utils import initialize_all_modules
from simio.app.config_names import AppConfig
from simio.app.app import Application
from simio.handler import router
from simio.handler.routes import Router
from simio.handler.entities import AppRoute
from simio.utils import deep_merge_dicts
from simio.job import async_worker, async_cron
from simio.job.abstract import AbstractExecutor
from simio.swagger.entities import SwaggerConfig
from simio.swagger.fabric import swagger_fabric

DEFAULT_EXECUTORS = (
    async_worker,
    async_cron,
)
DEFAULT_ROUTERS = (router,)


class AppBuilder:
    def __init__(
        self,
        config: Dict[str, Any],
        loop: Opt[AbstractEventLoop] = None,
        deps_container: Opt[DependenciesContainerProtocol] = None,
        routers: Iterable[Router] = DEFAULT_ROUTERS,
        job_executors: Iterable[AbstractExecutor] = DEFAULT_EXECUTORS,
    ):
        default_config = get_default_config()

        if loop is None:
            loop = asyncio.get_event_loop()

        if deps_container is None:
            deps_container = SingletoneDependenciesContainer()

        self._loop = loop
        self._config = deep_merge_dicts(default_config, config)
        self._routers: List[Router] = []
        self._job_executors: List[AbstractExecutor] = []
        self._injector = DependencyInjector(self._config, deps_container=deps_container)
        self._app = None

        for router_ in routers:
            self.add_router(router_)

        for job_executor in job_executors:
            self.add_executor(job_executor)

        initialize_all_modules(self._config[AppConfig][AppConfig.app_path])

    @property
    def loop(self):
        return self._loop

    def add_router(self, app_router: Router):
        self._routers.append(app_router)

    def add_executor(self, executor: AbstractExecutor):
        self._job_executors.append(executor)

    def build_app(self, **runner_kwargs) -> Application:
        if self._app is not None:
            return self._app

        app = web.Application()
        app["config"] = self._config

        self._setup_routes(app)
        self._setup_executors(app)
        self._setup_swagger(app)

        self._app = Application(
            app_runner=web.AppRunner(app, **runner_kwargs), loop=self._loop,
        )
        return self._app

    def get_app_routes(self) -> List[AppRoute]:
        routes = []

        for app_router in self._routers:
            for route in app_router.routes:
                routes.append(route)

        return routes

    def _setup_executors(self, app: web.Application):
        for executor in self._job_executors:
            for job in executor.jobs:
                job.func = self._injector.inject(job.func)

            app.on_startup.append(executor.start)
            app.on_shutdown.append(executor.stop)

    def _setup_routes(self, app: web.Application):
        routes = []

        for route in self.get_app_routes():
            route.handler = self._injector.inject(route.handler)
            routes.append(route.as_route_def())

        app.add_routes(routes)

    def _setup_swagger(self, app: web.Application):
        if self._config[AppConfig][AppConfig.enable_swagger]:
            if self._config[AppConfig][AppConfig.autogen_swagger]:
                self._generate_swagger()

            aiohttp_api_doc(app, **self._config[AppConfig][AppConfig.swagger_config])

    def _generate_swagger(self) -> SwaggerConfig:
        """
        Generates and saves swagger to json file
        :return: SwaggerConfig object
        """
        swagger = swagger_fabric(self._config[AppConfig], self.get_app_routes())
        self._save_swagger(swagger)

        return swagger

    def _save_swagger(self, swagger: SwaggerConfig):
        """
        Writes SwaggerConfig object to json file
        :param swagger: SwaggerConfig object
        """
        path = self._config[AppConfig][AppConfig.swagger_config]["config_path"]

        with open(path, "w") as f:
            f.write(json.dumps(swagger.json(), indent=4, sort_keys=True))
