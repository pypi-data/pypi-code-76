from coegil.ApiService import set_configuration, api_get, api_save, get_environment
from coegil.Helpers import put_s3_object
import tempfile
import subprocess
import sys
import tarfile
import os
import click
import json


@click.group()
def cli():
    pass


@cli.command('configure', help="Configure your environment.")
@click.option('--key', prompt=True, hide_input=True, required=True, help="Your Coegil API key.")
@click.option('--env', required=False, default='prod', help="Optionally, set an environment.  "
                                                            "If you don't know what this is, leave it blank.")
def configure(key: str, env: str):
    set_configuration(env, key)


@cli.command('validate', help="Validate your environment.")
def validate():
    result = api_get('/public/management/key/validate', {})
    environment = get_environment()
    if environment != 'prod':
        result['environment'] = environment
    print(result)


@cli.command('query', help="Run an ad hoc database query.")
@click.argument('query_text')
@click.option('--asset_id', required=True, help="The asset's unique identifier.")
@click.option('--database_name', required=True, help="Your database artifact's name.")
@click.option('--engine', default='mysql', type=click.Choice(['mysql', 'athena'], case_sensitive=False),
              help='The database engine (defaults to mysql)')
def query(query_text: str, engine: str, asset_id: str, database_name: str):
    result = api_save('POST', f'/public/query/{engine}', {
        'asset_id': asset_id,
        'database_name': database_name,
        'query_text': query_text
    })
    _write_to_std_out(result)


@cli.command('saved-query', help="Run a saved database query.")
@click.option('--asset_id', required=True, help="The asset's unique identifier.")
@click.option('--query_name', required=True, help="Your saved query's name.")
@click.option('--parameters', required=False, help="Parameter overrides - passed as a JSON string of a dictionary.")
def saved_query(asset_id: str, query_name: str, parameters: str):
    result = api_save('POST', '/public/query/stored', {
        'asset_id': asset_id,
        'query_name': query_name,
        'query_params': None if parameters is None else json.loads(parameters)
    })
    _write_to_std_out(result)


@cli.command('invoke-schedule', help="Invoke a job or pipeline schedule..")
@click.option('--asset_id', required=True, help="The asset's unique identifier.")
@click.option('--job_name', required=True, help="The name of the job artifact (pipeline, notebook, or trigger).")
@click.option('--schedule_name', required=False, help="Required unless you are invoking a trigger.")
@click.option('--variable_override', required=False, help="Passed as a JSON string of a dictionary.")
def invoke_schedule(asset_id: str, job_name: str, schedule_name: str, variable_override: str):
    api_save('PUT', '/public/schedule', {
        'asset_id': asset_id,
        'job_name': job_name,
        'schedule_name': schedule_name,
        'variable_override': None if variable_override is None else json.loads(variable_override)
    })


@cli.command('save-file', help="Publish a python library to an asset.")
@click.option('--asset_id', required=True, help="The asset's unique identifier.")
@click.option('--file', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help="The location of the file to upload.")
@click.option('--artifact_name', required=False, help="The artifact's name.  If not specified, "
                                                      "it will be the file's name.")
def save_file(asset_id: str, file: str, artifact_name: str):
    artifact_name = os.path.basename(file) if artifact_name is None else artifact_name
    _upload_file(asset_id, artifact_name, file)


@cli.command('publish', help="Publish a python library to an asset.")
@click.option('--asset_id', required=True, help="The asset's unique identifier.")
@click.option('--package_name', required=True, help="Your package's name.")
@click.option('--library', required=True, type=click.Path(exists=True),
              help="The location of the Python library to package.")
def publish(asset_id: str, package_name: str, library: str):
    with tempfile.TemporaryDirectory() as wheel_destination:
        commands = [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            library,
            f'--wheel-dir={wheel_destination}'
        ]
        process = subprocess.Popen(commands, stderr=subprocess.PIPE)
        out, err = process.communicate()
        output = out.decode() if out is not None else ''
        error = err.decode()
        success = error == ''
        print(output)
        if not success:
            raise Exception(error)
        tar_file_name = os.path.join(wheel_destination, f'{package_name}.tar')
        with tarfile.open(tar_file_name, "w:gz") as tar:
            tar.add(wheel_destination, arcname=os.path.basename(wheel_destination))
        _upload_file(asset_id, package_name, tar_file_name, 'python_package')


def _upload_file(asset_id: str, artifact_name: str, file_location: str, artifact_sub_type: str = None):
    s3_credentials = api_get('/public/artifact/credentials', {
        'asset_id': asset_id,
        'artifact_name': artifact_name,
        'artifact_sub_type': artifact_sub_type
    })
    s3_bucket = s3_credentials['Bucket']
    s3_key = s3_credentials['Key']
    artifact_id = s3_credentials['ArtifactGuid']
    credential_override = s3_credentials['Credentials']
    content_type = None
    split_file_name = artifact_name.rsplit('.', 1)
    if len(split_file_name) > 1:
        extension = split_file_name[1]
        if extension == 'xlsx' or extension == 'xls':
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif extension == 'ppt' or extension == 'pptx':
            content_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        elif extension == 'docx':
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    with open(file_location, 'rb') as package:
        put_s3_object(s3_bucket, s3_key, package, content_type=content_type, credential_override=credential_override)
    api_save('POST', '/public/artifact', {
        'asset_id': asset_id,
        'artifacts': [{
            'artifact_name': artifact_name,
            'artifact_type': 'S3',
            'artifact_sub_type': artifact_sub_type,
            'artifact_id': artifact_id
        }]
    })


def _write_to_std_out(val, is_error=False):
    click.echo(json.dumps(val), err=is_error)


if __name__ == '__main__':
    cli()
