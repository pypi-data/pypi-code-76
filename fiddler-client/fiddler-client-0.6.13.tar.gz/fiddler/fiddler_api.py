# TODO: Add License
import configparser
import contextlib
import copy
import json
import logging
import os.path
import pickle
import random
import shutil
import tempfile
import textwrap
import time
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Union

import pandas as pd
import requests
import yaml

from .core_objects import (
    ArtifactStatus,
    AttributionExplanation,
    Column,
    DatasetInfo,
    DataType,
    ModelInfo,
    MulticlassAttributionExplanation,
)
from .model_info_validator import ModelInfoValidator
from .utils import _df_to_dict, _try_series_retype, df_from_json_rows

LOG = logging.getLogger()

SUCCESS_STATUS = 'SUCCESS'
FAILURE_STATUS = 'FAILURE'
FIDDLER_ARGS_KEY = '__fiddler_args__'
STREAMING_HEADER_KEY = 'X-Fiddler-Results-Format'
AUTH_HEADER_KEY = 'Authorization'
ROUTING_HEADER_KEY = 'x-fdlr-fwd'
ADMIN_SERVICE_PORT = 4100

# A PredictionEventBundle represents a batch of inferences and their input
# features. All of these share schema, latency, and success status. A bundle
# can consist just one event as well.
PredictionEventBundle = namedtuple(
    'PredictionEventBundle',
    [
        'prediction_status',  # typeof: int # 0 for success, failure otherwise
        'prediction_latency',  # typeof: float # Latency in seconds.
        'input_feature_bundle',  # list of feature vectors.
        'prediction_bundle',  # list of prediction vectors.
        # TODO: Support sending schema as well.
    ],
)


_protocol_version = 1


class FiddlerApi:
    """Broker of all connections to the Fiddler API.
    Conventions:
        - Exceptions are raised for FAILURE reponses from the backend.
        - Methods beginning with `list` fetch lists of ids (e.g. all model ids
            for a project) and do not alter any data or state on the backend.
        - Methods beginning with `get` return a more complex object but also
            do not alter data or state on the backend.
        - Methods beginning with `run` invoke model-related execution and
            return the result of that computation. These do not alter state,
            but they can put a heavy load on the computational resources of
            the Fiddler engine, so they should be paralellized with care.
        - Methods beginning with `delete` permanently, irrevocably, and
            globally destroy objects in the backend. Think "rm -rf"
        - Methods beginning with `upload` convert and transmit supported local
            objects to Fiddler-friendly formats loaded into the Fiddler engine.
            Attempting to upload an object with an identifier that is already
            in use will result in an exception being raised, rather than the
            existing object being overwritten. To update an object in the
            Fiddler engine, please call both the `delete` and `upload` methods
            pertaining to the object in question.

    :param url: The base URL of the API to connect to. Usually either
        https://api.fiddler.ai (cloud) or http://localhost:4100 (onebox)
    :param org_id: The name of your organization in the Fiddler platform
    :param auth_token: Token used to authenticate. Your token can be
        created, found, and changed at <FIDDLER URL>/settings/credentials.
    :param proxies: optionally, a dict of proxy URLs. e.g.,
                    proxies = {'http' : 'http://proxy.example.com:1234',
                               'https': 'https://proxy.example.com:5678'}
    :param verbose: if True, api calls will be logged verbosely
    """

    def __init__(
        self, url=None, org_id=None, auth_token=None, proxies=None, verbose=False
    ):
        if Path('fiddler.ini').is_file():
            config = configparser.ConfigParser()
            config.read('fiddler.ini')
            info = config['FIDDLER']
            if not url:
                url = info['url']
            if not org_id:
                org_id = info['org_id']
            if not auth_token:
                auth_token = info['auth_token']

        if url[-1] == '/':
            raise ValueError('url should not end in "/"')

        # use session to preserve session data
        self.session = requests.Session()
        if proxies:
            assert isinstance(proxies, dict)
            self.session.proxies = proxies
        self.url = url
        self.org_id = org_id
        self.auth_header = {AUTH_HEADER_KEY: f'Bearer {auth_token}'}
        self.streaming_header = {STREAMING_HEADER_KEY: 'application/jsonlines'}
        self.verbose = verbose
        self.check_connection()

    def check_connection(self):
        try:
            path = ['get_supported_features', self.org_id]
            _ = self._call(path, is_get_request=True)
            return 'OK'
        except requests.exceptions.ConnectionError:
            LOG.warning(
                f'CONNECTION CHECK FAILED: Unable to connect with to '
                f'{self.url}. Are you sure you have the right URL?'
            )
        except RuntimeError as error:
            LOG.warning(
                f'API CHECK FAILED: Able to connect to {self.url}, '
                f'but request failed with message "{str(error)}"'
            )
        except Exception as e:
            LOG.warning(
                f'API CHECK FAILED: Able to connect to {self.url}, '
                f'but request failed with message "{str(e)}"'
            )

    @staticmethod
    def _get_routing_header(path_base: str) -> Dict[str, str]:
        """Returns the proper header so that a request is routed to the correct
        service."""
        executor_service_bases = (
            'dataset_predictions',
            'execute',
            'executor',
            'explain',
            'explain_by_row_id',
            'fairness',
            'feature_importance',
            'generate',
            'new_project',
            'precache_globals',
            'v1/point_explanation',
            'v1/model_explanation',
            'v1/execution',
        )
        if path_base in executor_service_bases:
            return {ROUTING_HEADER_KEY: 'executor_service'}
        else:
            return {ROUTING_HEADER_KEY: 'data_service'}

    def _call_executor_service(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
    ):
        no_auth_onebox = False
        try:
            if self.url == 'http://localhost:6100':
                no_auth_onebox = True
                self.url = 'http://localhost:5100'

            return self._call(path, json_payload, files, is_get_request, stream)
        finally:
            if no_auth_onebox:
                self.url = 'http://localhost:6100'

    def _call(
        self,
        path: List[str],
        json_payload: Any = None,
        files: Optional[List[Path]] = None,
        is_get_request: bool = False,
        stream: bool = False,
    ):
        """Issues a request to the API and returns the result,
        logigng and handling errors appropriately.


        Raises a RuntimeError if the response is a failure or cannot be parsed.
        Does not handle any ConnectionError exceptions thrown by the `requests`
        library.
        """

        # set up a context manager to open files
        with contextlib.ExitStack() as context_stack:
            endpoint = '/'.join([self.url] + path)
            request_type = 'GET' if is_get_request else 'POST'
            if json_payload:
                request_excerpt = textwrap.indent(
                    json.dumps(json_payload, indent=2)[:2048], '  '
                )
            else:
                request_excerpt = None
            if self.verbose:
                LOG.info(
                    f'running api call as {request_type} request\n'
                    f'to {endpoint}\n'
                    f'with headers {self.auth_header}\n'
                    f'with payload {request_excerpt}'
                )
            if is_get_request:
                req = requests.Request('GET', endpoint)
            else:
                # if uploading files, we use a multipart/form-data request and
                # dump the json_payload to be the special "fiddler args"
                # as a json object in the form
                if files is not None:
                    # open all the files into the context manager stack
                    opened_files = {
                        fpath.name: context_stack.enter_context(fpath.open('rb'))
                        for fpath in files
                    }
                    #
                    # NOTE: there are a lot LOT of ways to do this wrong with
                    # `requests`
                    #
                    # Take a look here (and at the thread linked) for more info:
                    # https://stackoverflow.com/a/35946962
                    #
                    # And here: https://stackoverflow.com/a/12385661
                    #
                    form_data = {
                        **{
                            FIDDLER_ARGS_KEY: (
                                None,  # filename
                                json.dumps(json_payload),  # data
                                'application/json',  # content_type
                            )
                        },
                        **{
                            fpath.name: (
                                fpath.name,  # filename
                                opened_files[fpath.name],  # data
                                'application/octet-stream',  # content_type
                            )
                            for fpath in files
                        },
                    }
                    req = requests.Request('POST', endpoint, files=form_data)
                else:
                    req = requests.Request('POST', endpoint, json=json_payload)

            # add necessary headers
            # using prepare_request from session to keep session data
            req = self.session.prepare_request(req)
            added_headers = dict()
            added_headers.update(self.auth_header)
            added_headers.update(self._get_routing_header(path[0]))
            if stream:
                added_headers.update(self.streaming_header)
            req.headers = {**added_headers, **req.headers}

            # log the raw request
            raw_request_info = (
                f'Request:\n'
                f'  url: {req.url}\n'
                f'  method: {req.method}\n'
                f'  headers: {req.headers}'
            )
            LOG.debug(raw_request_info)
            # if self.verbose:
            #     LOG.info(raw_request_info)

            # send the request using session to carry auth info from login
            res = self.session.send(req, stream=stream)

            if self.verbose:
                LOG.info(f'response: {res.text}')

        # catch auth failure
        if res.status_code == 401:
            error_msg = (
                f'API call to {endpoint} failed with status 401: '
                f'Authorization Required. '
                f'Do you have the right org_id and auth_token?'
            )
            LOG.debug(error_msg)
            raise RuntimeError(error_msg)
        # catch any failure
        elif res.status_code != 200:
            error_msg = (
                f'API call to {endpoint} failed with status {res.status_code}:'
                f' The full response message was {res.text}'
            )
            LOG.debug(error_msg)
            raise RuntimeError(error_msg)

        if stream:
            return self._process_streaming_call_result(res, endpoint, raw_request_info)
        return self._process_non_streaming_call_result(res, endpoint, raw_request_info)

    @staticmethod
    def _raise_on_status_error(
        response: requests.Response, endpoint: str, raw_request_info: str
    ):
        """Raises exception on HTTP errors similar to
        `response.raise_for_status()`."""
        # catch non-auth failures
        try:
            response.raise_for_status()
        except Exception:
            response_payload = response.json()
            try:
                failure_message = response_payload.get('message', 'Unknown')
                failure_stacktrace = response_payload.get('stacktrace')
                error_msg = (
                    f'API call failed.\n'
                    f'Error message: {failure_message}\n'
                    f'Endpoint: {endpoint}'
                )
                if failure_stacktrace:
                    error_msg += f'\nStacktrace: {failure_stacktrace}'

            except KeyError:
                error_msg = (
                    f'API call to {endpoint} failed.\n'
                    f'Request response: {response.text}'
                )
            LOG.debug(f'{error_msg}\n{raw_request_info}')
            raise RuntimeError(error_msg)

    def _process_non_streaming_call_result(
        self, response: requests.Response, endpoint: str, raw_request_info: str
    ):

        FiddlerApi._raise_on_status_error(response, endpoint, raw_request_info)

        # catch non-JSON response (this is rare, the backend should generally
        # return JSON in all cases)
        try:
            response_payload = response.json()
        except json.JSONDecodeError:
            print(response.status_code)
            error_msg = (
                f'API call to {endpoint} failed.\n' f'Request response: {response.text}'
            )
            LOG.debug(f'{error_msg}\n{raw_request_info}')
            raise RuntimeError(error_msg)

        assert response_payload['status'] == SUCCESS_STATUS
        result = response_payload.get('result')

        # log the API call on success (excerpt response on success)
        response_excerpt = textwrap.indent(
            json.dumps(response_payload, indent=2)[:2048], '  '
        )
        log_msg = (
            f'API call to {endpoint} succeeded.\n'
            f'Request response: {response_excerpt}\n'
            f'{raw_request_info}\n'
        )
        if self.verbose:
            LOG.info(log_msg)
        return result

    @staticmethod
    def _process_streaming_call_result(
        response: requests.Response, endpoint: str, raw_request_info: str
    ):
        """Processes response in jsonlines format. `json_streaming_endpoint`
        returns jsonlines with one json object per line when
        'X-Fiddler-Response-Format' header is set to 'jsonlines'.
        :returns: a generator for results."""

        FiddlerApi._raise_on_status_error(response, endpoint, raw_request_info)

        got_eos = False  # got proper end_of_stream.

        if response.headers.get('Content-Type') != 'application/x-ndjson':
            RuntimeError('Streaming response Content-Type is not "x-ndjson"')

        # Read one line at a time. `chunk_size` None ensures that a line
        # is returned as soon as it is read, rather waiting for any minimum
        # size (default is 512 bytes).
        for line in response.iter_lines(chunk_size=None):
            if line:
                row_json = json.loads(line)
                if 'result' in row_json:
                    yield row_json['result']
                elif row_json.get('status') == SUCCESS_STATUS:
                    got_eos = True
                    break
        if not got_eos:
            raise RuntimeError(
                'Truncated response for streaming request. '
                'Failed to receive successful status.'
            )

    def list_datasets(self) -> List[str]:
        """List the ids of all datasets in the organization.

        :returns: List of strings containing the ids of each dataset.
        """
        try:
            path = ['v1', 'dataset', 'get', self.org_id]
            payload = {}
            res = self._call(path, json_payload=payload)
        except Exception:
            path = ['list_datasets', self.org_id]
            res = self._call(path, is_get_request=True)

        return res

    def list_projects(self) -> List[str]:
        """List the ids of all projects in the organization.

        :returns: List of strings containing the ids of each project.
        """
        path = ['list_projects', self.org_id]
        res = self._call(path, is_get_request=True)
        return [proj['id'] for proj in res['projects']]

    def list_models(self, project_id: str, cached=True) -> List[str]:
        """List the names of all models in a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.
        :param cached: Receive a fresh, uncached list. Used for testing.

        :returns: List of strings containing the ids of each model in the
            specified project.
        """
        try:
            path = ['v1', 'model', 'get', self.org_id]
            payload = {'project_id': project_id, 'cached': cached}
            res = self._call(path, json_payload=payload)
        except Exception:
            path = ['list_models', self.org_id, project_id]
            res = self._call(path, is_get_request=True)

        return res

    def get_dataset_info(self, dataset_id: str) -> DatasetInfo:
        """Get DatasetInfo for a dataset.

        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: A fiddler.DatasetInfo object describing the dataset.
        """
        try:
            path = ['v1', 'dataset', 'get', self.org_id]
            payload = {'dataset_id': dataset_id}
            res = self._call(path, json_payload=payload)
        except Exception:
            path = ['dataset_schema', self.org_id, dataset_id]
            res = self._call(path, is_get_request=True)

        info = DatasetInfo.from_dict(res)
        info.dataset_id = dataset_id
        return info

    def get_model_info(self, project_id: str, model_id: str) -> ModelInfo:
        """Get ModelInfo for a model in a certain project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: A fiddler.ModelInfo object describing the model.
        """
        try:
            path = ['v1', 'model', 'get', self.org_id]
            payload = {'project_id': project_id, 'model_id': model_id}
            res = self._call(path, json_payload=payload)
        except Exception:
            path = ['model_info', self.org_id, project_id, model_id]
            res = self._call(path, is_get_request=True)
        return ModelInfo.from_dict(res)

    def _query_dataset(
        self,
        dataset_id: str,
        fields: List[str],
        max_rows: int,
        split: Optional[str] = None,
        stream=True,
        sampling=False,
        sampling_seed=0.0,
    ):
        payload = dict(
            streaming=True,
            dataset_id=dataset_id,
            fields=fields,
            limit=max_rows,
            sampling=sampling,
        )

        if sampling:
            payload['sampling_seed'] = sampling_seed
        if split is not None:
            payload['source'] = f'{split}.csv'
        # try:
        #     path = ['v1', 'dataset', 'get', self.org_id]
        #     res = self._call(path, json_payload=payload, stream=stream)
        # except Exception:
        payload.pop('streaming')
        payload.pop('dataset_id')

        path = ['dataset_query', self.org_id, dataset_id]
        res = self._call(path, json_payload=payload, stream=stream)

        return res

    def get_dataset(
        self,
        dataset_id: str,
        max_rows: int = 1_000,
        splits: Optional[List[str]] = None,
        sampling=False,
        dataset_info: Optional[DatasetInfo] = None,
        include_fiddler_id=False,
        stream=True,
    ) -> Dict[str, pd.DataFrame]:
        """Fetches data from a dataset on Fiddler.

        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.
        :param max_rows: Up to this many rows will be fetched from eash split
            of the dataset.
        :param splits: If specified, data will only be fetched for these
            splits. Otherwise, all splits will be fetched.
        :param sampling: If True, data will be sampled up to max_rows. If
            False, rows will be returned in order up to max_rows. The seed
            will be fixed for sampling.∂
        :param dataset_info: If provided, the API will skip looking up the
            DatasetInfo (a necessary precursor to requesting data).
        :param include_fiddler_id: Return the Fiddler engine internal id
            for each row. Useful only for debugging.
        :param stream: Streaming is generally faster, but you can disable
            this if you are having errors. Does not affect the results
            returned.

        :returns: A dictionary of str -> DataFrame that maps the name of
            dataset splits to the data in those splits. If len(splits) == 1,
            returns just that split as a dataframe, rather than a dataframe.
        """
        if dataset_info is None:
            dataset_info = self.get_dataset_info(dataset_id)
        else:
            dataset_info = copy.deepcopy(dataset_info)

        def get_df_from_split(split, fiddler_id=include_fiddler_id):
            column_names = dataset_info.get_column_names()
            if fiddler_id:
                column_names.insert(0, '__fiddler_id')
            dataset_rows = self._query_dataset(
                dataset_id,
                fields=column_names,
                max_rows=max_rows,
                split=split,
                sampling=sampling,
                stream=stream,
            )
            return df_from_json_rows(
                dataset_rows, dataset_info, include_fiddler_id=include_fiddler_id
            )

        if splits is None:
            use_splits = [
                os.path.splitext(filename)[0] for filename in dataset_info.files
            ]
        else:
            use_splits = splits
        res = {split: get_df_from_split(split) for split in use_splits}
        if splits is not None and len(splits) == 1:
            # unwrap single-slice results
            res = next(iter(res.values()))
        return res

    def get_slice(
        self,
        sql_query: str,
        project: Optional[str],
        columns_override: Optional[List[str]] = None,
        stream=True,
    ) -> pd.DataFrame:
        """Fetches data from Fiddler via a *slice query* (SQL query).

        :param sql_query: A special SQL query that begins with the keyword
            "SLICE"
        :param project: A project is required when the the slice query is
            for a model. The caller might not know if the query is a
            model slice. Is it safe to provide it whenever it is available.
        :param columns_override: A list of columns to return even if they are
            not specified in the slice.
        :param stream: Streaming is generally faster, but you can disable
            this if you are having errors. Does not affect the results
            returned.

        :returns: A table containing the sliced data (as a Pandas DataFrame)
        """
        payload = dict(streaming=True, sql=sql_query, project=project)
        if columns_override is not None:
            payload['slice_columns_override'] = columns_override

        try:
            path = ['v1', 'dataset', 'get', self.org_id]
            res = self._call(path, json_payload=payload, stream=stream)
        except Exception:
            payload.pop('streaming')

            path = ['slice_query', self.org_id]
            res = self._call(path, json_payload=payload, stream=stream)

        if stream:
            try:
                slice_info = next(res)
            except StopIteration:
                raise RuntimeError('Empty results for slice!')
        else:
            slice_info = res.pop(0)
        if not slice_info['is_slice']:
            raise RuntimeError(
                'Query does not return a valid slice. ' 'Query: ' + sql_query
            )
        column_names = slice_info['columns']
        dtype_strings = slice_info['dtypes']
        df = pd.DataFrame(res, columns=column_names)
        for column_name, dtype in zip(column_names, dtype_strings):
            df[column_name] = _try_series_retype(df[column_name], dtype)
        return df

    def delete_dataset(self, dataset_id: str):
        """Permanently delete a dataset.

        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        try:
            path = ['v1', 'dataset', 'delete', self.org_id]
            payload = {'dataset_id': dataset_id}
            result = self._call(path, json_payload=payload)
        except Exception:
            path = ['dataset_delete', self.org_id, dataset_id]
            result = self._call(path)

        return result

    def delete_model(
        self, project_id: str, model_id: str, delete_prod=False, delete_pred=True
    ):
        """Permanently delete a model.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param delete_prod: Boolean value to delete the production table.
            By default this table is not dropped.
        :param delete_pred: Boolean value to delete the prediction table.
            By default this table is dropped.

        :returns: Server response for deletion action.
        """
        payload = {
            'project_id': project_id,
            'model_id': model_id,
            'delete_prod': delete_prod,
            'delete_pred': delete_pred,
        }

        path = ['delete_model', self.org_id, project_id, model_id]
        try:
            result = self._call(path, json_payload=payload)
        except Exception:
            # retry on error
            result = self._call(path, json_payload=payload)

        self.delete_model_artifacts(project_id, model_id)

        # wait for ES to come back healthy
        for i in range(3):
            try:
                self._call_executor_service(
                    ['deploy', self.org_id], is_get_request=True
                )
                break
            except Exception:
                pass

        return result

    def delete_model_artifacts(self, project_id: str, model_id: str):
        """Permanently delete a model artifacts.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: Server response for deletion action.
        """
        # delete from executor service cache
        path = ['delete_model_artifacts', self.org_id, project_id, model_id]
        result = self._call_executor_service(path)

        return result

    def delete_project(self, project_id: str):
        """Permanently delete a project.

        :param project_id: The unique identifier of the project on the Fiddler
            engine.

        :returns: Server response for deletion action.
        """
        try:
            path = ['v1', 'project', 'delete', self.org_id]
            payload = {'project_id': project_id}
            result = self._call(path, json_payload=payload)
        except Exception:
            path = ['delete_project', self.org_id, project_id]
            result = self._call(path)

        return result

    def _upload_dataset_csvs(
        self,
        dataset_id: str,
        csv_file_paths: List[Path],
        split_test: Optional[bool] = None,
        dataset_info: Optional[DatasetInfo] = None,
        do_import: Optional[bool] = None,
    ):
        """Uploads a CSV file to the Fiddler platform."""
        payload = dict(dataset_name=dataset_id)
        if split_test is not None:
            payload['split_test'] = split_test
        if dataset_info is not None:
            payload['dataset_info'] = dict(dataset=dataset_info.to_dict())
        if do_import is not None:
            payload['do_import'] = do_import

        try:
            path = ['v1', 'dataset', 'upload', self.org_id]
            result = self._call(path, json_payload=payload, files=csv_file_paths)
        except Exception:
            path = ['dataset_upload', self.org_id]
            result = self._call(path, json_payload=payload, files=csv_file_paths)
        return result

    def _db_import(self, dataset_id):
        try:
            path = ['v1', 'dataset', 'import', self.org_id]
            payload = dict(dataset_id=dataset_id)
            res = self._call(path, json_payload=payload)
        except Exception:
            path = ['import_dataset', self.org_id, dataset_id]
            res = self._call(path, is_get_request=True)

        return res

    def _import_model_predictions(
        self,
        project_id: str,
        dataset_id: str,
        model_id: str,
        columns: Sequence[Dict],
        csv_file_paths: List[Path],
    ):
        """Uploads model predictions to Fiddler platform."""
        payload = dict(dataset=dataset_id)
        payload['model'] = model_id
        payload['columns'] = columns

        path = ['import_model_predictions', self.org_id, project_id]
        result = self._call(path, json_payload=payload, files=csv_file_paths)
        return result

    def upload_dataset(
        self,
        dataset: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        dataset_id: str,
        info: Optional[DatasetInfo] = None,
        split_test=False,
    ):
        """Uploads a dataset to the Fiddler engine.

        :param dataset: A DataFrame or dictionary mapping name -> DataFrame
            containing tabular data to be uploaded to the Fiddler engine.
        :param dataset_id: The unique identifier of the dataset on the Fiddler
            engine. Must be a short string without whitespace.
        :param info: A DatasetInfo object specifying all the details of the
            dataset. If not provided, a DatasetInfo will be inferred from the
            dataset and a warning raised.
        :param split_test: If you would like Fiddler to automatically split a
            single-dataframe dataset into a training set and a test set, set
            `split_test=True`. This option has no effect for multi-dataframe
            datasets.

        :returns: The server response for the upload.
        """
        assert (
            ' ' not in dataset_id
        ), 'The dataset identifier should not contain whitespace'

        # get a dictionary of str -> pd.DataFrame for all data to upload
        if not isinstance(dataset, dict):
            dataset = dict(data=dataset)

        # infer a dataset_info
        inferred_info = DatasetInfo.from_dataframe(
            dataset.values(), display_name=dataset_id
        )

        if info:
            # Since we started populating stats recently, some older yamls
            # dont have it. Or the user might just supply us the basic
            # schema without stats.
            # If the user provided the schema/yaml file, lets make sure
            # that we add stats if they are not already there.
            info = DatasetInfo.update_stats_for_existing_schema(dataset, info)
            updated_infos = []
            for item in dataset.values():
                update_info = DatasetInfo.check_and_update_column_info(info, item)
                updated_infos.append(update_info)
            info = DatasetInfo.as_combination(
                updated_infos, display_name=info.display_name
            )
        # validate `info` if passed
        if info is not None:
            inferred_columns = inferred_info.get_column_names()
            passed_columns = info.get_column_names()
            if inferred_columns != passed_columns:
                raise RuntimeError(
                    f'Provided data schema has columns {passed_columns}, '
                    f'which does not match the data schema {inferred_columns}'
                )
        # use inferred info with a warning if not `info` is passed
        else:
            LOG.warning(
                f'Heads up! We are inferring the details of your dataset from '
                f'the dataframe(s) provided. Please take a second to check '
                f'our work.'
                f'\n\nIf the following DatasetInfo is an incorrect '
                f'representation of your data, you can construct a '
                f'DatasetInfo with the DatasetInfo.from_dataframe() method '
                f'and modify that object to reflect the correct details of '
                f'your dataset.'
                f'\n\nAfter constructing a corrected DatasetInfo, please '
                f're-upload your dataset with that DatasetInfo object '
                f'explicitly passed via the `info` parameter of '
                f'FiddlerApi.upload_dataset().'
                f'\n\nYou may need to delete the initially uploaded version'
                f"via FiddlerApi.delete_dataset('{dataset_id}')."
                f'\n\nInferred DatasetInfo to check:'
                f'\n{textwrap.indent(repr(inferred_info), "  ")}'
            )
            info = inferred_info

        # determine whether or not the index of this dataset is a meaningful
        # column that should be written into CSV files
        include_index = next(iter(dataset.values())).index.name is not None

        # dump CSVs to named temp file
        with tempfile.TemporaryDirectory() as tmp:
            csv_paths = list()
            for name, df in dataset.items():
                filename = f'{name}.csv'
                path = Path(tmp) / filename
                csv_paths.append(path)
                LOG.info(f'[{name}] dataset upload: writing csv to {path}')
                df.to_csv(path, index=include_index)

            # add files to the DatasetInfo on the fly
            new_schema = copy.deepcopy(info)
            new_schema.files = [path.name for path in csv_paths]

            # upload the CSV
            LOG.info(f'[{dataset_id}] dataset upload: upload and import csv')
            res = self._upload_dataset_csvs(
                dataset_id,
                csv_paths,
                split_test=split_test,
                dataset_info=new_schema,
                do_import=True,
            )
            return res

    def upload_dataset_from_dir(self, dataset_id: str, dataset_dir: Path):
        logging.info(f'uploading dataset from dir: {dataset_dir}')
        if not dataset_dir.is_dir():
            raise ValueError(f'{dataset_dir} is not a directory')
        dataset_yaml = dataset_dir / f'{dataset_id}.yaml'
        if not dataset_yaml.is_file():
            raise ValueError(f'YAML file not found: {dataset_yaml}')
        with dataset_yaml.open() as f:
            dataset_info = DatasetInfo.from_dict(yaml.safe_load(f))
            files = dataset_dir.glob('*.csv')
            csv_files = [x for x in files if x.is_file()]
            logging.info(f'Found CSV file {csv_files}')
            result = self._upload_dataset_csvs(
                dataset_id, csv_files, False, dataset_info, True
            )
            LOG.info(f'Dataset uploaded {result}')

    def run_model(
        self, project_id: str, model_id: str, df: pd.DataFrame, log_events=False
    ) -> pd.DataFrame:
        """Executes a model in the Fiddler engine on a DataFrame.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param df: A dataframe contining model inputs as rows.
        :param log_events: Variable determining if the the predictions
            generated should be logged as production traffic

        :returns: A pandas DataFrame containing the outputs of the model.
        """
        data_array = _df_to_dict(df)
        payload = dict(
            project_id=project_id,
            model_id=model_id,
            data=data_array,
            logging=log_events,
        )

        try:
            path = ['v1/execution', 'run', self.org_id]
            res = self._call_executor_service(path, json_payload=payload)
        except Exception:
            payload.pop('project_id')
            payload.pop('model_id')

            path = ['execute', self.org_id, project_id, model_id]
            res = self._call_executor_service(path, json_payload=payload)
        return pd.DataFrame(res)

    def run_explanation(
        self,
        project_id: str,
        model_id: str,
        df: pd.DataFrame,
        explanations: Union[str, Iterable[str]] = 'shap',
        dataset_id: Optional[str] = None,
        return_raw_response=False,
    ) -> Union[
        AttributionExplanation,
        MulticlassAttributionExplanation,
        List[AttributionExplanation],
        List[MulticlassAttributionExplanation],
    ]:
        """Executes a model in the Fiddler engine on a DataFrame.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param df: A dataframe containing model inputs as rows. Only the first
            row will be explained.
        :param explanations: A single string or list of strings specifying
            which explanation algorithms to run.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine. Required for most tabular explanations, but
            optional for most text explanations.

        :returns: A single AttributionExplanation if `explanations` was a
            single string, or a list of AttributionExplanation objects if
            a list of explanations was requested.
        """
        # Explains a model's prediction on a single instance
        # wrap single explanation name in a list for the API
        if isinstance(explanations, str):
            explanations = (explanations,)

        data_array = _df_to_dict(df)
        payload = dict(
            project_id=project_id,
            model_id=model_id,
            data=data_array[0],
            explanations=[dict(explanation=ex) for ex in explanations],
        )
        if dataset_id is not None:
            payload['dataset'] = dataset_id

        payload.pop('project_id')
        payload.pop('model_id')

        path = ['explain', self.org_id, project_id, model_id]
        res = self._call_executor_service(path, json_payload=payload)

        explanations_list = res['explanations']

        if return_raw_response:
            return explanations_list

        # TODO: enable more robust check for multiclass explanations
        is_multiclass = 'explanation' not in explanations_list[0]
        deserialize_fn = (
            MulticlassAttributionExplanation.from_dict
            if is_multiclass
            else AttributionExplanation.from_dict
        )
        ex_objs = [
            deserialize_fn(explanation_dict) for explanation_dict in explanations_list
        ]
        if len(ex_objs) == 1:
            return ex_objs[0]
        else:
            return ex_objs

    def run_feature_importance(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        dataset_splits: Optional[List[str]] = None,
        slice_query: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Get global feature importance for a model over a dataset.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param dataset_splits: If specified, importance will only be computed
            over these splits. Otherwise, all splits will be used. Only a
            single split is currently supported.
        :param slice_query: A special SQL query.
        :param kwargs: Additional parameters to be passed to the importance
            algorithm. For example, `n_inputs`, `n_iterations`, `n_references`,
            `ci_confidence_level`.
        :return: A named tuple with the explanation results.
        """
        if dataset_splits is not None and len(dataset_splits) > 1:
            raise NotImplementedError(
                'Unfortunately, only a single split is '
                'currently supported for feature '
                'importances.'
            )
        source = None if dataset_splits is None else dataset_splits[0]

        payload = dict(
            subject='feature_importance',
            project_id=project_id,
            model_id=model_id,
            dataset_id=dataset_id,
            source=source,
            slice_query=slice_query,
        )
        payload.update(kwargs)

        try:
            path = ['v1/model_explanation', 'run', self.org_id]
            res = self._call(path, json_payload=payload)
        except Exception:
            payload.pop('subject')
            payload.pop('project_id')
            payload.pop('model_id')
            payload['dataset'] = payload.pop('dataset_id')

            path = ['feature_importance', self.org_id, project_id, model_id]
            res = self._call(path, json_payload=payload)
        # wrap results into named tuple
        res = namedtuple('FeatureImportanceResults', res)(**res)
        return res

    def run_fairness(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        protected_features: list,
        positive_outcome: Union[str, int],
        slice_query: Optional[str] = None,
        score_threshold: Optional[float] = 0.5,
    ) -> Dict[str, Any]:
        """Get fairness metrics for a model over a dataset.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.
        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param protected_features: List of protected features
        :param positive_outcome: Name or value of the positive outcome
        :param slice_query: If specified, slice the data.
        :param score_threshold: positive score threshold applied to get outcomes
        :return: A dictionary with the fairness metrics, technical_metrics,
         model_outcomes and correlation_features
        """
        if isinstance(protected_features, str):
            protected_features = [protected_features]

        payload = dict(
            subject='fairness',
            project_id=project_id,
            model_id=model_id,
            dataset_id=dataset_id,
            protected_features=protected_features,
            slice_query=slice_query,
            score_threshold=score_threshold,
            positive_outcome=positive_outcome,
        )

        try:
            path = ['v1/model_fairness', 'run', self.org_id]
            res = self._call(path, json_payload=payload)
        except Exception:
            payload.pop('subject')
            payload.pop('project_id')
            payload.pop('model_id')

            path = ['fairness', self.org_id, project_id, model_id]
            res = self._call(path, json_payload=payload)
        return res

    def get_mutual_information(self, dataset_id, features):
        """
        The Mutual information measures the dependency between two random variables.
        It's a non-negative value. If two random variables are independent MI is equal to zero.
        Higher MI values means higher dependency.

        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param features: list of features to compute mutual information.
        :return: a dictionary of mutual information w.r.t the given features.
        """
        if isinstance(features, str):
            features = [features]
        if not isinstance(features, list):
            raise ValueError(
                f'Invalid type: {type(features)}. Argument features has to be a list'
            )
        correlation = {}
        for col_name in features:
            payload = dict(org=self.org_id, dataset=dataset_id, col_name=col_name)
            path = ['dataset_mutual_information', self.org_id, dataset_id]
            res = self._call(path, json_payload=payload)
            correlation[col_name] = res
        return correlation

    def create_project(self, project_id: str):
        """Create a new project.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine. Must be a short string without whitespace.

        :returns: Server response for creation action.
        """
        res = None
        try:
            path = ['v1', 'project', 'run', self.org_id]
            payload = {'project_id': project_id}
            res = self._call(path, json_payload=payload)
        except RuntimeError:
            path = ['new_project', self.org_id, project_id]
            res = self._call(path)
        except Exception as e:
            if 'already exists' in str(e):
                print('Project already exists, no change.')
            else:
                raise e

        return res

    def create_model(
        self,
        project_id: str,
        dataset_id: str,
        target: str,
        features: Optional[List[str]] = None,
        train_splits: Optional[List[str]] = None,
        model_id: str = 'fiddler_generated_model',
        model_info: Optional[ModelInfo] = None,
    ):
        """Trigger auto-modeling on a dataset already uploaded to Fiddler.

        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.

        :param dataset_id: The unique identifier of the dataset in the
            Fiddler engine.
        :param target: The column name of the target to be modeled.
        :param features: If specified, a list of column names to use as
            features. If not specified, all non-target columns will be used
            as features.
        :param train_splits: A list of splits to train on. If not specified,
            all splits will be used as training data. Currently only a single
            split can be specified if `train_splits` is not None.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine.

        :returns: Server response for creation action.
        """
        if train_splits is not None and len(train_splits) > 1:
            raise NotImplementedError(
                'Sorry, currently only single-split training is '
                'supported. Please only pass a maximum of one element to '
                '`train_splits`.'
            )
        source = None if train_splits is None else train_splits[0]
        dataset_column_names = self.get_dataset_info(dataset_id).get_column_names()

        # raise exception if misspelled target
        if target not in dataset_column_names:
            raise ValueError(
                f'Target "{target}" not found in the columns of '
                f'dataset {dataset_id} ({dataset_column_names})'
            )

        # raise if target in features or features not in columns
        if features is not None:
            if target in features:
                raise ValueError(f'Target "{target}" cannot also be in ' f'features.')
            features_not_in_dataset = set(features) - set(dataset_column_names)
            if len(features_not_in_dataset) > 0:
                raise ValueError(
                    f'All features should be in the dataset, but '
                    f'the following features were not found in '
                    f'the dataset: {features_not_in_dataset}'
                )

        # use all non-target columns from dataset if no features are specified
        if features is None:
            features = list(dataset_column_names)
            features.remove(target)

        payload = {
            'dataset': dataset_id,
            'model_name': model_id,
            'source': source,
            'inputs': features,
            'targets': [target],
        }

        if model_info:
            payload['model_info'] = dict(model=model_info.to_dict())

        path = ['generate', self.org_id, project_id]
        result = self._call_executor_service(path, json_payload=payload)
        return result

    def upload_model_sklearn(
        self,
        model,
        info: ModelInfo,
        project_id: str,
        model_id: str,
        associated_dataset_ids: Optional[List[str]] = None,
    ):
        """Uploads a subclass of sklearn.base.BaseEstimator to the Fiddler
        engine.

        :param model: An instance of a sklearn.base.BaseEstimator object to be
            uploaded. NOTE: custom subclasses are not supported.
        :param info: A ModelInfo object describing the details of the model.
        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine. Must be a short string without
            whitespace.
        :param associated_dataset_ids: The unique identifiers of datasets in
            the Fiddler engine to associate with the model.

        :returns: Server response for upload action.
        """
        assert ' ' not in model_id, 'The model identifier should not contain whitespace'

        model_info = FiddlerApi._add_dataset_ids_to_model_info(
            info, associated_dataset_ids
        )

        # add framework info in ModelInfo
        try:
            sklearn_version_number = model.__getstate__()['_sklearn_version']
            info.framework = f'scikit-learn {sklearn_version_number}'
        except KeyError:
            pass

        sklearn_upload_warning = (
            'You are uploading a scikit-learn model using the Fiddler API.'
            '\nIf this model uses any custom (non-sklearn) code, it will not '
            'run properly on the Fiddler Engine.'
            '\nThe Fiddler engine may not be able to detect this in advance.'
        )
        LOG.warning(sklearn_upload_warning)

        payload = dict(
            project=project_id,
            model=model_id,
            model_schema=dict(model=model_info.to_dict()),
            framework=info.framework,
            model_type='sklearn',
        )
        LOG.info(f'[{model_id}] model upload: uploading pickle')
        with tempfile.TemporaryDirectory() as tmp:
            pickle_path = Path(tmp) / 'model.pkl'
            with pickle_path.open('wb') as pickle_file:
                pickle_file.write(pickle.dumps(model))

                try:
                    endpoint_path = ['v1', 'model', 'upload', self.org_id]
                    result = self._call(
                        endpoint_path, json_payload=payload, files=[pickle_path]
                    )
                except Exception:
                    endpoint_path = ['model_upload', self.org_id]
                    result = self._call(
                        endpoint_path, json_payload=payload, files=[pickle_path]
                    )
                return result

    def upload_model_custom(
        self,
        artifact_path: Path,
        info: ModelInfo,
        project_id: str,
        model_id: str,
        associated_dataset_ids: Optional[List[str]] = None,
        deployment_type: Optional[
            str
        ] = 'predictor',  # model type. one of {'predictor', 'executor'}
        image_uri: Optional[str] = None,  # image to be used for newly uploaded model
        namespace: Optional[str] = 'default',  # kubernetes namespace
        port: Optional[int] = 5100,  # port on which model is served
        replicas: Optional[int] = 1,  # number of replicas
        cpus: Optional[int] = 0.25,  # number of CPU cores
        memory: Optional[str] = '128m',  # amount of memory required.
        gpus: Optional[int] = 0,  # number of GPU cores
        await_deployment: Optional[bool] = True,  # wait for deployment
    ):
        """Uploads a custom model object to the Fiddler engine along with
            custom glue-code for running the model. Optionally, a new runtime
            (k8s deployment) can be specified for the model via
            the deployment_type and the image_uri parameters.

            Note: The parameters namespace, port, replicas, cpus, memory, gpus,
            await_deployment are only used if an image_uri is specified.

        :param artifact_path: A path to a directory containing all of the
            model artifacts needed to run the model. This includes a
            `package.py` file with the glue code needed to run the model.
        :param info: A ModelInfo object describing the details of the model.
        :param project_id: The unique identifier of the model's project on the
            Fiddler engine.
        :param model_id: The unique identifier of the model in the specified
            project on the Fiddler engine. Must be a short string without
            whitespace.
        :param associated_dataset_ids: The unique identifiers of datasets in
            the Fiddler engine to associate with the model.

        :param deployment_type: One of {'predictor', 'executor'}
        'predictor': where the model just exposes a `/predict` endpoint
                     - typically simple sklearn like models
        'executor': where fiddler needs the model internals
                     - typically deep models like tensorflow and pytorch etc

        :param image_uri: A URI of the form <registry>/<image-name>:<tag> which
            if specified will be used to create a new runtime and then serve the
            model.

        :param namespace: The kubernetes namespace to use for the newly created
            runtime.

        :param port: The port to use for the newly created runtime.

        :param replicas: The number of replicas running the model.
        :param cpus: The number of CPU cores reserved per replica.
        :param memory: The amount of memory reservation per replica.
        :param gpus: The number of GPU cores reserved per replica.

        :param await_deployment: whether to block until deployment completes.

        :returns: Server response for upload action.
        """
        assert ' ' not in model_id, 'The model identifier should not contain whitespace'

        if not artifact_path.is_dir():
            raise ValueError(f'The {artifact_path} must be a directory.')

        model_info = FiddlerApi._add_dataset_ids_to_model_info(
            info, associated_dataset_ids
        )

        # upload the model
        payload = dict(
            project=project_id,
            model=model_id,
            model_schema=dict(model=model_info.to_dict()),
            framework=info.framework,
            upload_as_archive=True,
            model_type='custom',
            deployment_type=deployment_type,
            image=image_uri,
            namespace=namespace,
            port=port,
            replicas=replicas,
            cpus=cpus,
            memory=memory,
            gpus=gpus,
            await_deployment=await_deployment,
        )

        with tempfile.TemporaryDirectory() as tmp:
            tarfile_path = Path(tmp) / 'files'
            shutil.make_archive(
                base_name=str(Path(tmp) / 'files'),
                format='tar',
                root_dir=str(artifact_path),
                base_dir='.',
            )
            LOG.info(
                f'[{model_id}] model upload: uploading custom model from'
                f' artifacts in {str(artifact_path)} tarred to '
                f'{str(tarfile_path)}'
            )

            try:
                endpoint_path = ['v1', 'model', 'upload', self.org_id]
                result = self._call(
                    endpoint_path, json_payload=payload, files=[Path(tmp) / 'files.tar']
                )
            except Exception:
                endpoint_path = ['model_upload', self.org_id]
                result = self._call(
                    endpoint_path, json_payload=payload, files=[Path(tmp) / 'files.tar']
                )
            return result

    def upload_model_package(
        self,
        artifact_path: Path,
        project_id: str,
        model_id: str,
        deployment_type: Optional[
            str
        ] = 'predictor',  # model deployment type. One of {'predictor', 'executor'}
        image_uri: Optional[str] = None,  # image to be used for newly uploaded model
        namespace: Optional[str] = 'default',  # kubernetes namespace
        port: Optional[int] = 5100,  # port on which model is served
        replicas: Optional[int] = 1,  # number of replicas
        cpus: Optional[int] = 0.25,  # number of CPU cores
        memory: Optional[str] = '128m',  # amount of memory required.
        gpus: Optional[int] = 0,  # number of GPU cores
        await_deployment: Optional[bool] = True,  # wait for deployment
    ):
        if not artifact_path.is_dir():
            raise ValueError(f'not a valid model dir: {artifact_path}')
        yaml_file = artifact_path / 'model.yaml'
        if not yaml_file.is_file():
            raise ValueError(f'Model yaml not found {yaml_file}')
        with yaml_file.open() as f:
            model_info = ModelInfo.from_dict(yaml.safe_load(f))
            self.upload_model_custom(
                artifact_path,
                model_info,
                project_id,
                model_id,
                deployment_type=deployment_type,
                image_uri=image_uri,
                namespace=namespace,
                port=port,
                replicas=replicas,
                cpus=cpus,
                memory=memory,
                gpus=gpus,
                await_deployment=await_deployment,
            )

    def await_model_deployment(
        self,
        project_id: str,
        model_id: str,
    ):
        """
        Await model deployment.
        """
        assert ' ' not in model_id, 'The model identifier should not contain whitespace'

        endpoint_path = ['model_await_deployment', self.org_id]
        payload = dict(
            project=project_id,
            model=model_id,
        )
        return self._call(endpoint_path, json_payload=payload)

    def delete_model_deployment(
        self,
        project_id: str,
        model_id: str,
    ):
        """
        Delete the model deployment.
        """
        assert ' ' not in model_id, 'The model identifier should not contain whitespace'

        endpoint_path = ['model_delete_deployment', self.org_id]
        payload = dict(
            project=project_id,
            model=model_id,
        )
        return self._call(endpoint_path, json_payload=payload)

    def create_surrogate_model(
        self, project_id, name, baseline_df, dataset_info, target, features
    ):
        """
        Uploads a baseline to fiddler, and creates a surrogate model
        and sets up monitoring on this stream

        :param project_id: id of the project
        :param name: name to be used for the dataset and model
        :param baseline_df: baseline Dataframe
        :param dataset_info: schema for the baseline
        :param target: target for the generated model
        :param features: input features to the model
        :return: location of the newly created model
        """
        print('Validating inputs ...')
        try:
            self.get_dataset_info(name)
            raise ValueError(f'name already in used: {name}')
        except Exception:
            LOG.info('dataset not found, creating it')

        print('Uploading dataset ...')

        dataset_info.dataset_id = name
        self.upload_dataset(baseline_df, name, split_test=False, info=dataset_info)
        train_splits = ['data']
        print('Generating surrogate model ...')
        self.create_model(
            project_id,
            name,
            target=target,
            features=features,
            train_splits=train_splits,
            model_id=name,
        )
        print('Triggering model predictions ...')
        self.trigger_model_predictions(project_id, name, name)

        project_url = self.url.replace('host.docker.internal', 'localhost', 1)
        return (
            f'Surrogate model successfully setup on Fiddler. \n '
            f'Visit {project_url}/projects/{project_id} '
        )

    def create_model_from_prediction_log(
        self,
        project_id,
        model_id,
        prediction_log_df,
        features,
        outputs,
        model_task,
        dataset_info=None,
    ):
        """
        Creates a model based on the prediction log specified.

        :param project_id: id of the project
        :param model_id: name to be used for the dataset and model
        :param prediction_log_df: production log Dataframe
        :param features: input features to the model
        :param outputs: model outputs
        :param model_task:
        :param dataset_info: schema for the baseline
        :param model_task: type of the model eg: binary_classification
        :return: location of the newly created model
        """
        print('Validating inputs ...')
        try:
            self.get_dataset_info(model_id)
            raise ValueError(f'name already in used: {model_id}')
        except Exception:
            LOG.info('dataset not found, creating it')

        print('Uploading dataset ...')
        baseline_df = prediction_log_df.drop(columns=outputs)

        if not dataset_info:
            dataset_info = DatasetInfo.from_dataframe(
                baseline_df, max_inferred_cardinality=1000
            )

        dataset_info.dataset_id = model_id
        self.upload_dataset(baseline_df, model_id, split_test=False, info=dataset_info)
        print('Setting up monitoring without model artifact ...')
        package_py = (
            'def get_model():\n\traise RuntimeError("Model artifact not available")'
        )
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            model_info = ModelInfo.from_dataset_info(
                dataset_info=dataset_info,
                target=None,
                features=features,
                display_name=model_id,
                description='Model-less monitoring',
                model_task=model_task,
                outputs=outputs,
            )
            model_info.framework = None
            model_info.artifact_status = ArtifactStatus.NO_MODEL
            package_py_file = tmp_dir / 'package.py'
            with open(package_py_file, mode='w') as fid:
                fid.write(package_py)
            self.upload_model_custom(tmp_dir, model_info, project_id, model_id)

        output_columns = [Column('__dataset_fiddler_id', DataType.INTEGER).to_dict()]
        for output in outputs:
            output_columns.append(Column(output, DataType.FLOAT).to_dict())

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            output_df = prediction_log_df[outputs]
            output_df.insert(0, '__dataset_fiddler_id', range(1, 1 + len(output_df)))
            path = tmp_dir / 'data.csv'
            output_df.to_csv(path, index=False, header=None)
            self._import_model_predictions(
                project_id, model_id, model_id, output_columns, [path]
            )

        project_url = self.url.replace('host.docker.internal', 'localhost', 1)
        return (
            f'Monitoring successfully setup on Fiddler. \n '
            f'Visit {project_url}/projects/{project_id} to monitor'
        )

    @staticmethod
    def _add_dataset_ids_to_model_info(model_info, associated_dataset_ids):
        model_info = copy.deepcopy(model_info)
        # add associated dataset ids to ModelInfo
        if associated_dataset_ids is not None:
            for dataset_id in associated_dataset_ids:
                assert (
                    ' ' not in dataset_id
                ), 'Dataset identifiers should not contain whitespace'
            model_info.misc['datasets'] = associated_dataset_ids
        return model_info

    def trigger_dataset_import(self, dataset_id: str):
        """Makes the Fiddler service (re-)import the specified dataset."""
        return self._db_import(dataset_id)

    def trigger_model_predictions(
        self, project_id: str, model_id: str, dataset_id: str
    ):
        """Makes the Fiddler service compute and cache model predictions on a
        dataset."""
        payload = dict(model=model_id, dataset=dataset_id)
        result = self._call_executor_service(
            ['dataset_predictions', self.org_id, project_id], payload
        )

        return result

    def trigger_pre_computation(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        overwrite_cache: Optional[bool] = False,
        batch_size: Optional[int] = 10,
        calculate_predictions: Optional[bool] = True,
        cache_global_pdps: Optional[bool] = True,
        cache_global_impact_importance: Optional[bool] = True,
    ):
        """Triggers various precomputation steps within the Fiddler service based on input parameters.

        :param project_id:                        the project to which the model whose events are
                                                  being published belongs.
        :param model_id:                          the model whose events are being published.
        :param dataset_id:                        id of the dataset to be used.
        :param overwrite_cache:                   Boolean indicating whether to overwrite previously cached
                                                  information.
        :param batch_size:                        Batch size of global PDP calculation.
        :param calculate_predictions:             Boolean indicating whether to pre-calculate and store model
                                                  predictions.
        :param cache_global_pdps:                 Boolean indicating whether to pre-calculate and cache global partial
                                                  dependence plots.
        :param cache_global_impact_importance:    Boolean indicating whether to pre-calculate and global feature impact
                                                  and global feature importance.
        """
        if calculate_predictions:
            print(
                f'Beginning to process and upload predictions for dataset {dataset_id} with model {model_id}...'
            )

            path = ['dataset_predictions', self.org_id, project_id]
            payload = dict(model=model_id, dataset=dataset_id)
            result = self._call_executor_service(path, payload)

            print(f'{result}\n')

        if cache_global_pdps or cache_global_impact_importance:
            print(
                f'Beginning to precache for dataset {dataset_id} with model {model_id}...'
            )

            path = ['precache_globals', self.org_id, project_id, model_id]
            payload = {
                'dataset_id': dataset_id,
                'cache_global_pdps': cache_global_pdps,
                'cache_global_impact_importance': cache_global_impact_importance,
                'overwrite_cache': overwrite_cache,
                'batch_size': batch_size,
            }

            result = self._call_executor_service(path, payload, stream=True)
            for res in result:
                print(res)

    def publish_event(
        self,
        project_id: str,
        model_id: str,
        event: dict,
        event_id: Optional[str] = None,
        update_event: Optional[bool] = None,
        event_time_stamp: Optional[int] = None,
    ):
        """
        Publishes an event to Fiddler Service.
        :param project_id: the project to which the model whose events are
                           being published belongs
        :param model_id: the model whose events are being published
        :param dict event: Dictionary of event details, such as features
                           and predictions.
        :param event_id: unique str event id for the event
        :param update_event: if the event is an update to a previously
                             published row
        :param event_time_stamp: the UTC timestamp of the event in
                                 milliseconds

        """
        if update_event:
            event['__event_type'] = 'update_event'
            event['__updated_at'] = event_time_stamp
            if event_id is None:
                raise ValueError('An update event needs an event_id')
        else:
            event['__event_type'] = 'execution_event'
            event['__occurred_at'] = event_time_stamp

        if event_id is not None:
            event['__event_id'] = event_id

        path = ['external_event', self.org_id, project_id, model_id]
        result = self._call(path, event)

        return result

    def add_monitoring_config(
        self,
        config_info: dict,
        project_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ):
        """Adds a config for either an entire org, or project or a model.
        Here's a sample config:
        {
            'min_bin_value': 3600, # possible values 300, 3600, 7200, 43200, 86400, 604800 secs
            'time_ranges': ['Day', 'Week', 'Month', 'Quarter', 'Year'],
            'default_time_range': 7200,
            'event_sampling_rate': 1.0,
            'tag': 'anything you want'
        }
        """
        path = ['monitoring_setup', self.org_id]
        if project_id:
            path.append(project_id)
        if model_id:
            if not project_id:
                raise ValueError(
                    'We need to have a project_id when a model is specified'
                )
            path.append(model_id)

        result = self._call(path, config_info)
        return result

    def publish_events_log(
        self,
        project_id: str,
        model_id: str,
        logs: pd.DataFrame,
        force_publish: Optional[bool] = None,
        ts_column: Optional[str] = None,
        default_ts: Optional[int] = None,
    ):
        """
        Publishes prediction log to Fiddler Service.
        :param project_id:    the project to which the model whose events are
                              being published belongs
        :param model_id:      the model whose events are being published
        :param logs:          data frame of event details, such as features
                              and predictions.
        :param force_publish: continue with publish even if all input and
                              output columns not in log.
        :param ts_column:     column to extract time stamp value from.
        :param default_ts:    default time stamp to use if ts_column not specified.
        """
        try:
            model_info = self.get_model_info(project_id, model_id)
        except RuntimeError:
            raise RuntimeError(
                f'Did not find ModelInfo for project "{project_id}" and model "{model_id}".'
            )

        log_columns = [c for c in list(logs.columns)]
        in_columns = [c.name for c in model_info.inputs]
        in_not_found = [c for c in in_columns if c not in log_columns]
        out_columns = [c.name for c in model_info.outputs]
        out_not_found = [c for c in out_columns if c not in log_columns]
        if (out_not_found or in_not_found) and not force_publish:
            raise ValueError(
                f'Model output columns "{out_not_found}" or input columns "{in_not_found}"'
                f'not found in logs. If this is expected try again with force_publish=True.'
            )

        payload = dict()
        if ts_column is not None:
            if ts_column not in log_columns:
                raise ValueError(f'Did not find {ts_column} in the logs columns.')
            payload['ts_column'] = ts_column
        else:
            if default_ts is None:
                default_ts = int(round(time.time() * 1000))
            payload['default_ts'] = default_ts

        include_index = logs.index.name is not None
        with tempfile.TemporaryDirectory() as tmp:
            csv_paths = list()
            csv_path = Path(tmp) / 'log.csv'
            logs.to_csv(csv_path, index=include_index)
            csv_paths.append(csv_path)
            path = ['publish_events_log', self.org_id, project_id, model_id]
            result = self._call(path, json_payload=payload, files=csv_paths)
            return result

    def publish_parquet_s3(
        self,
        project_id: str,
        model_id: str,
        parquet_file: str,
        auth_context: Optional[Dict[str, Any]] = None,
        ts_column: Optional[str] = None,
        default_ts: Optional[int] = None,
    ):
        """
        Publishes parquet events file from S3 to Fiddler instance. Experimental and may be expanded in the future.

        :param project_id:    the project to which the model whose events are
                              being published belongs
        :param model_id:      the model whose events are being published
        :param parquet_file:  s3_uri for parquet file to be published
        :param auth_context:  Dictionary containing authorization for AWS. List of expected keys are
                              ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token']
                              with 'aws_session_token' being applicable to the AWS account being used.
        :param ts_column:     column to extract time stamp value from.
        :param default_ts:    default time stamp to use if ts_column not specified.
        """
        payload = dict()
        payload['file_path'] = parquet_file
        payload['auth_context'] = auth_context
        if ts_column is not None:
            payload['ts_column'] = ts_column
        else:
            if default_ts is None:
                default_ts = int(round(time.time() * 1000))
            payload['default_ts'] = default_ts

        publish_path = ['publish_parquet_file', self.org_id, project_id, model_id]
        publish_result = self._call(publish_path, json_payload=payload, stream=True)
        for res in publish_result:
            print(res)

    def register_model(
        self, project_id: str, model_id: str, dataset_id: str, model_info: ModelInfo
    ):
        """
        Register a model in fiddler. This will generate a surrogate model,
        which can be replaced later with original model.

        Note: This method can take a while if the dataset is large. It is
        recommended to call register_model on a smaller representative
        dataset, before trying out on larger dataset.

        :param project_id: id of the project
        :param model_id: name to be used for the dataset and model
        :param dataset_id: id of the dataset to be used
        :param model_info: model info
        """
        print('Loading dataset info ...')
        dataset_info = self.get_dataset_info(dataset_id)

        print('Validating model info ...')
        ModelInfoValidator(model_info, dataset_info).validate()

        print('Generating model ...')
        for i in range(3):
            try:
                self.create_model(
                    project_id,
                    dataset_id,
                    target=model_info.targets[0].name,
                    features=[],
                    train_splits=None,
                    model_id=model_id,
                    model_info=model_info,
                )
                break
            except Exception:
                print('retrying ...')
                pass

        output_names = [o.name for o in model_info.outputs]
        dataset_cols = [c.name for c in dataset_info.columns]
        outputs_available = all(elem in dataset_cols for elem in output_names)

        if outputs_available:
            print('Model output provided')
            fiddler_id_fk = '__dataset_fiddler_id'
            outputs_df = self.get_slice(
                sql_query=f'select {",".join(output_names)} from {dataset_id}',
                project=project_id,
            )
            outputs_df[fiddler_id_fk] = outputs_df['__fiddler_id']
            output_names.insert(0, fiddler_id_fk)
            outputs_df = outputs_df[output_names]

            output_columns = [Column(fiddler_id_fk, DataType.INTEGER)]
            output_columns.extend(model_info.outputs)

            with tempfile.TemporaryDirectory() as tmp:
                tmp_dir = Path(tmp)
                path = tmp_dir / 'data.csv'
                outputs_df.to_csv(path, index=False, header=None)
                self._import_model_predictions(
                    project_id,
                    dataset_id,
                    model_id,
                    [oc.to_dict() for oc in output_columns],
                    [path],
                )
        else:
            print('Model output not given, calculating model prediction')
            self.trigger_model_predictions(project_id, model_id, dataset_id)

        project_url = self.url.replace('host.docker.internal', 'localhost', 1)
        return (
            f'Model successfully registered on Fiddler. \n '
            f'Visit {project_url}/projects/{project_id} '
        )

    def generate_sample_events(
        self,
        project_id: str,
        model_id: str,
        dataset_id: str,
        number_of_events: Optional[int] = 100,
        time_range: Optional[int] = 8,
    ):
        """
        Generate monitoring traffic for the given model. Traffic is generated
        by randomly sampling rows from the specified dataset.

        Note: This method can be used to generate monitoring traffic for
        testing purpose. In production, use publish_event or publish_events_logs
        to send model input and output to fiddler.

        :param project_id:
        :param model_id:
        :param dataset_id:
        :param number_of_events: number of prediction events to generate
        :param time_range: number of days. time_range is used
                to spread the traffic
        :return: stats about generated events
        """

        if number_of_events < 1 or number_of_events > 1000:
            raise ValueError('number_of_events must be between 1 and 1000')

        if time_range < 1 or time_range > 365:
            raise ValueError('time_range must be between 1 and 365 days')

        dataset_dict = self.get_dataset(
            dataset_id, max_rows=number_of_events, sampling=True
        )

        datasets = dataset_dict.values()
        for df in datasets:
            df.reset_index(inplace=True, drop=True)

        event_sample_df = pd.concat(datasets, ignore_index=True)
        if len(event_sample_df) > number_of_events:
            event_sample_df = event_sample_df[:number_of_events]

        # get prediction result
        result = self.run_model(project_id, model_id, event_sample_df, log_events=False)

        result_df = pd.concat([event_sample_df, result], axis=1)

        # create well distributed time stamps
        ONE_DAY_MS = 8.64e7
        event_time = round(time.time() * 1000) - (ONE_DAY_MS * time_range)
        interval = round((time.time() * 1000 - event_time) / number_of_events)
        time_stamp = []
        for i in range(0, len(result_df)):
            time_stamp.append(event_time)
            event_time = event_time + random.randint(1, interval * 2)
        result_df['__occurred_at'] = time_stamp

        return self.publish_events_log(
            project_id,
            model_id,
            result_df,
            force_publish=False,
            ts_column='__occurred_at',
        )
