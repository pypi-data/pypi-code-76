import json
from typing import List

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel, parse_obj_as

from lavender.models import Player, GameLog
from lavender.views.api.decorator import authenticated


class LogInstance(BaseModel):
    kind: str
    payload: str


@csrf_exempt
@authenticated
def save_logs(player: Player, request: HttpRequest):
    log_instances: List[LogInstance] = parse_obj_as(List[LogInstance], json.loads(request.body))
    logs = [
        GameLog(player=player, kind=log.kind, payload=log.payload)
        for log
        in log_instances
    ]
    GameLog.objects.bulk_create(logs)
    return HttpResponse()
