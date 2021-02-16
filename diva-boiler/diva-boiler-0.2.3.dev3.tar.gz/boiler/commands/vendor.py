import click

from boiler import cli
from boiler.commands.utils import activity_types_from_file, exit_with, handle_request_error
from boiler.definitions import AnnotationVendors


@click.group(name='vendor', short_help='Manage annotation vendors')
@click.pass_obj
def vendor(ctx):
    pass


@vendor.command(name='search')
@click.pass_obj
def search(ctx, **kwargs):
    r = ctx['session'].get('annotation-vendor')
    exit_with(handle_request_error(r))


@vendor.command(name='dispatch')
@click.option('--name', type=click.Choice([v.value for v in AnnotationVendors]), required=True)
@click.option('--video-name', type=click.STRING, required=True)
@click.option('--activity-type-list', type=click.File(mode='r'), required=True)
@click.option('--set-name', type=click.STRING, required=True)
@click.option('--annotation-repo-path', type=click.STRING, required=True)
@click.pass_obj
def dispatch(ctx, name, video_name, activity_type_list, set_name, annotation_repo_path):
    activity_types = activity_types_from_file(activity_type_list)
    data = {
        'video_name': video_name,
        'vendor_name': name,
        'activity_types': activity_types,
        'set_name': set_name,
        'annotation_repo_path': annotation_repo_path,
    }
    r = ctx['session'].post('video-pipeline/annotate', json=data)
    exit_with(handle_request_error(r))


cli.add_command(vendor)
