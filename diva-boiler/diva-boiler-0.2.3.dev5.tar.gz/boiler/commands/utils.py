import hashlib
from itertools import groupby
import json
from json.decoder import JSONDecodeError
from typing import BinaryIO, List, TextIO

import click
from requests import Response

from boiler.definitions import ActivityType
from boiler.models import ActivityList


def handle_request_error(r: Response) -> dict:
    if not r.ok:
        # TODO: inspect content-type to infer this
        error_text = r.text
        try:
            error_text = r.json()
        except ValueError:
            pass

        headers = dict(r.request.headers)
        headers.pop('X-Stumpf-Token', None)
        body = str(r.request.body)
        try:
            body = json.loads(body)
        except JSONDecodeError:
            pass

        return {
            'context': {
                'url': r.url,
                'method': r.request.method,
                'status': r.status_code,
                'body': body,
                'headers': headers,
            },
            'error': error_text,
        }
    return {'response': r.json()}


def exit_with(out: dict):
    click.echo(json.dumps(out, indent=2, sort_keys=True))
    if out.get('error'):
        exit(1)
    exit(0)


def sha1(file: BinaryIO) -> str:
    file.seek(0, 0)  # reset reader position
    m = hashlib.sha1()
    m.update(file.read())
    sha1 = m.hexdigest()
    file.seek(0, 0)
    return sha1


def activity_types_from_file(file: TextIO) -> List[str]:
    activity_types: List[str] = []
    for a in file.read().splitlines():
        if len(a) > 0:
            activity_types.append(ActivityType(a).value)
    return activity_types


def summarize_activities(activity_list: ActivityList):
    def activity_keyfunc(v):
        return v.activity_type

    def actor_keyfunc(v):
        return v.actor_type.value

    activity_counts = []
    for key1, group1 in activity_list.activity_types.items():
        group1_list = list(group1)
        activity_counts.append(
            {
                'name': key1.value,
                'count': len(group1_list),
                'frame_length_sum': sum([a.end - a.begin for a in group1_list]),
            }
        )

    actors = []
    for act in activity_list.activity_map.values():
        for actor in act.actors:
            actors.append(actor)
    actor_counts = []
    for key2, group2 in groupby(sorted(actors, key=actor_keyfunc), key=actor_keyfunc):
        group2_list = list(group2)
        actor_counts.append(
            {
                'name': key2,
                'count': len(group2_list),
                'frame_length_sum': sum([a.end - a.begin for a in group2_list]),
            }
        )

    return {
        'activities': {'count': len(activity_list.activity_map), 'by_type': activity_counts,},
        'actors': {'count': len(actors), 'by_type': actor_counts},
    }
