from typing import Any, Dict, IO, List

import click
from requests import Session

from boiler import cli
from boiler.commands.utils import (
    exit_with,
    handle_request_error,
    summarize_activities,
)
from boiler.serialization import (
    kpf as kpf_serialization,
    kw18 as kw18_serialization,
)
from boiler.validate import validate_activities

serializers = {'kw18': kw18_serialization}


class KPFIngestError(Exception):
    pass


def _upload_kpf_component(session: Session, file: IO[bytes]) -> Dict[str, Any]:
    file.seek(0)
    resp = session.post('upload', files={'file': file})
    file.seek(0)
    if resp.status_code == 409:
        # for these purposes, we don't care if it was a conflict or not
        resp.status_code = 201

    return handle_request_error(resp)


def _ingest_single_video(
    session: Session,
    types: IO[bytes],
    geom: IO[bytes],
    activities: IO[bytes],
    video_name: str,
    vendor_name: str,
    activity_type_list: List[str],
):
    types_id = _upload_kpf_component(session, types)
    geom_id = _upload_kpf_component(session, geom)
    activities_id = _upload_kpf_component(session, activities)

    data = {
        'activity_types': activity_type_list,
        'kpf_activities_id': activities_id,
        'kpf_geom_id': geom_id,
        'kpf_types_id': types_id,
        'validate_existing_files': True,  # set to False for faster no-op processing
        'vendor_name': vendor_name,
        'video_name': video_name,
    }
    resp = session.post('video-pipeline/process-annotation', json=data)
    return handle_request_error(resp)


@click.group(name='kpf', short_help='Ingest and validate kpf')
@click.pass_obj
def kpf(ctx):
    pass


@kpf.command(name='load', help='interact locally with the KPF format')
@click.option('--types', type=click.File(mode='rb'), help='path to types.yml')
@click.option('--geom', type=click.File(mode='rb'), help='path to geom.yml')
@click.option('--activities', type=click.File(mode='rb'), help='path to activities.yml')
@click.option('--validate', is_flag=True, help='run static integrity checks')
@click.option('--prune', is_flag=True, help='prune interpolated detections before validation')
@click.option(
    '--convert',
    nargs=2,
    type=click.Tuple(
        [
            click.Choice(serializers.keys()),
            click.Path(
                exists=False, file_okay=True, dir_okay=False, writable=True, resolve_path=True
            ),
        ]
    ),
    default=(None, None),
    help='convert to another serialization',
)
def load(types, geom, activities, validate, prune, convert):
    # TODO: fix
    raise NotImplementedError('This command is currently broken, sorry')

    actor_map = {}  # type: ignore
    activity_map = {}
    if types:
        kpf_serialization.deserialize_types(types, actor_map)
    if activities:
        kpf_serialization.deserialize_activities(activities, activity_map, actor_map)
    if geom:
        kpf_serialization.deserialize_geom(geom, actor_map)
    if prune:
        [a.prune() for a in activity_map.values()]

    output = {'summary': summarize_activities(list(activity_map.values()))}

    if validate:
        warnings, errors = validate_activities(activity_map.values())
        output['error'] = errors
        output['warning'] = warnings

    serialization_type = convert[0]
    base_path = convert[1]
    if serialization_type and base_path:
        serializer = serializers[serialization_type]
        serializer.serialize_to_files(
            base_path, activity_map.values(), actor_map.values(), keyframes_only=prune
        )

    exit_with(output)


cli.add_command(kpf)
