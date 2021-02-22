import os
from pathlib import Path
import datetime

import time

from mangum import Mangum

from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .config import MagicSettings, config_firestore

from magicapi.Globals.G import g


def add_cors(new_app):
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_sentry(new_app):
    from magicapi.Services.Sentry import SentryAsgiMiddleware, HAS_SENTRY_DSN

    if HAS_SENTRY_DSN:
        new_app.add_middleware(SentryAsgiMiddleware)


def add_tasks_and_process_time_middleware(new_app):
    from magicapi.Models.task_executor import save_tasks
    from magicapi.Models.NotFound import save_not_found_from_request

    @new_app.middleware("http")
    async def add_process_time_and_tasks(request: Request, call_next):
        start_time = time.time()
        g.request = request
        g.app = new_app
        print("url path", request.url.path, "***url", request.url)
        if "aws.context" in request.scope:
            context = request.scope["aws.context"]
            if hasattr(context, "serverless_sdk"):
                print("added context to endpoint!")
                context.serverless_sdk.set_endpoint(request.url.path)
        response = await call_next(request)
        if response.status_code in [404, 405] and g.settings.save_calls:
            await save_not_found_from_request(request)
        response.headers["X-Tasks-Time"] = str(save_tasks())  # queue tasks
        response.headers["X-Process-Time"] = str(time.time() - start_time)
        return response


def add_process_time_middleware(new_app):
    @new_app.middleware("http")
    async def add_process_time(request: Request, call_next):
        start_time = time.time()
        print("url path", request.url.path, "***url", request.url)
        if "aws.context" in request.scope:
            context = request.scope["aws.context"]
            if hasattr(context, "serverless_sdk"):
                print("added context to endpoint!")
                context.serverless_sdk.set_endpoint(request.url.path)
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time.time() - start_time)
        return response


def add_hello_world_testing_route(new_app):
    @new_app.get("/", tags=["boilerplate"])
    def read_root():
        print("hello world!")
        return {
            "Welcome": "!",
            # "cwd": Path.cwd(),
            # "dir": os.listdir(),
        }


def add_addons(new_app, only_server: bool = False):
    add_cors(new_app)
    add_sentry(new_app)
    if not only_server:
        add_tasks_and_process_time_middleware(new_app)
    else:
        add_process_time_middleware(new_app)
    add_hello_world_testing_route(new_app)


def add_background_tasks():
    from magicapi.Decorators.background_tasks import run_in_background


def make_magic_router():
    from magicapi.RouteClasses import MagicCallLogger

    magic_router = APIRouter(route_class=MagicCallLogger)
    g.magic_router = magic_router


def add_magic_routers():
    g.app.include_router(g.magic_router)


def set_settings(settings=MagicSettings()):
    g.settings = settings


def create_app(config_settings=MagicSettings(), only_server: bool = False):
    set_settings(config_settings)
    print("creating_app", datetime.datetime.now())
    new_app = FastAPI(
        title=config_settings.app_name,
        version=config_settings.version,
        root_path="" if config_settings.local else f"/{config_settings.stage}",
    )

    g.app = new_app
    if not only_server:
        add_background_tasks()
    if not only_server:
        make_magic_router()

    add_addons(g.app, only_server)

    config_firestore(g.settings.service_account_name)

    return g.app


from fastapi.routing import APIRoute


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


def create_handler(app):
    def handler(event, context):
        """Handler to give to lambda... which wraps FastAPI"""
        if event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
            print("Lambda is warm, now!!!")
            if hasattr(context, "serverless_sdk"):
                context.serverless_sdk.set_endpoint("/warmup")
            return {}

        asgi_handler = Mangum(app, api_gateway_base_path=g.settings.stage)
        response = asgi_handler(event, context)
        return response

    g.handler = handler
    return handler
