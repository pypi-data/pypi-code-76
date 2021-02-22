import grpc
import time
import random
import urllib.request
import platform
import tempfile
import os
import stat
import logging
import subprocess

from veriservice import veriservice_pb2 as pb
from veriservice import veriservice_pb2_grpc as pb_grpc

__version__ = "0.0.32"

logging.basicConfig(level=logging.DEBUG)

BASE_PATH = "https://github.com/bgokden/veri/releases/download/v0.0.43"

def get_url(base_path = BASE_PATH):
    platform_type = platform.system().lower()
    url_map = {
        "darwin": "veri-darwin-amd64",
        "windows": "veri-windows-amd64",
        "linux": "veri-linux-amd64",
    }
    return base_path+"/"+url_map.get(platform_type, url_map.get("linux"))


def init_service(service: str, dirpath: str = "", base_path: str = BASE_PATH, discover: str = None):
    host, port = service.split(":")
    if host == "localhost":
        pid_file_path = os.path.join(dirpath, service + ".pid")
        logging.debug(f"Using pid file : {pid_file_path}")
        if os.path.isfile(pid_file_path):
            pid = open(pid_file_path, 'r').read()
            logging.debug(f"Service already exists with pid {pid}, if not remove: {pid_file_path}")
        else:
            if dirpath == "":
                dirpath = tempfile.mkdtemp()
            os.makedirs(dirpath, exist_ok=True)
            source_url = get_url(base_path)
            download_path = os.path.join(dirpath, 'veri')
            if not os.path.isfile(download_path):
                urllib.request.urlretrieve(source_url, download_path)
            st = os.stat(download_path)
            os.chmod(download_path, st.st_mode | stat.S_IEXEC)
            data_path = os.path.join(dirpath, 'data')
            os.makedirs(data_path, exist_ok=True)
            args = [str(download_path), "serve", "-p", str(port), "-d", data_path]
            if discover is not None:
                args.extend(["-s", discover])
            logging.debug(f"Running with args: {args}")
            FNULL = open(os.devnull, 'w')
            popen_output = subprocess.Popen(args, stdout=FNULL, stderr=subprocess.STDOUT)
            pid = popen_output.pid
            with open(pid_file_path, 'w') as f:
                f.write(str(pid))
    else:
        logging.debug("Service is not localhost")



class GrpcClientWrapper:
    def __init__(self, service, client):
        self.service = service
        self.client = client

    def get_service(self):
        return self.service

    def get_client(self):
        return self.client


class VeriClient:
    def __init__(self, services, data_name):
        self.services = services.split(",") # eg.: 'localhost:50051, localhost2:50051'
        self.clients = {}
        self.data_name = data_name

    def __get_client(self):
        service = random.choice(self.services)
        if service in self.clients:
            return self.clients[service]
        channel = grpc.insecure_channel(service)
        self.clients[service] = GrpcClientWrapper(service, pb_grpc.VeriServiceStub(channel))
        return self.clients[service]

    def __refresh_client(self, service):
        channel = grpc.insecure_channel(service)
        self.clients[service] = GrpcClientWrapper(service, pb_grpc.VeriServiceStub(channel))
        time.sleep(0.500)


    def create_data_if_not_exists(self, **kwargs):
        request = pb.DataConfig(
            name=self.data_name,
            version=kwargs.get("version", 1),
            targetN=kwargs.get("target_n", 10000),
            targetUtilization=kwargs.get("target_utilization", 0.5),
            noTarget=kwargs.get("no_target", False),
        )
        response = None
        retry = kwargs.get("retry", 5)
        while retry >= 0:
            client_wrapper = None
            try:
                client_wrapper = self.__get_client()
                response = client_wrapper.get_client().CreateDataIfNotExists(request)
                if response != None:
                    return response
            except grpc.RpcError as e:  # there should be connection problem
                if client_wrapper is not None:
                    self.__refresh_client(client_wrapper.get_service())
            except Exception as e:
                time.sleep(0.200)
            retry -= 1
        return response


    def insert(self,
              vector,
              label,
              **kwargs
              ):
        retry = kwargs.get("retry", 5)
        request = pb.InsertionRequest(
            config=pb.InsertConfig(
                tTL=kwargs.get("ttl", None)
            ),
            datum=pb.Datum(
                key=pb.DatumKey(
                    feature=vector,
                    groupLabel=kwargs.get("group_label", None),
                    size1=kwargs.get("size1", 1),
                    size2=kwargs.get("size2", 0),
                    dim1=kwargs.get("dim1", len(vector)),
                    dim2=kwargs.get("dim2", 0),
                ),
                value=pb.DatumValue(
                    version=kwargs.get("version", None),
                    label=label,
                ),
            ),
            dataName=self.data_name,
        )
        response = None
        while retry >= 0:
            client_wrapper = None
            try:
                client_wrapper = self.__get_client()
                response = client_wrapper.get_client().Insert(request)
                if response.code == 0:
                    return response
            except grpc.RpcError as e:  # there should be connection problem
                logging.debug(f"Grpc Error: {e}")
                if client_wrapper is not None:
                    self.__refresh_client(client_wrapper.get_service())
            except Exception as e:
                logging.debug(f"Error: {e}")
                time.sleep(0.200)
            retry -= 1
        return response

    def search(self, vectors, **kwargs):
        retry = kwargs.get("retry", 5)
        datum_list = []
        for vector in vectors:
            datum_list.append(
                pb.Datum(
                    key=pb.DatumKey(
                        feature=vector,
                        groupLabel=kwargs.get("group_label", None),
                        size1=kwargs.get("size1", 1),
                        size2=kwargs.get("size2", 0),
                        dim1=kwargs.get("dim1", len(vector)),
                        dim2=kwargs.get("dim2", 0),
                    ),
                )
            )
        context_list = []
        for vector in kwargs.get("context_vectors", []):
            context_list.append(
                pb.Datum(
                    key=pb.DatumKey(
                        feature=vector,
                        groupLabel=kwargs.get("group_label", None),
                        size1=kwargs.get("size1", 1),
                        size2=kwargs.get("size2", 0),
                        dim1=kwargs.get("dim1", len(vector)),
                        dim2=kwargs.get("dim2", 0),
                    ),
                )
            )
        request = pb.SearchRequest(
            config=pb.SearchConfig(
                dataName=self.data_name,
                scoreFuncName=kwargs.get("score_func_name", "VectorDistance"),
                higherIsBetter=kwargs.get("higher_is_better", False),
                timestamp=kwargs.get("timestamp", 0),
                timeout=kwargs.get("timeout", 1000),
                limit=kwargs.get("limit", 1000),
                cacheDuration=kwargs.get("cache_duration", 60),
                groupLimit=kwargs.get("group_limit", 0),
                resultLimit=kwargs.get("result_limit", 0),
                filters=kwargs.get("filters", []),
                groupFilters=kwargs.get("group_filters", []),
            ),
            datum=datum_list,
            context=pb.SearchContext(
                datum=context_list,
                prioritize=kwargs.get("prioritize_context", 0),
            )
        )
        response = None
        while retry >= 0:
            client_wrapper = None
            try:
                client_wrapper = self.__get_client()
                response = client_wrapper.get_client().SearchStream(request)
                return response
            except grpc.RpcError as e: # there should be connection problem
                logging.debug(f"Grpc Error: {e}")
                if client_wrapper is not None:
                    self.__refresh_client(client_wrapper.get_service())
            except Exception as e:
                logging.debug(f"Error: {e}")
                time.sleep(0.200)
            retry -= 1
        return response

    def data(self, **kwargs):
        retry = kwargs.get("retry", 5)
        request = pb.GetDataRequest(
            name = self.data_name,
        )
        response = None
        while retry >= 0:
            client_wrapper = None
            try:
                client_wrapper = self.__get_client()
                response = client_wrapper.get_client().DataStream(request)
                return response
            except grpc.RpcError as e: # there should be connection problem
                logging.debug(f"Grpc Error: {e}")
                if client_wrapper is not None:
                    self.__refresh_client(client_wrapper.get_service())
            except Exception as e:
                logging.debug(f"Error: {e}")
                time.sleep(0.200)
            retry -= 1
        return response