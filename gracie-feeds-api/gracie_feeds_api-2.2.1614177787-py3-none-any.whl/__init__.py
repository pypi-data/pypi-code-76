server_type = 'feeds'

name = "gracie_api"
import errno
import hashlib
# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import tempfile
import time
from inspect import signature

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), server_type + '_controllers_classes'))
# sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

if server_type == 'feeds':
    from gracie_feeds_api.GracieAuth import GracieSSOAuth
    from gracie_feeds_api.GracieAPIClassLoader import GracieApiClassLoader
    from gracie_feeds_api.GracieErrors import GracieAPIResponseError
    from gracie_feeds_api.GracieErrors import GracieAuthError
    from gracie_feeds_api.GracieErrors import GracieError
    from gracie_feeds_api.GracieErrors import MissingDirectory
    from gracie_feeds_api.GracieErrors import FileAccessError
    from gracie_feeds_api.GracieErrors import gracieAPIUnknownParameter
    from gracie_feeds_api.GracieErrors import gracieAPIUnknownSendDataType
elif server_type == 'dictionary':
    from gracie_dictionary_api.GracieAuth import GracieSSOAuth
    from gracie_dictionary_api.GracieAPIClassLoader import GracieApiClassLoader
    from gracie_dictionary_api.GracieErrors import GracieAPIResponseError
    from gracie_dictionary_api.GracieErrors import GracieAuthError
    from gracie_dictionary_api.GracieErrors import GracieError
    from gracie_dictionary_api.GracieErrors import MissingDirectory
    from gracie_dictionary_api.GracieErrors import FileAccessError
    from gracie_dictionary_api.GracieErrors import gracieAPIUnknownSendDataType
    from gracie_dictionary_api.GracieErrors import gracieAPIUnknownParameter
else:
    raise BaseException('Unknown server type %s' % server_type)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

THIS_FILE_PATH = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
if 'CONTROLLERS_CLASSES_PATH' in os.environ:
    CONTROLLERS_CLASSES_PATH = os.environ['CONTROLLERS_CLASSES_PATH']
else:
    CONTROLLERS_CLASSES_PATH = server_type + '_controllers_classes'


class GracieBaseAPI(GracieAPIResponseError, GracieError, GracieAuthError, GracieSSOAuth):
    _session = None

    def __init__(self):
        pass

    def _format_params_for_api(self, set_api_params=None, parameters_names=None, parameters_names_map={}):
        skip_vars = ['api', 'actions', 'all_api_parameters']

        if not set_api_params:
            return

        params = {}
        data = None
        for var_name in set_api_params.keys():
            if var_name != 'self' and var_name not in skip_vars and set_api_params[var_name] is not None:

                if var_name == 'kwargs':
                    for v_n in set_api_params[var_name]:
                        if v_n in parameters_names_map:
                            _v_n = parameters_names_map[v_n]
                        else:
                            _v_n = v_n

                        if v_n in parameters_names:
                            if parameters_names[v_n]['in'] == 'query' or \
                                    parameters_names[v_n]['in'] == 'formData':
                                params.update({v_n: set_api_params[var_name][v_n]})
                            elif parameters_names[v_n]['in'] == 'body':
                                data = set_api_params[var_name][v_n]
                            else:
                                raise gracieAPIUnknownSendDataType(
                                    '%s is not query or body' % set_api_params[var_name]['in'])
                        else:
                            raise gracieAPIUnknownParameter(
                                '%s is not a know parameter for this API' % v_n)
                else:
                    if parameters_names and var_name not in parameters_names:
                        continue

                    # some params are not compatible with python
                    # map back to the correct param name for the Gracie API
                    if var_name in parameters_names_map:
                        var_name = parameters_names_map[var_name]

                    if var_name in parameters_names:
                        if parameters_names[var_name]['in'] == 'query' or \
                                parameters_names[var_name]['in'] == 'formData':
                            params.update({var_name: set_api_params[var_name]})
                        elif parameters_names[var_name]['in'] == 'body':
                            data = set_api_params[var_name]
                        else:
                            raise gracieAPIUnknownSendDataType(
                                '%s is not query or body' % set_api_params[var_name]['in'])

        if len(params) == 0:
            params = None

        return params, data

    def _start_session(self):
        if self._session:
            self._close_session()
        self._session = requests.session()

    def _close_session(self):
        self._session = None

    def _prepare_file_for_upload(self, file):
        if not os.path.isfile(file):
            raise GracieAPI('Missing upload file', file)

        return {'file': open(file, 'rb')}

    def _prepare_files_for_upload(self, files):
        if type(files) is not list:
            files = [files]

        upload_files = []
        for upload_file in files:
            if not os.path.isfile(upload_file):
                raise GracieAPI('Missing upload file', upload_file)

            file_tuple = ('files', open(upload_file, 'rb'))
            upload_files.append(file_tuple)

        if len(upload_files) < 1:
            return None
        return upload_files

    def _md5(self, file_name):
        try:
            hash_md5 = hashlib.md5()
            with open(file_name, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except:
            raise FileAccessError('Error creating file hash for download file %s' % file_name)

        return hash_md5.hexdigest()

    def _process_api(self, controller_name, api, actions, params, data, consumes=None):
        if not self._session:
            self._start_session()

        files = None
        if params:
            if 'file' in params:
                files = self._prepare_file_for_upload(params['file'])
                del params['file']
            elif 'files' in params:
                files = self._prepare_files_for_upload(params['files'])
                del params['files']

        api_url = '%s://%s:%s%s%s' % (self._http_protocol, self._gracie_host, self._port, self._api_prefix, api)

        if 'post' in actions:
            session_action = self._session.post
        elif 'get' in actions:
            session_action = self._session.get
        elif 'put' in actions:
            session_action = self._session.put
        elif 'delete' in actions:
            session_action = self._session.delete
        else:
            raise GracieError('Bad http action %s attempted on api: %s' % (','.join(actions), api))

        headers = self.access_headers
        if data:
            if not consumes:
                data = data.encode('utf-8')
                headers.update({'Content-type': 'text/plain; charset=utf-8'})
            else:
                # only serialize list, dict, and tuple - other types are fine
                if isinstance(data, list) or isinstance(data, dict) or isinstance(data, tuple):
                    data = json.dumps(data)
                headers.update({'Content-type': '%s' % consumes[0]})

        if not files:
            response = session_action(api_url, params=params, data=data, verify=self._verify_ssl, proxies=self._proxies,
                                      headers=headers)
        else:
            response = session_action(api_url, params=params, data=data, files=files, verify=self._verify_ssl,
                                      proxies=self._proxies, headers=headers)

        if response.status_code == 401:
            if controller_name == 'logoutController':
                raise GracieAPIResponseError(401, 'Authentication required')
            else:
                raise GracieAPIResponseError(401, 'Invalid session')

        if response.status_code == 403:
            raise GracieAPIResponseError(403, 'Access is forbidden')

        elif 'content-type' in response.headers and response.headers[
            'content-type'].lower() == 'application/octet-stream':
            file_name = re.findall('filename=(.+)', response.headers.get('content-disposition'))[0]
            save_file = os.path.join(self._download_location, file_name)
            if os.path.exists(save_file):
                try:
                    os.unlink(save_file)
                except OSError as e:
                    if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                        raise

            try:
                with open(save_file, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=128):
                        fd.write(chunk)
            except OSError as e:
                raise FileAccessError('Unable to save file %s - %s' % (file_name, e))
            return {
                'downloadFile': save_file,
                'fileSize': os.path.getsize(save_file),
                'fileHash': self._md5(save_file)
            }

        elif not response.status_code == 200 or response.json()['status'] is False:
            try:
                response_data = json.loads(response.content)
            except:
                e = sys.exc_info()[0]
                raise GracieError('Unable to "%s" on api "%s": (%s)' % (','.join(actions), api, response.content))
            raise GracieError('Unable to "%s" on api "%s": %s' % (
                ','.join(actions), api, response_data['message']))

        if hasattr(response, 'json'):
            return response.json()['response']


class GracieAPI(GracieApiClassLoader, GracieBaseAPI):
    """GracieAPI - Gracie AI platform API wrapper.

    Attributes:
        wait_for_task_complete: Wait for long running tasks to complete before response
        remove_task_data_on_complete: Remove task data from long running task once complete without error
        full_results: Return full results from API calls, not just results from search
    """

    _gracie_host = None
    _port = 443
    _verify_ssl = False
    _http_protocol = 'https'
    _proxies = None
    _download_location = None
    _api_prefix = ''

    _class_loader = None
    _api_controllers = []
    _controller_name = None

    _wait_for_task_complete = True
    _remove_task_data_on_complete = True
    _full_results = False

    def __init__(self, host, sso_host, port, login_name, login_password,
                 require_ssl=True,
                 verify_ssl=False,
                 wait_for_task_complete=True,
                 remove_task_data_on_complete=True,
                 proxies=None,
                 download_file_location=None,
                 api_prefix=None):

        self._gracie_host = host
        self._port = port
        self._wait_for_task_complete = wait_for_task_complete
        self._remove_task_data_on_complete = remove_task_data_on_complete
        self._proxies = proxies

        if download_file_location:
            self._download_location = download_file_location
        else:
            self._download_location = tempfile.gettempdir()
        if not os.path.isdir(self._download_location):
            raise MissingDirectory('Missing download directory %s' % self._download_location)

        if require_ssl:
            self._http_protocol = 'https'
        else:
            self._http_protocol = 'http'

        self._verify_ssl = verify_ssl

        if isinstance(api_prefix, str):
            self._api_prefix = api_prefix

        GracieBaseAPI.__init__(self)
        GracieApiClassLoader.__init__(self, CONTROLLERS_CLASSES_PATH)
        GracieSSOAuth.__init__(self, sso_host, login_name, login_password, verify_ssl)

    @property
    def wait_for_task_complete(self):
        return self.wait_for_task_complete

    @wait_for_task_complete.setter
    def wait_for_task_complete(self, bool_val):
        if not isinstance(bool_val, bool):
            raise GracieError('Bad value - must be True or False')
        self._wait_for_task_complete = bool_val

    @property
    def remove_task_data_on_complete(self):
        return self._remove_task_data_on_complete

    @remove_task_data_on_complete.setter
    def remove_task_data_on_complete(self, bool_val):
        if not isinstance(bool_val, bool):
            raise GracieError('Bad value - must be True or False')
        self._remove_task_data_on_complete = bool_val

    @property
    def download_file_location(self):
        return self.download_file_location

    @download_file_location.setter
    def download_file_location(self, bool_val):
        if not isinstance(bool_val, bool):
            raise GracieError('Bad value - must be True or False')
        self.download_file_location = bool_val

    @property
    def full_results(self):
        return self._full_results

    @full_results.setter
    def full_results(self, bool_val):
        if not isinstance(bool_val, bool):
            raise GracieError('Bad value - must be True or False')
        self._full_results = bool_val

    def _get_api_from_controller(self, controller_name, api):
        if controller_name not in self._controller_classes:
            raise GracieError('Invalid controller')

        if api not in self._controller_classes[controller_name].__dict__.keys():
            raise GracieError('%s API does not exist in controller' % api)

        api_class_method = getattr(self._controller_classes[controller_name], api)
        sig = signature(api_class_method)

        function_params = ['self']
        has_kawargs = False
        for k, v in sig.parameters.items():
            if k == 'kwargs':
                has_kawargs = True
            elif k != 'self':
                function_params.append(str(v))
        if has_kawargs:
            function_params.append('**kwargs')

        return len(sig.parameters), api_class_method, function_params

    def _wait_for_task_results(self, task_data, remove_results=True, sleep_time=1):
        while True:
            if task_data and 'status' in task_data:

                if server_type == 'feeds' and 'taskId' in task_data:
                    task_id = task_data['taskId']
                elif 'id' in task_data:
                    task_id = task_data['id']
                else:
                    raise GracieAPIResponseError('Task id not found in results')

                task_data = self.call_api('tasksController', 'retrieve', id=task_id)
                if task_data and 'status' in task_data and \
                        type(task_data['status']) is str and \
                        (task_data['status'].lower() == 'completed' or task_data['status'].lower() == 'failed'):
                    break
            time.sleep(sleep_time)

        if remove_results:
            self.call_api('tasksController', 'delete', id=task_id)
            if task_data['error']:
                raise GracieError(task_data['error'])

        if self._full_results:
            return task_data
        else:
            return task_data['result']

    def call_api(self, controller_name, api, **kwargs):
        """Gracie API request

                Args:
                    controller_name: (string): Name of Gracie controller
                    api: (string): Name of Gracie controller api
                    **kargs: Name/value pairs of API params
                Returns:
                    API response
        """

        arg_len, api_obj, function_params = self._get_api_from_controller(controller_name, api)
        self._controller_name = controller_name
        function_sig = 'api_obj(%s)' % ', '.join(function_params)

        _kwargs = None
        if kwargs:
            thismodule = sys.modules[__name__]
            _kwargs = kwargs
            for p in function_params:
                found = False
                if p in _kwargs:
                    setattr(thismodule, p, kwargs[p])
                    del _kwargs[p]
                    found = True
                if not found and p != 'self' and p != '**kwargs':
                    function_params.remove('self')
                    raise GracieError('Missing API parameter(s) "%s" for %s' % (', '.join(function_params),
                                                                                self._controller_name),
                                      'Required parameter: %s' % ', '.join(function_params))

        if _kwargs and len(_kwargs) > 0:
            kwargs = _kwargs

        # counter = 0
        while True:
            # counter += 1
            # try:
            api_ret_data = eval(function_sig)
            if controller_name != 'tasksController' and \
                    'status' in api_ret_data and \
                    api_ret_data['status'].lower() != 'unchanged' and \
                    self._wait_for_task_complete:
                return self._wait_for_task_results(api_ret_data, self._remove_task_data_on_complete)
            return api_ret_data

            # except GracieAPIResponseError as e:
            #     if counter > 2 or e.message == 401:
            #         raise GracieError('API error: (%s) %s' % (e.parameter, ' - '.join(e.args)))
            #     else:
            #         break
