#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from contextlib import contextmanager

import grpc
from aos_prov.communication.unit import api_iamanager_iamanager_pb2 as api_iam_manager
from aos_prov.communication.unit import api_iamanager_iamanager_pb2_grpc as api_iam_manager_grpc
from aos_prov.communication.utils.errors import BoardError
from aos_prov.communication.utils.unit_certificate import UnitCertificate
from colorama import Fore, Style


class UnitCommunication(object):
    def __init__(self, address: str = 'localhost:8089'):
        self.__unit_address = address

    @contextmanager
    def unit_stub(self, catch_inactive=False):
        try:
            with grpc.insecure_channel(self.__unit_address) as channel:
                stub = api_iam_manager_grpc.IAManagerStub(channel)
                yield stub

        except grpc.RpcError as e:
            if catch_inactive and \
                    not (e.code() == grpc.StatusCode.UNAVAILABLE.value and e.details() == 'Socket closed'):
                return

            print(f"{Fore.RED}FAILED! Error occurred: {Style.RESET_ALL}")
            print(f"{Fore.RED}{e.code()}: {e.details()}{Style.RESET_ALL}")
            raise BoardError()

    def get_system_info(self) -> (str, str):
        with self.unit_stub() as stub:
            print('Getting System Info...')
            response = stub.GetSystemInfo(api_iam_manager.google_dot_protobuf_dot_empty__pb2.Empty())
            print('System ID: ' + response.system_id)
            print('Model name: ' + response.board_model)
            return response.system_id, response.board_model

    def clear(self, certificate_type: str) -> None:
        with self.unit_stub() as stub:
            print('Clear certificate: ' + certificate_type)
            response = stub.Clear(api_iam_manager.ClearReq(type=certificate_type))
            return response

    def set_cert_owner(self, certificate_type: str, password: str) -> None:
        with self.unit_stub() as stub:
            print('Set owner: ' + certificate_type)
            response = stub.SetOwner(api_iam_manager.SetOwnerReq(type=certificate_type, password=password))
            return response

    def get_cert_types(self) -> [str]:
        with self.unit_stub() as stub:
            print('Getting certificate types to renew')
            response = stub.GetCertTypes(api_iam_manager.google_dot_protobuf_dot_empty__pb2.Empty())
            print('Will be renewed: ' + str(response.types))
            return response.types

    def create_keys(self, cert_type: str, password: str) -> UnitCertificate:
        with self.unit_stub() as stub:
            print('Generating key type:' + cert_type)
            response = stub.CreateKey(api_iam_manager.CreateKeyReq(type=cert_type, password=password))
            uc = UnitCertificate()
            uc.cert_type = response.type
            uc.csr = response.csr
            return uc

    def apply_certificate(self, unit_cert: UnitCertificate):
        with self.unit_stub() as stub:
            stub.ApplyCert(api_iam_manager.ApplyCertReq(type=unit_cert.cert_type, cert=unit_cert.certificate))

    def set_users(self, users: [str]):
        with self.unit_stub() as stub:
            stub.SetUsers(api_iam_manager.SetUsersReq(users=users))

    def finish_provisioning(self):
        with self.unit_stub(True) as stub:
            stub.FinishProvisioning(api_iam_manager.google_dot_protobuf_dot_empty__pb2.Empty())
