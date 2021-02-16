#
#    (C) Quantum Computing Inc., 2020.
#
#    THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE of the Copyright Holder. 
#    The contents of this file may not be disclosed to third parties, copied 
#    or duplicated in any form, in whole or in part, without the prior written
#    permission of the Copyright Holder.
#
from typing import Tuple, Callable, Union, Any, Optional
import requests
import time
import os
import sys
from datetime import datetime as dt
import dateutil as du
import yaml
import json
import numpy as np
import scipy.sparse as sp
import networkx as nx
from warnings import warn
from requests_toolbelt.multipart import encoder

from qatalyst.package_info import __version__

from .encoders import encode_data, encode_sparse_array, encode_ndarray, encode_graph
from .decoders import decodeResponse
from .utils import print_available_samplers, \
    load_available_samplers, \
    get_scipy_minimize_methods, \
    param_check, \
    check_dwave_size, \
    parse_status
from .data_processing import TicToc, Status, StatusCodes, AwsDeviceClient


def get_client_kwargs(**kwargs):
    """
    From kwargs extract arguments relevant to Client instances.

    :param kwargs: dict, user-provided kwargs
    :return: client arguments dictionary, parameter dictionary
    """
    client_kwargs = {'username': None,
                     'password': None,
                     'access_token': None,
                     'sampler': 'csample',
                     'configuration': 'default',
                     'conf_path': None,
                     'url': 'https://api.qci-prod.com'}
    for key in client_kwargs:
        if key in kwargs:
            # We use `pop` so that items do not get passed to the
            # server if not necessary.
            client_kwargs[key] = kwargs.pop(key)
    return client_kwargs, kwargs


class HTTPClient:

    # default paths to look for the user configuration file
    CONF_PATHS = ('~/.qci.conf', '~/.qci/qci.conf')

    STATUS_MESSAGE = '\n{} | Problem started\n'

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 access_token: str = None,
                 configuration: str = 'default',
                 conf_path: str = None,
                 url: str = 'https://api.qci-prod.com',
                 braket_url: str = None):
        """Initialize the HTTPClient.

        :param :dict:`options: { url: str, username: str, password: str, access_token: str }`
        """
        self.url = url
        self.username = username
        self.password = password
        self.access_token = access_token
        self.configuration = configuration

        conf = self.get_config(path=conf_path)
        self.conf = conf[self.configuration]
        # fill username, password, access_token with conf file values if the former are None
        self.set_attributes()

        # endpoints
        self.post_endpoint = '/queues/submit'
        self.status_endpoint = '/queues/status?JobID={}'
        self.result_endpoint = '/queues/result?JobID={}'

        # braket-specific API variables (braket_url used mostly for testing)
        self.braketcheck_url = braket_url or url
        self.braketcheck_endpoint = '/braketcheck'

        self.JobId = None

        # delay in seconds
        self.delay = 1
        self.delay_incr = 1
        self.max_delay = 10
        self.status_message_written = False
        self.status_codes = StatusCodes

        self._status_time = None
        # self._status = None

    @property
    def status_time(self):
        return self._status_time

    @status_time.setter
    def status_time(self, val):
        self._status_time = val

    def __authenticate(self) -> str:
        r"""Try to authenticate against the csample /authorize endpoint"""

        user = {}
        if self.username:
            user['Username'] = self.username

        if self.password:
            user['Password'] = self.password

        if self.access_token:
            user['AccessToken'] = self.access_token

        headers = {"Qatalyst-Version": __version__}

        try:
            res = requests.post(self.url + '/authorize', headers=headers, json=user)
            if res.status_code == 409:
                raise Exception("Unsupported Qatalyst client, please update the client")
            return res.json()
        except requests.HTTPError as e:
            # TODO: DY, check error
            raise e

    def get_config(self, path=None):
        if path is not None:
            path = os.path.expanduser(path)
            try:
                with open(path, 'r') as fh:
                    conf = yaml.safe_load(fh)
            except FileNotFoundError as e:
                raise e
        else:
            for pth in self.CONF_PATHS:
                # Logic: if the conf file exists and we successfully read it in then
                # we drop through to 'else' and break out of the loop. If 'pth' doesn't exist
                # then continue through path options. If yaml cannot load it, then throw this
                # as a legitimate error.
                try:
                    with open(os.path.expanduser(pth), 'r') as fh:
                        conf = yaml.safe_load(fh)
                # keep looking in CONF_PATHS
                except FileNotFoundError:
                    continue
                except yaml.YAMLError as e:
                    raise e
                else:
                    break
            else:
                locs = ', '.join(['{}'.format(os.path.expanduser(f)) for f in self.CONF_PATHS])
                raise FileNotFoundError('Configuration file not found the following expected locations: {}'.format(locs))
        return conf

    def set_attributes(self):
        """
        Setting attributes in this way is a little awkward looking, but it allows the user to override the values in
        the .qci.conf file by passing in args if desired.
        """
        self.username = self.username if self.username is not None else self.conf.get('username')
        self.password = self.password if self.password is not None else self.conf.get('password')
        self.access_token = self.access_token if self.access_token is not None else self.conf.get('access_token')

    def check_status(self, res: requests.Response) -> Status:
        stat = parse_status(res)
        return stat

    def increment_delay(self):
        """
        Increase the polling delay until we reach 60 seconds between checks. Then check back every 60 seconds.

        :return: None
        """
        if self.delay < self.max_delay:
            self.delay += self.delay_incr
        else:
            self.delay = self.max_delay

    def get_token(self) -> Union[dict, str]:
        if self.username or self.access_token:
            return self.__authenticate()
        else:
            return {'access_token': ''}

    def create_callback(self, enc) -> Callable:
        encoder_len = enc.len
        # get a starting time and return an instance of the TicToc class
        tic = TicToc()

        def callback(monitor, bar_length=20):
            # mean bytes per second and estimated time remaining
            # tic.toc() takes latest time and subtracts start time
            mean_bps = monitor.bytes_read / tic.toc()
            est_remaining = 'Est. remaining (sec): {}'.format(round((encoder_len - monitor.bytes_read) / mean_bps, 1))
            # Calculate fraction of upload to completed and redo the progress bar
            fractional_progress = round(monitor.bytes_read / encoder_len, 2)
            progress = round(100.0 * fractional_progress, 1)
            tick_len = int(round(bar_length * fractional_progress))
            bar = '=' * tick_len + '-' * (bar_length - tick_len)
            # stdout stays on the same line, and \r moves the cursor back to the start
            sys.stdout.write('\rUpload progress [{}] | {}% | {}'.format(bar, progress, est_remaining))
            sys.stdout.flush()

        return callback

    def post_request(self,
                     data: dict,
                     token: dict,
                     timeout=21600) -> None:
        """
        Post a request to the API endpoint at self.post_endpoint.

        :param data: dict, data package
        :param token: dict, contains {'access_token': access_token}
        :param timeout: int, length of time to wait for a job creation response. In seconds.
        :return: None
        """
        with requests.Session() as session:
            enc = encoder.MultipartEncoder(fields=data)
            callback = self.create_callback(enc)
            monitor = encoder.MultipartEncoderMonitor(enc, callback)
            headers = {'Authorization': 'Bearer ' + token['access_token'], "Content-Type": monitor.content_type, "Qatalyst-Version": __version__}
            resp = session.post(self.url + self.post_endpoint, timeout=timeout, headers=headers, data=monitor)

            resp.raise_for_status()

            if resp.status_code == 409:
                raise requests.HTTPError("Unsupported Qatalyst client, please update the client")

            # Make sure the post confirm that the problem was created (== 201)
            if resp.status_code not in [200, 201]:
                raise requests.HTTPError("Job not successfully created.")

            # Report JobId to the user
            self.JobId = resp.json()['JobID']

            # The job is asynchronous. User can check status using the JobId
            sys.stdout.write('\nJob started with JobID: {}.\n'.format(self.JobId))

    def get_status_api(self, token: dict) -> requests.Response:
        return requests.get(self.url + self.status_endpoint.format(self.JobId),
                            headers={'Authorization': 'Bearer ' + token['access_token'], "Qatalyst-Version": __version__})

    def report_status_to_user(self, status) -> None:
        if status.status is StatusCodes.complete:
            print('\nProblem COMPLETE, returning solution.\n')
        elif status.status == StatusCodes.error:
            print('\nEncountered ERROR, check traceback.\n')
        else:
            now = dt.now().ctime()
            # new message to write
            if not self.status_message_written:
                sys.stdout.write(f'{self.STATUS_MESSAGE.format(now)}\n')
                self.status_message_written = True
            # an updated timestamp --> new status
            if self.status_time is None or status.timestamp > self.status_time:
                self.status_time = status.timestamp
                if status.message:
                    sys.stdout.write(f'Update: {status.message}\n')
            print(f"{dt.now().ctime()} | Checking again in {self.delay} seconds...", end='\r', flush=True)

    def poll_status(self, token: dict) -> Status:
        """
        Check status of JobId at increasing intervals. Starts at Default is adding 2 seconds after each check, until
        max_delay is reached (default = 60 sec)

        :param token: dict, {'access_token', access_token}
        :return: None
        """
        status = Status(StatusCodes.processing, message='', timestamp=str(dt.now()))
        while status.status is StatusCodes.processing:
            time.sleep(self.delay)
            res = self.get_status_api(token)
            res.raise_for_status()
            self.increment_delay()
            status = self.check_status(res)
            self.report_status_to_user(status)
        else:
            return status

    def check_braket_status(self, device_name: str, models: str, token: dict):
        """
        :param device_name: str, name of device for lookup purposes on AWS
        :param models: str, list of models assigned to device name
        :param token: dict, {'access_token', access_token}

        :return: dict
        """
        headers = {'Authorization': 'Bearer ' + token['access_token'], "Qatalyst-Version": __version__}
        data = json.dumps({'device_name': device_name, 'models': ','.join(models)})
        resp = requests.post(self.braketcheck_url + self.braketcheck_endpoint, headers=headers, data=data)

        # Try letting requests deal with the dictionary itself. This seems to behave
        # differently depending on which system the API is running on. Flask issue or requests quirk??
        if resp.status_code == 500:
            try:
                data = {'device_name': device_name, 'models': ','.join(models)}
                resp = requests.post(self.braketcheck_url + self.braketcheck_endpoint, headers=headers, data=data)
            except Exception as e:
                raise e

        # Carefully handle response object.
        try:
            resp = json.loads(resp.json())
        except json.JSONDecodeError:
            resp = resp.json()
        # something that's not a decoding error
        except (ValueError, TypeError) as e:
            print(f"Content of response: {resp.content}.")
            raise e
        return resp

    def sendRequest(self, data, large_data=False, timeout=21600) -> Any:
        """
        Send a request to the web service
        :param data: dict, contains 'metadata', 'params', and 'data'
        :param large_data: bool, toggle info message if the data is large.
        :param timeout: int, seconds to wait until giving up on posting to the API # TODO: do we still need this?
        :return: JSON response from server
        """
        if large_data:
            print("Data may take a moment to transfer to the server... ")
        token = self.get_token()
        self.post_request(data, token, timeout)
        trying= True
        threw_exception= False
        while (trying):        # handle possible connection loss
            try:            
                status = self.poll_status(token)
                trying= False
                if (threw_exception):
                    print(f"{dt.now().ctime()} | Reconnected Successsfully!                               ", end='\r', flush=True)
            except:
                print(f"{dt.now().ctime()} | Possible connection error                                ", end='\r', flush=True)
                threw_exception= True
                time.sleep(2)
        # complete, error = self.poll_status(token)
        if status.status is StatusCodes.error:
            # go get the final status so we can send it to the user
            raise ValueError("Failed with the following error: {}".format(status.message))
        else:
            # get the completed result, or error if there is one
            res = requests.get(self.url + self.result_endpoint.format(self.JobId),
                               headers={'Authorization': 'Bearer ' + token['access_token'], "Qatalyst-Version": __version__})

            try:
                assert res.status_code == 200
                return json.loads(decodeResponse(res.text))
            except AssertionError:
                print("Failed Response: status_code = {}\n".format(res.status_code), file=sys.stderr)


class ClientService(HTTPClient):

    BRAKET_ONLINE = 'ONLINE'
    BRAKET_OFFLINE = 'OFFLINE'

    PROBLEM_TYPES = ['qubo', 'constraint_problem', 'graph', 'lagrange_opt']

    DEFAULT_OPTIMIZER = 'cobyla'
    DEFAULT_ALGORITHM = 'vqe'
    CLASSICAL_SAMPLERS = ['csample']
    DEFAULT_OPTIMIZER_PARAMS = {'maxiter': 5}
    DEFAULT_NUM_SHOTS = 100
    DEFAULT_NUM_READS = 100
    DEFAULT_CIRCUIT_DEPTH = 2
    DEFAULT_LAGRANGE_MAX_DEPTH = 5
    OPTIMIZER_PARAMS = {'cobyla': DEFAULT_OPTIMIZER_PARAMS}
    HYBRID_ALGORITHMS = ['qaoa', 'vqe']

    DATA_OBJ_FNAME = 'data_obj.npz'
    DATA_CON_FNAME = 'data_con.npz'
    METADATA_FNAME = 'metadata.txt'
    PARAMS_NAME = 'params.txt'

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 access_token: str = None,
                 sampler: str = None,
                 configuration: str = 'default',
                 conf_path: str = None,
                 url: str = 'https://api.qci-prod.com',
                 braket_url: Optional[str] = None,
                 optimizer: str = None,
                 optimizer_params: dict = None,
                 algorithm: str = None):

        """
        Handles specific data processing for input, as well as communicating with the HTTPClient for authorization and
        sending requests to the API.

        Requires a username and password, or a username and access_token in order to complete authorization

        :param username: str
        :param password: str
        :param access_token: str
        :param sampler: str, which sampler to use. Current list is ['csample'].
        :param configuration: str, configuration name, in case the config file contains multiples
        :param conf_path: str, optional path to local configuration file. By default, HttpClient will check in
            these locations: ('~/.qci.conf', '~/.qci/qci.conf').
        :param url: str, Portal-API server. Default = 'https://api.qci-prod.com'
        :param optimizer: str, Classical optimizer to use in a quantum-classical hybrid algorithm.
        :param optimizer_params: dict, parameters to pass to the optimizer.
        :param algorithm: str, hybrid algorithm used for solving a QUBO. One of 'qaoa' or 'vqe'.
        """
        super().__init__(username, password, access_token, configuration, conf_path, url, braket_url)
        self.samplers = load_available_samplers()
        # handle backards compatibility with sampler='csample' for version < 2.0.6
        if sampler == 'csample':
            self.sampler = 'csample'
        # default to Advantage if unspecified
        elif sampler == 'braket_dwave':
            self.sampler = 'braket_dwave_advantage'
        else:
            self.sampler = sampler or self.conf.get('sampler', 'csample')
        self.algorithm = None
        self.optimizer = None
        self.optimizer_params = None

        # Braket-specific attributes
        self._arn = None
        self._device: Optional[AwsDeviceClient] = None

        # Make sure the 'target_name' is in the list of available samplers
        assert self.sampler in set(self.samplers['target_name']), \
            f"Sampler must be one of {set(self.samplers['target_name'].to_list())}."

        # If we have a valid hybrid algorithm and ask for a compatible solver, then set the optimizer and params
        if self.sampler in set(self.samplers[self.samplers['hybrid']]['target_name']):

            if algorithm:
                self.algorithm = algorithm.lower()
            else:
                self.algorithm = self.DEFAULT_ALGORITHM

            if self.algorithm in self.HYBRID_ALGORITHMS:
                self.optimizer = optimizer or self.DEFAULT_OPTIMIZER
                self.optimizer_params = optimizer_params or \
                    self.OPTIMIZER_PARAMS.get(self.DEFAULT_OPTIMIZER, self.DEFAULT_OPTIMIZER_PARAMS)

                # The sampler and algorithm are correct for a hybrid algorithm, and the user passed in optimizer and
                # param args.
                # Now check to make sure these are legit. We need to parse the output of scipy's show_method.
                # Make sure that optimizer is in our available algorithms
                self.__check_optimizer()
                # Make sure that the optimizer params are correctly type
                self.__check_optimizer_params()

            # If user sends in an unrecognized algorithm, throw an exception
            else:
                raise ValueError(f"Sampler ({self.sampler}) and algorithm ({self.algorithm}) incompatible. "
                                 f"Make sure that the sampler is compatible with hybrid (variational) algorithms.")

            if self.sampler.startswith('braket'):
                self._set_braket_device()
                self._set_arn()

        # select quantum computer that is not for hybrid/variational algorithms. Eg., annealer like D-Wave.
        elif self.sampler in set(self.samplers[self.samplers['quantum'] & ~self.samplers['hybrid']]['target_name']):
            if algorithm:
                warn(f"Annealing sampler {self.sampler} does not utilize an algorithm argument. "
                     f"You passed {algorithm}", UserWarning)
            elif optimizer:
                warn(f"Annealing sampler {self.sampler} does not utilize an optimizer argument. "
                     f"You passed '{optimizer}'", UserWarning)

            if self.sampler.startswith('braket'):
                self._set_braket_device()
                self._set_arn()

        # We've fallen through  all quantum and hybrid options
        else:
            self.sampler = 'csample'

    @property
    def arn(self):
        return self._arn

    @arn.setter
    def arn(self, value):
        self._arn = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    def __check_optimizer(self):
        """Make sure that optimizer is in our available algorithms"""
        assert isinstance(self.optimizer, str), "Parameter 'optimizer' must be of type str."
        if self.sampler.startswith('braket'):
            if self.optimizer.lower() not in get_scipy_minimize_methods():
                raise ValueError(f"Unknown optimizer. Parameter 'optimizer' must be one of "
                                 f"{get_scipy_minimize_methods()}")
        return True

    def __check_optimizer_params(self):
        assert isinstance(self.optimizer_params, dict), "Parameter 'optimizer_params' must be of type dictionary."
        return True

    def _check_sampler_type_is_qpu(self) -> bool:
        return self.sampler in set(self.samplers[self.samplers['quantum']]['target_name'])

    def _check_optimizer_has_params(self) -> bool:
        return self.optimizer is not None or self.optimizer_params is not None

    def get_device_and_models(self):
        # we only need one device name, the rest are repeats
        device_names = self.samplers[self.samplers['target_name'] == self.sampler]['device'].tolist()[0]
        models = self.samplers[self.samplers['target_name'] == self.sampler]['model'].tolist()
        return device_names, models

    def _set_braket_device(self):
        device_name, models = self.get_device_and_models()
        token = self.get_token()
        resp = self.check_braket_status(device_name, models, token)
        self.device = AwsDeviceClient.from_braket_check(resp)

        print(f"Set quantum device to {self.device.name}")
        assert self.device.status == self.BRAKET_ONLINE, f"No available devices for {self.sampler} sampler type."

    def confirm_qpu_execution(self, text):
        capture = input(text)
        if capture == 'n' or capture == 'N':
            print("Exiting...")
            sys.exit(0)
        else:
            print(f"You entered '{capture}'. Continuing...")

    def _set_arn(self):
        if not self.device:
            raise DeviceUnreachableException(f"There are no available devices for {self.sampler} sampler type.")
        self.arn = self.device.arn

    def is_quantum(self):
        return self._check_sampler_type_is_qpu() or self.is_hybrid()

    def is_hybrid(self):
        return self.sampler in set(self.samplers[self.samplers['hybrid']]['target_name'])

    def _check_size(self, obj) -> bool:
        if not self._check_problem_size(obj):
            qubit_count = self.samplers[self.samplers['model'] == self.device.name]['max_size'].item()
            raise ValueError(f"Problem size exceeds the number of qubits or variables available "
                             f"for the QPU, {self.sampler}. Maximum number of qubits = {qubit_count}")
        # make sure if a DW problem is solving a complete graph that it
        elif 'dwave' in self.sampler:
            # returns True if nqubits < max, raises value error otherwise
            print("Checking basic size thresholds for D-Wave QPUs...")
            return check_dwave_size(obj, self.device)
        else:
            return True

    def _check_problem_size(self, qubo: Union[dict, sp.spmatrix, np.ndarray]) -> bool:
        """
        Confirm whether sampler is a QPU and if so, whether size of qubo aligns
        with the number of qubits provided bythe QPU.

        :param qubo:  Union[dict, sp.spmatrix, np.ndarray]

        :return: bool
        """
        if self.device is not None:
            qubit_count = self.samplers[self.samplers['model'] == self.device.name]['max_size'].item()
        else:
            qubit_count = self.samplers[self.samplers['target_name'] == self.sampler]['max_size'].item()
        if isinstance(qubo, dict):
            n_qubits = len([key for key in qubo.keys() if key[0] == key[1]])
            return n_qubits <= qubit_count
        else:
            return qubo.shape[0] <= qubit_count

    def _get_data_type(self, data) -> str:
        if isinstance(data, dict):
            return 'dict'
        elif isinstance(data, np.ndarray):
            return 'dense'
        elif isinstance(data, nx.Graph):
            return 'graph'
        elif isinstance(data, sp.spmatrix):
            return 'sparse'
        else:
            raise TypeError('Unknown data type {}. Must pass dictionary, np.ndarray, '
                            'scipy sparse matrix, or NetworkX Graph'.format(type(data)))

    def get_available_samplers(self) -> None:
        """
        Provide a list of the available samplers.

        :return: List of samplers available to users.
        """
        print_available_samplers()

    def process_metadata(self, problem_type, data) -> dict:
        """
        Formulate the metadata dictionary based on input parameters and user input. We need to inform the backend
        services what type of problem we want to solve, the type of data sent, what sampler to use, and (optionally)
        the shape of the data so an encoded matrix can be reconstructed on the server side.

        :param problem_type: str, one of 'qubo', 'constraint_problem', 'lagrange_opt', 'graph'
        :param data:

        :return: dict with {problem_type, data_type, sampler, [shape]}
        """
        assert problem_type in self.PROBLEM_TYPES, \
            ValueError('Problem type must be one of {}'.format(self.PROBLEM_TYPES))
        m = {'problem_type': problem_type,
             'data_type': self._get_data_type(data),
             'sampler': self.sampler}
        if isinstance(data, np.ndarray) or isinstance(data, sp.spmatrix):
            m['shape'] = data.shape
        return encode_data(m)

    def process_params(self, params):

        quantum = self.sampler != 'csample'
        if not param_check(params, quantum=quantum):
            raise ValueError(f"Unknown parameter error. Please check kwargs. {params}")
        return encode_data(params)

    @staticmethod
    def process_data(data: Union[dict, np.ndarray, sp.spmatrix, nx.Graph]) -> Union[bytes, dict]:
        """
        Process the input data by encoding it.

        :param data: dict, np.ndarray, sp.spmatrix, nx.Graph,

        :return: Union[bytes, dict]. Encoded data, either dict with {'data': base64 encoded data object} or
            byte string encoding a NPTZ file obj.
        """
        if isinstance(data, dict):
            return {'data': encode_data(data)}
        elif isinstance(data, nx.Graph):
            return encode_graph(data)
        elif isinstance(data, np.ndarray):
            # byte string of a savez_compressed array
            return encode_ndarray(data)
        elif isinstance(data, sp.spmatrix):
            data = sp.coo_matrix(data, dtype=np.float)
            # byte string of a savez_compressed array
            return encode_sparse_array(data)
        else:
            raise TypeError("Input data must be dictionary, np.ndarray, or scipy.spmatrix")


class DeviceUnreachableException(Exception):
    """
    Raise when a device is offline.
    """
    pass
