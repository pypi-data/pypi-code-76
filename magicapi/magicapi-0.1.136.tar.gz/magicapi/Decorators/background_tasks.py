import time
import requests
import os
from functools import wraps
import functools
from fastapi import Request, Body

from magicapi.Models.Task import Task, TaskParams
from magicapi.Models.BackgroundTask import BackgroundTask, Params

import inspect
from fastapi import HTTPException, APIRouter
import json
from datetime import datetime

from magicapi.Utils.random_utils import random_str
from magicapi.Errors import BackendException

from magicapi import g

from magicapi.Decorators.helpers import async_safe


def run_in_background_no_dynamo(f=None, background_url: str = None):
    if not f:
        if background_url and g.settings.local:
            background_url = None
        return functools.partial(
            run_in_background_no_dynamo, background_url=background_url
        )

    router_path = f"/run_in_background_no_dynamo/{f.__name__}"
    new_r = APIRouter()

    @new_r.post(router_path, tags=["background_tasks"], include_in_schema=False)
    async def endpoint(task: BackgroundTask):
        start = time.time()
        await async_safe(f, *task.params.args, **task.params.kwargs)
        time_took = time.time() - start
        task.finished_at = datetime.utcnow()
        task.task_took = datetime.utcnow()
        print(f"Finished {f.__name__}, task {task.id} in {time_took}.")
        return task

    g.app.include_router(new_r)

    @wraps(f)
    def wrapper(*args, **kwargs):
        task = BackgroundTask(
            params=Params(args=list(args), kwargs=kwargs), created_at=datetime.utcnow()
        )
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        url = f"{background_url or g.base_url}{router_path}"
        try:
            requests.post(
                url=url,
                data=task.json(),
                headers=headers,
                timeout=0.01,
            )
        except requests.exceptions.ReadTimeout:
            print(f"Sent {f.__name__} background task {task.id}, {url=}")

    return wrapper


def run_in_background(f=None, background_url: str = None):
    if not f:
        if background_url and g.settings.local:
            background_url = None
        return functools.partial(run_in_background, background_url=background_url)
    router_path = f"/run_in_background/{f.__name__}"
    new_r = APIRouter()

    @new_r.post(router_path, tags=["background_tasks_dynamo"], include_in_schema=False)
    async def endpoint(
        request: Request,
        task_id: str = Body(...),
        secret_token: str = Body(...),
        params: str = Body(...),
    ):
        if g.settings.print_level > 1:
            print("endpoint just received!", "params", params)
        # get the task from dynamo
        response = Task.get_table().get_item(Key={"task_id": task_id})
        task_dict = response.get("Item")
        if not task_dict:
            raise HTTPException(status_code=404, detail="Invalid task id.")

        task = Task(**task_dict)
        if not task or secret_token != task.secret_token:
            raise HTTPException(status_code=404, detail="Invalid task request.")

        if task.status != "in-lambda":
            # when local sometimes this happens before lambda changes queued to in-lambda
            if not task.local:
                raise HTTPException(
                    status_code=404, detail="This task was already completed."
                )

        j_params = json.loads(params)
        args = j_params.get("args", [])
        kwargs = j_params.get("kwargs", {})
        if g.settings.print_level > 1:
            print("inspect", inspect.signature(f), "a", args, "k", kwargs)

        await async_safe(f, *args, **kwargs)

        return {"success": True, "message": ""}

    g.app.include_router(new_r)

    @wraps(f)
    def wrapper(*args, **kwargs):
        if not os.getenv("HasDB"):
            raise BackendException(
                message="You cannot add tasks if you do not add a DB!"
            )

        if g.settings.print_level > 1:
            print("given to function", "args", args, "kwargs", kwargs)
        task_params = TaskParams(args=list(args), kwargs=kwargs)
        now = datetime.utcnow()

        base_url = background_url or g.base_url
        task = Task(
            task_id=random_str(30),
            url=base_url + router_path,
            status="queued",
            sent=False,
            secret_token=random_str(50),
            created_at=now,
            last_updated=now,
            params=task_params.json(),
            local=g.settings.local,
        )
        g.tasks.append(task)

        return task.task_id

    return wrapper
