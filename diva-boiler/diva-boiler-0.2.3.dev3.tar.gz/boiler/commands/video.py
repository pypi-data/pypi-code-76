from collections import defaultdict
import functools
import json
import operator
from pathlib import Path
import platform
import re
import subprocess
import sys
from typing import Dict
import uuid
from uuid import UUID

import attr
import boto3
from botocore.exceptions import WaiterError
import click

from boiler import BoilerSession, cli
from boiler.commands.utils import exit_with, handle_request_error
from boiler.definitions import CameraLocation, ReleaseBatches, Scenarios

video_name_regexp = re.compile(
    r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    r'\.(?P<start_hour>\d{2})-(?P<start_minute>\d{2})-(?P<start_second>\d{2})'
    r'\.(?P<end_hour>\d{2})-(?P<end_minute>\d{2})-(?P<end_second>\d{2})'
    r'\.(?P<location>[^.]+)'
    r'\.(?P<gtag>G[^.]+)$'
)
BUCKET = 'diva-mturk-ingestion-prod'

ELASTIC_TRANSCODER_PIPELINE_ID = '1536759483093-n34917'
ELASTIC_TRANSCODER_PORTRAIT_PRESET_ID = '1582841064651-nyezpa'
ELASTIC_TRANSCODER_LANDSCAPE_PRESET_ID = '1536756735287-cx0qtx'


def bold(x, **kwargs):
    return click.style(x, bold=True, **kwargs)


@attr.s(auto_attribs=True)
class VideoInfo:
    frame_rate: float
    duration: float
    width: int
    height: int
    name: str
    portrait: bool

    @classmethod
    def create(cls, file: str) -> 'VideoInfo':
        ffprobe = 'ffprobe'
        if platform.system() == 'Windows':
            ffprobe = 'ffprobe.exe'
        try:
            ps = subprocess.Popen(
                [ffprobe, '-print_format', 'json', '-show_streams', file],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            raise click.UsageError(f'Could not find {ffprobe} in your PATH, try install ffmpeg.')

        output = ps.communicate()[0]
        stream = json.loads(output)['streams'][0]
        stream['framerate'] = round(
            functools.reduce(
                operator.truediv, map(int, stream.get('avg_frame_rate', '').split('/'))
            )
        )
        return cls(
            frame_rate=stream['framerate'],
            duration=float(stream['duration']),
            width=int(stream['width']),
            height=int(stream['height']),
            name=str(Path(file).stem),
            portrait=int(stream['height']) > int(stream['width']),
        )

    def s3_path(self, id: UUID) -> str:
        _m = video_name_regexp.match(self.name)
        if _m is None:
            raise Exception('Could not parse video name')
        m = _m.groupdict()
        date = f'{m["year"]}-{m["month"]}-{m["day"]}'
        time = (
            f'{m["start_hour"]}-{m["start_minute"]}-{m["start_second"]}'
            f'{m["end_hour"]}-{m["end_minute"]}-{m["end_second"]}'
        )
        return f'uuid-encoded/{date}/{time}/{m["gtag"]}_{m["location"]}/{id}.mp4'


def _transcode_video(upload_id: str, video_info: VideoInfo):
    transcoder = boto3.client('elastictranscoder', region_name='us-east-1')
    job = transcoder.create_job(
        PipelineId=ELASTIC_TRANSCODER_PIPELINE_ID,
        Input={'Key': f'uploads/original/{upload_id}', 'FrameRate': 'auto'},
        Output={
            'Key': f'uploads/encoded/{upload_id}',
            'PresetId': ELASTIC_TRANSCODER_PORTRAIT_PRESET_ID
            if video_info.portrait
            else ELASTIC_TRANSCODER_LANDSCAPE_PRESET_ID,
        },
    )

    try:
        transcoder.get_waiter('job_complete').wait(Id=job['Job']['Id'], WaiterConfig={'Delay': 10})
    except WaiterError:
        raise Exception(f'an error occurred while transcoding {upload_id}')


def ingest_video(video_path: str, release_batch: str, phase: str, session: BoilerSession):
    video_name = Path(video_path).stem
    video_info = VideoInfo.create(video_path)
    upload_id = str(uuid.uuid4())

    if Path(video_path).suffix != '.avi':
        raise Exception('Expected a non-transcoded video')

    r = session.get('video', json={'name': video_name})
    r.raise_for_status()

    if r.json():
        click.echo(f'name={video_name} already exists', err=True)
        return

    try:
        s3 = boto3.client('s3')
        click.echo(f'uploading {video_name}..')
        s3.upload_file(video_path, BUCKET, f'uploads/original/{upload_id}')
    except Exception:
        click.echo('Could not upload file to S3.  Have you set up your credentials?', err=True)
        raise

    click.echo(f'transcoding {video_name}..')
    _transcode_video(upload_id, video_info)

    # create stumpf video and move encoded upload to correct location
    r = session.post('video/name', json={'video_name': video_name, 'release_batch': release_batch})
    if not r.ok:
        raise Exception(f'Could not generate new video for {video_name}')

    src_path = f'uploads/encoded/{upload_id}'
    dest_path = f'{video_info.s3_path(r.json()["id"])}'
    s3.copy_object(Bucket=BUCKET, CopySource={'Bucket': BUCKET, 'Key': src_path}, Key=dest_path)
    s3.delete_object(Bucket=BUCKET, Key=f'uploads/original/{upload_id}')
    s3.delete_object(Bucket=BUCKET, Key=src_path)

    resp = session.patch(
        f'video/{r.json()["id"]}',
        json={
            'duration': video_info.duration,
            'frame_rate': video_info.frame_rate,
            'height': video_info.height,
            'width': video_info.width,
            'phase': phase,
            'path': f'https://s3.amazonaws.com/{BUCKET}/{dest_path}',
        },
    )
    if not resp.ok:
        raise Exception(f'Could not set video metadata on {video_path}')
    click.echo(f'ingested {video_name} -> {r.json()["id"]}.')


@click.group(name='video', short_help='ingest and query video')
@click.pass_obj
def video(ctx):
    pass


@video.command(name='status', help='status of video annotation')
@click.argument('name', type=click.STRING)
@click.pass_obj
def status(ctx, name):
    r = ctx['session'].get('video', params={'name': name})
    if not r.ok and r.status_code != 404:
        exit_with(handle_request_error(r))
    elif r.status_code == 404 or not r.json():
        click.echo('Video not found, has it been ingested?', err=True)
        sys.exit(1)

    video_id = r.json()[0]['id']
    r = ctx['session'].get(f'video/{video_id}/status').json()

    click.echo('-' * len(name))
    click.secho(name, bold=True)
    click.echo('-' * len(name))
    click.echo(f'https://admin.stumpf.avidannotations.com/#/video/{video_id}')

    status = r['status']
    fg = 'red'
    if 'complete' in status:
        fg = 'green'
    click.echo(f'status: {bold(status, fg=fg)}')
    click.echo(f"activity types: {bold(str(r['activity_type_count']))}")
    for cauldron in r['cauldrons']:
        click.echo(f"\ncauldron: {bold(cauldron['path'])}")
        click.echo(f"  * vendor: {bold(cauldron['vendor'])}")
        click.echo(f"  * set: {bold(cauldron['set_name'])}")

    total = 0
    total_counts: Dict[str, int] = defaultdict(lambda: 0)
    activities: Dict[str, Dict[str, int]] = defaultdict(lambda: {})
    for a in r['activity_types']:
        total += a['count']
        total_counts[a['activity_type']] += a['count']
        activities[a['activity_type']][a['status']] = a['count']

    click.echo(f'\n{total} activities:')
    for name in sorted(activities.keys()):
        summary = activities[name]
        fg = 'green' if summary.get('good') == total_counts[name] else 'yellow'

        click.echo(f'  * {bold(name, fg=fg)} ({total_counts[name]})')
        for status in sorted(summary.keys()):
            if status == 'good':
                continue
            count = summary[status]
            click.echo(f'    * {status} ({count})')


@video.command(name='search', help='search for video')
@click.option('--name', type=click.STRING)
@click.option('--gtag', type=click.STRING)
@click.option('--location', type=click.Choice([e.value for e in CameraLocation]))
@click.option('--release-batch', type=click.Choice([e.value for e in ReleaseBatches]))
@click.option('--scenario', type=click.Choice([e.value for e in Scenarios]))
@click.option('--phase', type=click.STRING)
@click.option('--page', type=click.INT)
@click.option('--size', type=click.INT)
@click.pass_obj
def search(ctx, **kwargs):
    data = {}
    for key, value in kwargs.items():
        if value is not None:
            data[key] = value
    r = ctx['session'].get('video', params=data)
    exit_with(handle_request_error(r))


@video.command(name='add', short_help='ingest video into stumpf from file')
@click.argument(
    'videos',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    nargs=-1,
    required=True,
)
@click.option(
    '--release-batch', type=click.Choice([e.value for e in ReleaseBatches]), required=True
)
@click.option(
    '--phase',
    type=click.Choice(['m1', 'm2', 'meva', 'none', 'BWC', 'm2-boost', 'meva-training']),
    required=True,
)
@click.pass_obj
def add(ctx, videos, release_batch, phase):
    """Ingest locally transcoded video files into Stumpf.

    \b
    Videos are found in the following SMB shares:
    * //diva-nas06/m1-complete   (all m1 locations)
    * //diva-nas01/m2-albany     (alb)
    * //diva-nas03/m2n-keu       (gdb, Greo1)
    * //diva-nas05/m2-unimore    (uni)

    Mount with:
    \b
    mount -t cifs -o username=<user>,password=<password>,ro <share> <local>

    This command requires a working `ffprobe` in your path.
    """
    phase = None if phase == 'none' else phase

    for video in videos:
        ingest_video(video, release_batch, phase, ctx['session'])


@video.command(name='summary', short_help='get a summary of all videos')
@click.argument('output', type=click.File('wb'), default='-')
@click.pass_obj
def get_video_summary(ctx, output):
    """
    Get a summary of all videos in csv format.  By default, this will print to
    the terminal.  Add a path argument to write to a file.
    """
    r = ctx['session'].get('video/summary')
    output.write(r.content)


cli.add_command(video)
