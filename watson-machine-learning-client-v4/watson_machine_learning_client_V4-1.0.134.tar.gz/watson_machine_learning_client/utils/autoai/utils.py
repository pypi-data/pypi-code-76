import io
import json
import os
from contextlib import redirect_stdout
from subprocess import check_call
from sys import executable
from tarfile import open as open_tar
from time import sleep
from typing import Dict, Union, Tuple, List, TYPE_CHECKING
from warnings import warn
from functools import wraps

import requests
from watson_machine_learning_client.wml_client_error import ApiRequestFailure

from .enums import RunStateTypes
from .errors import (MissingPipeline, AutoAIComputeError, DataFormatNotSupported, LibraryNotCompatible,
                     CannotInstallLibrary, CannotDownloadTrainingDetails, CannotDownloadWMLPipelineDetails,
                     VisualizationFailed)

if TYPE_CHECKING:
    from io import BytesIO, BufferedIOBase
    from pandas import DataFrame
    from collections import OrderedDict
    from sklearn.pipeline import Pipeline
    from watson_machine_learning_client import WatsonMachineLearningAPIClient
    from watson_machine_learning_client.helpers import DataConnection, S3Connection
    from ibm_boto3 import resource, client

__all__ = [
    'fetch_pipelines',
    'load_file_from_file_system',
    'NextRunDetailsGenerator',
    'prepare_auto_ai_model_to_publish',
    'remove_file',
    'RunDetailsGenerator',
    'is_ipython',
    'try_import_lale',
    'try_load_dataset',
    'check_dependencies_versions',
    'try_import_autoai_libs',
    'try_import_tqdm',
    'try_import_xlrd',
    'try_import_graphviz',
    'prepare_cos_client',
    'create_model_download_link',
    'create_summary',
    'prepare_auto_ai_model_to_publish_notebook',
    'get_node_and_runtime_index',
    'download_experiment_details_from_file',
    'prepare_model_location_path',
    'download_wml_pipeline_details_from_file',
    'init_cos_client',
    'check_graphviz_binaries'
]


def create_model_download_link(file_path: str):
    """
    Creates download link and shows it in the jupyter notebook

    Parameters
    ----------
    file_path: str, required
    """
    if is_ipython():
        from IPython.display import display
        from watson_machine_learning_client.utils import create_download_link
        display(create_download_link(file_path))


def fetch_pipelines(run_params: dict,
                    path: str,
                    pipeline_name: str = None,
                    load_pipelines: bool = False,
                    store: bool = False,
                    wml_client: 'WatsonMachineLearningAPIClient' = None) -> Union[None, Dict[str, 'Pipeline']]:
    """
    Helper function to download and load computed AutoAI pipelines (sklearn pipelines).

    Parameters
    ----------
    run_params: dict, required
        Fetched details of the run/fit.

    path: str, required
        Local system path indicates where to store downloaded pipelines.

    pipeline_name: str, optional
        Name of the pipeline to download, if not specified, all pipelines are downloaded.

    load_pipelines: bool, optional
        Indicator if we load and return downloaded piepelines.

    store: bool, optional
        Indicator to store pipelines in local filesystem

    wml_client: WatsonMachineLearningAPIClient, optional
        Should be passed when we are operating on CP4D instance.

    Returns
    -------
    List of sklearn Pipelines or None if load_pipelines is set to False.
    """

    def check_pipeline_nodes(pipeline: dict) -> None:
        """
        Automate check all pipeline nodes to find xgboost or lightgbm dependency.
        """
        # note: check dependencies for estimators
        for node in pipeline['context']['intermediate_model'].get('pipeline_nodes', []):
            if 'XGBClassifierEstimator' == node or 'XGBRegressorEstimator' == node:
                check_dependencies_versions(lib_name='xgboost', error=True)
            elif 'LGBMClassifierEstimator' == node or 'LGBMRegressorEstimator' == node:
                check_dependencies_versions(lib_name='lightgbm', error=True)
        # --- end note

    try:
        from sklearn.externals import joblib
    except ImportError:
        import joblib

    path = os.path.abspath(path)
    pipelines_names = []
    pipelines = {}

    if wml_client is not None:
        model_paths = []

        # note: iterate over all computed pipelines
        for pipeline in run_params['entity']['status'].get('metrics', []):

            # note: fetch and create model paths from file system
            model_path = pipeline['context']['intermediate_model']['location']['model']
            # --- end note

            # note: populate available pipeline names
            if pipeline_name is None:  # checking all pipelines
                model_paths.append(model_path)
                pipelines_names.append(
                    f"Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}")

                # note: check dependencies for estimators
                check_pipeline_nodes(pipeline=pipeline)

            # checking only chosen pipeline
            elif pipeline_name == f"Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}":
                model_paths.append(model_path)
                pipelines_names = [f"Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}"]

                # note: check dependencies for estimators
                check_pipeline_nodes(pipeline=pipeline)

                break
            # --- end note

        if load_pipelines:
            # Disable printing to suppress warning from ai4ml
            with redirect_stdout(open(os.devnull, "w")):
                for model_path, pipeline_name in zip(model_paths, pipelines_names):
                    pipelines[pipeline_name] = joblib.load(load_file_from_file_system(wml_client=wml_client,
                                                                                      file_path=model_path))

        if store:
            for name, pipeline in pipelines.items():
                local_model_path = os.path.join(path, name)
                joblib.dump(pipeline, local_model_path)
                print(f"Selected pipeline stored under: {local_model_path}")

                # note: display download link to the model
                create_model_download_link(local_model_path)
                # --- end note

    else:
        from ibm_boto3 import client
        cos_client = client(
            service_name=run_params['entity']['results_reference']['type'],
            endpoint_url=run_params['entity']['results_reference']['connection']['endpoint_url'],
            aws_access_key_id=run_params['entity']['results_reference']['connection']['access_key_id'],
            aws_secret_access_key=run_params['entity']['results_reference']['connection']['secret_access_key']
        )
        buckets = []
        filenames = []
        keys = []

        for pipeline in run_params['entity']['status'].get('metrics', []):

            if pipeline['context']['phase'] == 'global_output':
                model_path = f"{pipeline['context']['intermediate_model']['location']['model']}"

                if pipeline_name is None:
                    buckets.append(run_params['entity']['results_reference']['location']['bucket'])
                    filenames.append(
                        f"{path}/Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}.pickle")
                    keys.append(model_path)
                    pipelines_names.append(
                        f"Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}")

                    # note: check dependencies for estimators
                    check_pipeline_nodes(pipeline=pipeline)

                elif pipeline_name == f"Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}":
                    buckets = [run_params['entity']['results_reference']['location']['bucket']]
                    filenames = [
                        f"{path}/Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}.pickle"]
                    keys = [model_path]
                    pipelines_names = [f"Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}"]

                    # note: check dependencies for estimators
                    check_pipeline_nodes(pipeline=pipeline)

                    break

        for bucket, filename, key, name in zip(buckets, filenames, keys, pipelines_names):
            cos_client.download_file(Bucket=bucket, Filename=filename, Key=key)
            if load_pipelines:

                # Disable printing to suppress warning from ai4ml
                with redirect_stdout(open(os.devnull, "w")):
                    pipelines[name] = joblib.load(filename)

                if not store:
                    if os.path.exists(filename):
                        os.remove(filename)

                else:
                    print(f"Selected pipeline stored under: {filename}")

                    # note: display download link to the model
                    create_model_download_link(filename)
                    # --- end note

    if load_pipelines and pipelines:
        return pipelines

    elif load_pipelines:
        raise MissingPipeline(
            pipeline_name if pipeline_name is not None else "global_output pipeline",
            reason="The name of the pipeline is incorrect or there are no pipelines computed.")


def load_file_from_file_system(wml_client: 'WatsonMachineLearningAPIClient',
                               file_path: str,
                               stream: bool = True) -> 'io.BytesIO':
    """
    Load file into memory from the file system.

    Parameters
    ----------
    wml_client: WatsonMachineLearningAPIClient, required
        WML v4 client.

    file_path: str, required
        Path in the file system of the file.

    stream: bool, optional
        Indicator to stream data content.

    Returns
    -------
    Sklearn Pipeline
    """
    # note: prepare the file path
    file_path = file_path.split('auto_ml/')[-1]

    if wml_client.default_project_id:
        file_path = f"{file_path}?project_id={wml_client.default_project_id}"

    else:
        file_path = f"{file_path}?space_id={wml_client.default_space_id}"
    # --- end note

    buffer = io.BytesIO()

    response_with_model = requests.get(
        url=f"{wml_client.data_assets._href_definitions.get_wsd_model_attachment_href()}auto_ml/{file_path}",
        headers=wml_client._get_headers(),
        stream=stream,
        verify=False)

    if stream:
        for data in response_with_model.iter_content():
            buffer.write(data)
    else:
        buffer.write(response_with_model.content)

    buffer.seek(0)

    return buffer


class NextRunDetailsGenerator:
    """
    Generator class to produce next list of run details.

    Parameters
    ----------
    wml_client: WatsonMachineLearningAPIClient, required
        WML Client Instance
    """

    def __init__(self, wml_client: 'WatsonMachineLearningAPIClient', href: str) -> None:
        self.wml_client = wml_client
        self.next_href = href

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_href is not None:
            response = requests.get(
                url=f"{self.wml_client.wml_credentials['url']}{self.next_href}",
                headers=self.wml_client._get_headers(),
                verify=not self.wml_client.ICP)
            details = response.json()
            self.next_href = details.get('next', {'href': None})['href']
            return details.get('resources', [])

        else:
            raise StopIteration


def prepare_auto_ai_model_to_publish_notebook(pipeline_model: Union['Pipeline', 'TrainablePipeline'],
                                              result_connection,
                                              cos_client) -> str:
    """
    Prepares autoai model to publish in Watson Studio via COS.
    Option only for auto-gen notebooks with correct result references on COS.

    Parameters
    ----------
    pipeline_model: Union['Pipeline', 'TrainablePipeline'], required
        model object to publish

    result_connection: DataConnection, required
        Connection object with COS credentials and all needed locations for jsons

    cos_client: ibm_boto3.resource, required
        initialized COS client

    Returns
    -------
    String with path to the saved model and jsons in COS.
    """
    try:
        from sklearn.externals import joblib
    except ImportError:
        import joblib
    from ibm_boto3 import resource

    wml_pipeline_definition_name = "pipeline-model.json"
    temp_model_name = '__temp_model.pickle'

    # note: path to the json describing the autoai POD specification
    path = result_connection.location._model_location.split('model.pickle')[0]
    pipeline_model_json_path = f"{path}pipeline-model.json"
    schema_path = f"{path}schema.json"

    bucket = result_connection.location.bucket

    # note: need to download model schema and wml pipeline definition json
    cos_client.meta.client.download_file(Bucket=bucket, Filename=wml_pipeline_definition_name,
                                         Key=pipeline_model_json_path)
    cos_client.meta.client.download_file(Bucket=bucket, Filename='schema.json', Key=schema_path)

    # note: save model temporally
    joblib.dump(pipeline_model, temp_model_name)

    # note: make writable cos client
    details = download_experiment_details_from_file((result_connection, cos_client))
    connection = details['entity']['results_reference']['connection']
    writable_cos_client = resource(
        service_name='s3',
        endpoint_url=connection['endpoint_url'],
        aws_access_key_id=connection['access_key_id'],
        aws_secret_access_key=connection['secret_access_key']
    )
    # --- end note

    # note: workaround for the cloud deployment, storing model, schema and pipeline definition on COS
    path = f"auto-gen-notebook-tmp-files/"
    writable_cos_client.meta.client.upload_file(
        Filename=temp_model_name,
        Bucket=bucket,
        Key=f"{path}model.pickle")
    writable_cos_client.meta.client.upload_file(
        Filename='schema.json',
        Bucket=bucket,
        Key=f"{path}schema.json")
    writable_cos_client.meta.client.upload_file(
        Filename=wml_pipeline_definition_name,
        Bucket=bucket,
        Key=f"{path}{wml_pipeline_definition_name}")

    # note: clean up local storage
    remove_file(filename='schema.json')
    remove_file(filename=temp_model_name)
    remove_file(filename=wml_pipeline_definition_name)

    return path


def prepare_auto_ai_model_to_publish(
        pipeline_model: Union['Pipeline', 'TrainablePipeline'],
        run_params: dict,
        run_id: str,
        wml_client: 'WatsonMachineLearningAPIClient' = None) -> Union[Tuple[Dict[str, dict], str], str]:
    """
    Helper function to download and load computed AutoAI pipelines (sklearn pipelines).

    Parameters
    ----------
    pipeline_model: Union['Pipeline', 'TrainablePipeline'], required
        Model that will be prepared for an upload.

    run_params: dict, required
        Fetched details of the run/fit.

    run_id: str, required
        Fit/run ID associated with the model.

    wml_client: WatsonMachineLearningAPIClient, optional
        Indicator if we are working on top of cp4d or cloud. Only CP4D version needs to have a WML client passed.

    Returns
    -------
    If cp4d: Dictionary with model schema and artifact name to upload, stored temporally in the user local file system.
    else: path name to the stored model in COS
    """

    try:
        from sklearn.externals import joblib
    except ImportError:
        import joblib

    artifact_name = "artifact_auto_ai_model.tar.gz"
    model_artifact_name = f"model_{run_id}.tar.gz"
    wml_pipeline_definition_name = "pipeline-model.json"
    temp_model_name = '__temp_model.pickle'

    # note: prepare file paths of pipeline-model and schema (COS / file system location)
    pipeline_info = run_params['entity']['status'].get('metrics')[-1]
    pipeline_model_path = f"{pipeline_info['context']['intermediate_model']['location']['pipeline_model']}"
    schema_path = f"{pipeline_info['context']['intermediate_model']['schema_location']}"
    # --- end note

    if wml_client:
        # note: downloading pipeline-model.json and schema.json from file system on CP4D
        schema_json = load_file_from_file_system(wml_client=wml_client, file_path=schema_path).read().decode()
        pipeline_model_json = load_file_from_file_system(wml_client=wml_client,
                                                         file_path=pipeline_model_path).read().decode()
        with open(wml_pipeline_definition_name, 'w') as f:
            f.write(pipeline_model_json)
        # --- end note

        # note: update the schema, it has wrong field types
        schema_json = schema_json.replace('fieldType', 'type')
        # --- end note

        # note: saved passed model as pickle, for further tar.gz packaging
        joblib.dump(pipeline_model, temp_model_name)
        # --- end note

        # note: create a tar.gz file with model pickle, name it as 'model_run_id.tar.gz', model.pickle inside
        with open_tar(model_artifact_name, 'w:gz') as tar:
            tar.add(temp_model_name, arcname='model.pickle')

        remove_file(filename=temp_model_name)
        # --- end note

        # note: create final tar.gz to publish on WML (includes pipeline config and tar.gz with model)
        with open_tar(artifact_name, 'w:gz') as tar:
            tar.add(model_artifact_name)
            tar.add(wml_pipeline_definition_name)

        remove_file(filename=model_artifact_name)
        remove_file(filename=wml_pipeline_definition_name)
        # --- end note

        return json.loads(schema_json), artifact_name

    else:
        cos_client = init_cos_client(run_params['entity']['results_reference']['connection'])
        bucket = run_params['entity']['results_reference']['location']['bucket']

        # note: need to download model schema and wml pipeline definition json
        cos_client.meta.client.download_file(Bucket=bucket, Filename=wml_pipeline_definition_name,
                                             Key=pipeline_model_path)
        cos_client.meta.client.download_file(Bucket=bucket, Filename='schema.json', Key=schema_path)

        # note: save model temporally
        joblib.dump(pipeline_model, temp_model_name)

        # note: workaround for the cloud deployment, storing model, schema and pipeline definition on COS
        path = f"{run_params['entity']['results_reference']['location']['path']}/{run_params['metadata']['guid']}/"

        # note: change model location in pipeline-mode.json to new one
        modify_pipeline_model_json(data_location=wml_pipeline_definition_name, model_path=path)

        cos_client.meta.client.upload_file(
            Filename=temp_model_name,
            Bucket=bucket,
            Key=f"{path}model.pickle")
        cos_client.meta.client.upload_file(
            Filename='schema.json',
            Bucket=bucket,
            Key=f"{path}schema.json")
        cos_client.meta.client.upload_file(
            Filename=wml_pipeline_definition_name,
            Bucket=bucket,
            Key=f"{path}{wml_pipeline_definition_name}")

        # note: clean up local storage
        remove_file(filename='schema.json')
        remove_file(filename=temp_model_name)
        remove_file(filename=wml_pipeline_definition_name)

        return path


def modify_pipeline_model_json(data_location: str, model_path: str) -> None:
    """
    Change the location of KB model in pipeline-model.json

    Parameters
    ----------
    data_location: str, required
        pipeline-model.json data local path

    model_path: str, required
        Path to KB model stored in COS.
    """
    with open(data_location, 'r') as f:
        data = json.load(f)

    data['pipelines'][0]['nodes'][-1]['parameters']['output_model']['location'] = f"{model_path}model.pickle"

    with open(data_location, 'w') as f:
        f.write(json.dumps(data))


def init_cos_client(connection: dict) -> 'resource':
    """Initiate COS client for further usage."""
    from ibm_botocore.client import Config
    from ibm_boto3 import resource

    if connection.get('auth_endpoint') is not None and connection.get('api_key') is not None:
        cos_client = resource(
            service_name='s3',
            ibm_api_key_id=connection['api_key'],
            ibm_auth_endpoint=connection['auth_endpoint'],
            config=Config(signature_version="oauth"),
            endpoint_url=connection['endpoint_url']
        )

    else:
        cos_client = resource(
            service_name='s3',
            endpoint_url=connection['endpoint_url'],
            aws_access_key_id=connection['access_key_id'],
            aws_secret_access_key=connection['secret_access_key']
        )
    return cos_client


def remove_file(filename: str):
    """Helper function to clean user local storage from temporary package files."""
    if os.path.exists(filename):
        os.remove(filename)


class RunDetailsGenerator:
    """
    Generator class to produce specified run details. Needed for progress bar.

    Parameters
    ----------
    wml_client: WatsonMachineLearningAPIClient, required
        WML Client Instance

    run_id: str, required
        ID of the run/fit.

    wait_time: float, required
        Waiting time in seconds, how long we will wait until next details will be fetched.
    """

    def __init__(self, wml_client: 'WatsonMachineLearningAPIClient', run_id: str, wait_time: float) -> None:
        self._wml_client = wml_client
        self.run_id = run_id
        self.wait_time = wait_time
        self.finished = False
        status = self._wml_client.training.get_status(training_uid=self.run_id)
        self.message = status.get('message', {}).get('text', 'Started waiting for resources.').split(': ')[-1]

    def __iter__(self):
        return self

    def __next__(self):
        sleep(self.wait_time)
        try:
            status = self._wml_client.training.get_status(training_uid=self.run_id)
            state = status.get('state')
            message = status.get('message', {}).get('text', 'Started waiting for resources.').split(': ')[-1]

        except ApiRequestFailure as e:
            state = {'state': 'ApiRequestFailure'}
            message = f'{e}, reconnecting...'

        if state == RunStateTypes.FAILED:
            sleep(3)
            try:
                status = self._wml_client.training.get_status(training_uid=self.run_id)
                message = status.get('failure', {}).get('errors', [])
            except ApiRequestFailure as e:
                message = f'{e}, reconnecting...'

            if 'Not Found' in str(message) or 'HeadObject' in str(message):
                raise AutoAIComputeError(self.run_id,
                                         reason=f"Fetching training data error. Please check if COS credentials, "
                                                f"bucket name and path are correct or file system path is correct.")

            elif 'Failed_Image' in str(message):
                raise AutoAIComputeError(
                    self.run_id,
                    reason=f"This version of WML V4 SDK with AutoAI component is no longer supported. "
                           f"Please update your package to the newest version. "
                           f"Error: {message}")

            else:
                raise AutoAIComputeError(self.run_id, reason=f"Error: {message}")

        # note: additional checks, OBM produces similar completed message state, we need to finish only when KB finished
        elif state == RunStateTypes.COMPLETED and 'Training job' in message and 'completed' in message:
            if self.finished:
                raise StopIteration
            else:
                self.finished = True
                return message

        else:
            return message


def is_ipython():
    """Check if code is running in the notebook."""
    try:
        name = get_ipython().__class__.__name__
        if name != 'ZMQInteractiveShell':
            return False
        else:
            return True

    except Exception:
        return False


def try_import_lale():
    """
    Check if lale package is installed in local environment, if not, just download and install it.
    """
    lale_version = '0.3.18'
    try:
        import lale
        from packaging import version
        if version.parse(lale.__version__) < version.parse(lale_version):
            warn(f"\"lale\" package version is to low."
                 f"Installing version >={lale_version}")

            try:
                check_call([executable, "-m", "pip", "install", f"lale>={lale_version}"])

            except Exception as e:
                raise CannotInstallLibrary(value_name=e,
                                           reason="lale failed to install. Please install it manually.")

    except AttributeError:
        warn(f"Cannot determine \"lale\" package version."
             f"Installing version >={lale_version}")

        try:
            check_call([executable, "-m", "pip", "install", f"lale>={lale_version}"])

        except Exception as e:
            raise CannotInstallLibrary(value_name=e,
                                       reason="lale failed to install. Please install it manually.")

    except ImportError:
        warn(f"\"lale\" package is not installed. "
             f"This is the needed dependency for pipeline model refinery, we will try to install it now...")

        try:
            check_call([executable, "-m", "pip", "install", f"lale>={lale_version}"])

        except Exception as e:
            raise CannotInstallLibrary(value_name=e,
                                       reason="lale failed to install. Please install it manually.")


def try_import_autoai_libs():
    """
    Check if autoai_libs package is installed in local environment, if not, just download and install it.
    """
    try:
        import autoai_libs

    except ImportError:
        warn(f"\"autoai_libs\" package is not installed. "
             f"This is the needed dependency for pipeline model refinery, we will try to install it now...")

        try:
            check_call([executable, "-m", "pip", "install", "autoai_libs>=1.11.0"])

        except Exception as e:
            raise CannotInstallLibrary(value_name=e,
                                       reason="autoai_libs>=1.11.0 failed to install. Please install it manually.")


def try_import_tqdm():
    """
    Check if tqdm package is installed in local environment, if not, just download and install it.
    """
    try:
        import tqdm

    except ImportError:
        warn(f"\"tqdm\" package is not installed. "
             f"This is the needed dependency for pipeline training, we will try to install it now...")

        try:
            check_call([executable, "-m", "pip", "install", "tqdm==4.43.0"])

        except Exception as e:
            raise CannotInstallLibrary(value_name=e,
                                       reason="tqdm==4.43.0 failed to install. Please install it manually.")


def try_import_xlrd():
    """
    Check if xlrd package is installed in local environment, if not, just download and install it.
    """
    try:
        import xlrd

    except ImportError:
        warn(f"\"xlrd\" package is not installed. "
             f"This is the needed dependency for loading dataset from xls files, we will try to install it now...")

        try:
            check_call([executable, "-m", "pip", "install", "xlrd==1.2.0"])

        except Exception as e:
            raise CannotInstallLibrary(value_name=e,
                                       reason="xlrd==1.2.0 failed to install. Please install it manually.")


def try_import_graphviz():
    """
    Check if graphviz package is installed in local environment, if not, just download and install it.
    """
    try:
        import graphviz

    except ImportError:
        warn(f"\"graphviz\" package is not installed. "
             f"This is the needed dependency for visualizing data join graph, we will try to install it now...")

        try:
            check_call([executable, "-m", "pip", "install", "graphviz==0.14"])

        except Exception as e:
            raise CannotInstallLibrary(value_name=e,
                                       reason="graphviz==0.14 failed to install. Please install it manually.")


def try_load_dataset(buffer: Union['BytesIO', 'BufferedIOBase'], sheet_name: str = 0, separator: str = ',') -> Union[
    'DataFrame', 'OrderedDict']:
    """
    Load data into a pandas DataFrame from BytesIO object.

    Parameters
    ----------
    buffer: Union['BytesIO', 'BufferedIOBase'], required
        Buffer with bytes data.

    sheet_name: str, optional
        Name of the xlsx sheet to read.

    separator: str, optional
        csv separator

    Returns
    -------
    DataFrame or OrderedDict
    """
    from pandas import read_csv, read_excel

    try:
        buffer.seek(0)
        data = read_csv(buffer, sep=separator, encoding='utf-8')

    except Exception as e1:
        try:
            try_import_xlrd()
            buffer.seek(0)
            data = read_excel(buffer, sheet_name=sheet_name)

        except Exception as e2:
            raise DataFormatNotSupported(None, reason=f"Error1: {e1} Error2: {e2}")

    return data


def check_dependencies_versions(lib_name: str = None, error: bool = False, msg: str = '') -> None:
    """Check scikit, xgboost and lightbm installed versions and inform the user about needed ones.

    Parameters
    ----------
    lib_name: str, optional
        Library name to check

    error: bool, optional
        If True, raise an error when some library is missing or is incompatible.

    msg: str, optional
        Error message.
    """

    scikit_version = '0.20.3'
    numpy_version = '1.18.2'
    xgboost_version = '0.90'
    lightgbm_version = '2.2.3'

    scikit_message = f'To use AutoAI, you need to have scikit-learn {scikit_version} installed.'
    numpy_message = f'To use AutoAI, you need to have numpy {numpy_version} installed.'
    xgboost_message = f'To use AutoAI with xgboost estimators, you need to have xgboost {xgboost_version} installed.'
    lightgbm_message = f'To use AutoAI with lightgbm estimators, you need to have lightgbm {lightgbm_version} installed.'

    def print_or_warn(library: str) -> None:
        if library == 'scikit':
            message = scikit_message

        elif library == 'xgboost':
            message = xgboost_message

        elif library == 'numpy':
            message = numpy_message

        else:
            message = lightgbm_message

        if error:
            raise LibraryNotCompatible(reason=f'{msg} {message}')

        if is_ipython():
            print(f'Warning: {message}')

        else:
            warn(message=message)

    # note: scikit version check
    try:
        if lib_name == 'scikit' or lib_name is None:
            import sklearn
            if sklearn.__version__ != scikit_version:
                print_or_warn(library='scikit')

    except (ImportError, AttributeError, ModuleNotFoundError):
        print_or_warn(library='scikit')
    # --- end note

    # note: xgboost version check
    try:
        if lib_name == 'xgboost' or lib_name is None:
            import xgboost
            if xgboost.__version__ != xgboost_version:
                print_or_warn(library='xgboost')

    except (ImportError, AttributeError, ModuleNotFoundError):
        print_or_warn(library='xgboost')
    # --- end note

    # note: lightgbm version check
    try:
        if lib_name == 'lightgbm' or lib_name is None:
            import lightgbm
            if lightgbm.__version__ != lightgbm_version:
                print_or_warn(library='lightgbm')

    except (ImportError, AttributeError, ModuleNotFoundError):
        print_or_warn(library='lightgbm')
    # --- end note

    # note: numpy version check
    try:
        if lib_name == 'numpy' or lib_name is None:
            import numpy
            from packaging import version
            if version.parse(numpy.__version__) < version.parse(numpy_version):
                print_or_warn(library='numpy')

    except (ImportError, AttributeError, ModuleNotFoundError):
        print_or_warn(library='numpy')
    # --- end note


def prepare_cos_client(
        training_data_references: List['DataConnection'] = None,
        training_result_reference: 'DataConnection' = None) -> Tuple[Union[List[Tuple['DataConnection', 'resource']]],
                                                                     Union[Tuple['DataConnection', 'resource'], None]]:
    """
    Create COS clients for training data and results.

    Parameters
    ----------
    training_data_references: List['DataConnection'], optional

    training_result_reference: 'DataConnection', optional

    Returns
    -------
    list of COS clients for training data , client for results
    """
    from watson_machine_learning_client.helpers import S3Connection
    from ibm_boto3 import resource
    from ibm_botocore.client import Config

    def differentiate_between_credentials(connection: 'S3Connection') -> 'resource':
        # note: we do not know which version of COS credentials user used during training
        if hasattr(connection, 'auth_endpoint') and hasattr(connection, 'api_key'):
            cos_client = resource(
                service_name='s3',
                ibm_api_key_id=connection.api_key,
                ibm_auth_endpoint=connection.auth_endpoint,
                config=Config(signature_version="oauth"),
                endpoint_url=connection.endpoint_url
            )

        else:
            cos_client = resource(
                service_name='s3',
                endpoint_url=connection.endpoint_url,
                aws_access_key_id=connection.access_key_id,
                aws_secret_access_key=connection.secret_access_key
            )
        # --- end note

        return cos_client

    cos_client_results = None
    data_cos_clients = []

    if training_result_reference is not None:
        if isinstance(training_result_reference.connection, S3Connection):
            cos_client_results = (training_result_reference,
                                  differentiate_between_credentials(connection=training_result_reference.connection))

    if training_data_references is not None:
        for reference in training_data_references:
            if isinstance(reference.connection, S3Connection):
                data_cos_clients.append((reference,
                                         differentiate_between_credentials(connection=reference.connection)))

    return data_cos_clients, cos_client_results


def create_summary(details: dict, scoring: str) -> 'DataFrame':
    """
    Creates summary in a form of a pandas.DataFrame of computed pipelines (should be used in remote and local scenario
    with COS).

    Parameters
    ----------
    details: dict, required
        Dictionary with all training data

    scoring: str, required
        scoring method

    Returns
    -------
    pandas.DataFrame with pipelines summary
    """
    from watson_machine_learning_client.utils.autoai.enums import MetricsToDirections, Directions
    from pandas import DataFrame

    columns = (['Pipeline Name', 'Number of enhancements', 'Estimator'] +
               [metric_name for metric_name in
                details['entity']['status'].get('metrics', [{}])[0].get('ml_metrics', {}).keys()])
    values = []

    for pipeline in details['entity']['status'].get('metrics', []):
        if pipeline['context']['phase'] == 'global_output':
            number_of_enhancements = len(pipeline['context']['intermediate_model']['composition_steps']) - 5

            # note: workaround when some pipelines have less or more metrics computed
            metrics = columns[3:]
            pipeline_metrics = [None] * len(metrics)
            for metric, value in pipeline['ml_metrics'].items():
                for i, metric_name in enumerate(metrics):
                    if metric_name == metric:
                        pipeline_metrics[i] = value
            # --- end note

            values.append(
                ([f"Pipeline_{pipeline['context']['intermediate_model']['name'].split('P')[-1]}"] +
                 [number_of_enhancements] +
                 [pipeline['context']['intermediate_model']['pipeline_nodes'][-1]] +
                 pipeline_metrics
                 ))

    pipelines = DataFrame(data=values, columns=columns)
    pipelines.drop_duplicates(subset="Pipeline Name", keep='first', inplace=True)
    pipelines.set_index('Pipeline Name', inplace=True)

    try:
        if (MetricsToDirections[scoring.upper()].value ==
                Directions.ASCENDING):
            return pipelines.sort_values(
                by=[f"training_{scoring}"], ascending=False).rename(
                {
                    f"training_{scoring}":
                        f"training_{scoring}_(optimized)"
                }, axis='columns')

        else:
            return pipelines.sort_values(by=[f"training_{scoring}"]).rename(
                {
                    f"training_{scoring}":
                        f"training_{scoring}_(optimized)"
                }, axis='columns')

    # note: sometimes backend will not return 'training_' prefix to the metric
    except KeyError:
        return pipelines


def get_node_and_runtime_index(node_name: str, optimizer_config: dict) -> Tuple[int, int]:
    """Find node index from node name in experiment parameters."""
    node_number = None
    runtime_number = None

    for i, node in enumerate(optimizer_config['entity']['document']['pipelines'][0]['nodes']):
        if node_name == 'kb' and (node.get('id') == 'kb' or node.get('id') == 'automl'):
            node_number = i
            break

        elif node_name == 'obm' and node.get('id') == 'obm':
            node_number = i
            break

    for i, runtime in enumerate(optimizer_config['entity']['document']['runtimes']):
        if node_name == 'kb' and (runtime.get('id') == 'kb' or runtime.get('id') == 'automl' or
                                  runtime.get('id') == 'autoai'):
            runtime_number = i
            break

        elif node_name == 'obm' and runtime.get('id') == 'obm':
            runtime_number = i
            break

    return node_number, runtime_number


def download_experiment_details_from_file(result_client_and_connection: Tuple['DataConnection', 'resource']) -> dict:
    """Try to download training details from user COS."""

    try:
        file = result_client_and_connection[1].Object(
            result_client_and_connection[0].location.bucket,
            result_client_and_connection[0].location._training_status).get()

        details = json.loads(file['Body'].read())

    except Exception as e:
        raise CannotDownloadTrainingDetails('', reason=f"Error: {e}")

    return details


def download_wml_pipeline_details_from_file(result_client_and_connection: Tuple['DataConnection', 'resource']) -> dict:
    """Try to download wml pipeline details from user COS."""

    try:
        path = result_client_and_connection[0].location._model_location.split('model.pickle')[0]
        path = f"{path}pipeline-model.json"

        file = result_client_and_connection[1].Object(
            result_client_and_connection[0].location.bucket,
            path).get()

        details = json.loads(file['Body'].read())

    except Exception as e:
        raise CannotDownloadWMLPipelineDetails('', reason=f"Error: {e}")

    return details


def prepare_model_location_path(model_path: str) -> str:
    """
    To be able to get best pipeline after computation we need to change model_location string to global_output.
    """

    if "data/automl/" in model_path:
        path = model_path.split('data/automl/')[0]
        path = f"{path}data/automl/global_output/"

    else:
        path = model_path.split('data/kb/')[0]
        path = f"{path}data/kb/global_output/"

    return path


def check_graphviz_binaries(f):
    @wraps(f)
    def _f(*method_args, **method_kwargs):
        from graphviz.backend import ExecutableNotFound
        try:
            output = f(*method_args, **method_kwargs)

        except ExecutableNotFound as e:
            raise VisualizationFailed(
                reason=f"Cannot perform visualization with graphviz. Please make sure that you have Graphviz binaries "
                       f"installed in your system. Please follow this guide: https://www.graphviz.org/download/")

        return output

    return _f
