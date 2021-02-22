#!/usr/bin/env python
import os
import click
from click import echo, secho, pass_context, command, argument, option

import hjson
import logging
import subprocess
from collections import OrderedDict

from nextcode.packagelocal import package_and_upload
from nextcode.exceptions import ServerError, UploadError

from nextcodecli.utils import abort
from nextcodecli.utils import find_aws_credentials

log = logging.getLogger(__name__)


@command()
@argument('pipeline_name', required=False)
@argument('project_name', required=False)
@option('-p', '--parameters', help="Parameters for the run", multiple=True)
@option('-s', '--script', help="Git link to a workflow (only for custom)")
@option('-c', '--context', help="Optional context string")
@option('-r', '--revision', help="Git SHA to run")
@option('--profile', help="Nextflow configuration profile to use")
@option('--local', 'local_folder', help='Run a local nextflow folder')
@option('-f', '--file', 'job_filename', help='Run a manifest file')
@option(
    '-t',
    '--trace',
    is_flag=True,
    help='Inject trace directives to get more debugging information in nextflow log',
)
@option(
    '-q', '--nowait', is_flag=True, help='Do not execute the watch command for a running pipeline'
)
@option('-d', '--description', help='A human readable description of the job')
@option('--storage_type', help="Overrides the pipeline storage type for the run")
@option('-c', '--credentials', help="Credentials to forward to workflow-service", multiple=True)
@option('--executor_memory_mb', help='Override the memory limit of the nextflow executor')
@pass_context
def run(
    ctx,
    pipeline_name,
    project_name,
    parameters,
    script,
    context,
    revision,
    profile,
    local_folder,
    job_filename,
    nowait,
    trace,
    description,
    storage_type,
    credentials,
    executor_memory_mb,
):
    """
    Start a new nextflow job.

    Specify a named workflow and project or a manifest via --file.

    You can override all parameters in the file on the command-line via '-p key1=val1 -p key2=val2'

    If you are running against a debug server that allows direct script execution you
    can use 'custom' for pipeline_name.
    """
    credentials = creds_to_dict(credentials)
    manifest = {}
    params = {}
    if job_filename:
        with open(job_filename, 'r') as f:
            manifest = hjson.load(f)
        pipeline_name = pipeline_name or manifest.get('pipeline_name')
        project_name = project_name or manifest.get('project_name')
        script = script or manifest.get('script')
        revision = revision or manifest.get('revision')
        profile = profile or manifest.get('profile')
        context = context or manifest.get('context')
        params = manifest.get('params', {})
        credentials = credentials or manifest.get('credentials', {})
    try:
        override_params = {}
        for p in parameters:
            lst = p.split("=", 1)
            override_params[lst[0]] = lst[1].strip()
    except Exception:
        abort("Override parameters are badly formed. Expected '-p k1=v1 -p k2=v2'")

    for k, v in override_params.items():
        params[k] = v

    log.info(
        "Running pipeline '%s' on project '%s' with parameters %s",
        pipeline_name,
        project_name,
        dict(params),
    )

    creds = {}
    for upload_name, local_name in credentials.items():
        cred = find_aws_credentials(local_name)
        creds[upload_name] = {}
        creds[upload_name]['aws_access_key_id'] = cred['aws_access_key_id']
        creds[upload_name]['aws_secret_access_key'] = cred['aws_secret_access_key']
        if 'region' in cred:
            creds[upload_name]['region'] = cred['region']

    if not project_name:
        abort("You must specify PROJECT_NAME")
    if pipeline_name == 'custom' or not pipeline_name:
        if not script and not local_folder:
            abort(
                "If you are executing a custom script the you must specify a script or local folder"
            )
        pipeline_name = None
        if script and local_folder:
            abort("You cannot specify both a script and local folder")

    elif script or local_folder:
        abort("You cannot specify a script or local folder if you are running a named workflow")

    build_source = 'builtin'
    build_context = pipeline_name
    if local_folder:
        path = os.path.abspath(os.path.expanduser(local_folder))
        try:
            p = package_and_upload(ctx.obj.service, 'local_workflow', path)
        except UploadError as ex:
            abort(ex)
        build_source = 'url'
        build_context = p
    elif script:
        build_source = 'git'
        build_context = script

    try:
        job = ctx.obj.service.post_job(
            pipeline_name,
            project_name,
            params,
            script,
            revision or None,
            build_source,
            build_context,
            profile,
            trace,
            context=context,
            description=description,
            credentials=creds,
            storage_type=storage_type,
            executor_memory_mb=int(executor_memory_mb) if executor_memory_mb else None,
        )
    except ServerError as e:
        abort(str(e))

    secho('Job %s has been submitted' % job.job_id, bold=True)

    if not nowait:
        job_id = job.job_id
        cmd = ['nextcode', 'workflow', 'job', str(job_id), 'watch']
        echo("Executing %s..." % ' '.join(cmd))
        subprocess.call(cmd)


def creds_to_dict(credentials):
    """
    convert a list of string of the form ['upload=joe', 'download=joe']
    to an  ordered dict of the form {'upload': 'joe', 'download': 'joe'}
    """
    ret = OrderedDict()
    # credentials are supplied on the form 'upload=joe'
    # 'joe' being the local profile in ~/.aws/credentials
    # and 'upload' being the name we give the credentials
    # when forwarding to the workflow-service
    for cred in credentials:
        key, value = cred.split('=')
        ret[key] = value
    return ret
