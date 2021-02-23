import time
import json
import threading
import requests

from fastapi.encoders import jsonable_encoder

from magicapi import g
from .Task import Task

from botocore.exceptions import ClientError


def run_tasks_locally(task):
    # make a dict but make sure dates are properly parsed
    d = json.loads(task.json())
    resp = requests.post(task.url, json=d)
    print("resp from local task", resp.content)


def save_tasks():
    if not g.tasks:
        return 0

    start = time.time()
    count = 0
    saved_tasks = []

    try:
        with Task.get_table().batch_writer() as batch:
            while len(g.tasks) and count < 25:
                task = g.tasks.pop(0)
                batch.put_item(Item=jsonable_encoder(task))
                saved_tasks.append(task)
                count += 1
    except ClientError as dynamo_error:
        print("Dynamo error likely so cannot save response:", dynamo_error)
        raise dynamo_error

    if g.settings.local:
        for task in saved_tasks:
            threading.Thread(target=run_tasks_locally, args=(task,)).start()
    return time.time() - start
