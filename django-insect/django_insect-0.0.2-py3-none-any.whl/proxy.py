import socket
import threading
import time
import uuid

import etcd3
from django.conf import settings

"""
    For server
"""
SERVER_NAME = 'INSECT_SERVER_NAME'
SERVER_URL = 'INSECT_SERVER_URL'
SERVER_PORT = 'INSECT_SERVER_PORT'
"""
    For etcd
"""
ETCD_URL = 'INSECT_ETCD_URL'
ETCD_PORT = 'INSECT_ETCD_PORT'
ETCD_USER = 'INSECT_ETCD_USER'
ETCD_PASSWORD = 'INSECT_ETCD_PASSWORD'

ETCD_LEASE_TTL = 'INSECT_ETCD_LEASE_TTL'


class EtcdProxy:
    etcd_client = None

    def __init__(self):
        self.server_key = ''

        self.server_name = getattr(settings, SERVER_NAME, None)
        self.server_url = getattr(settings, SERVER_URL, None)
        self.server_port = getattr(settings, SERVER_PORT, None)

        self.etcd_url = getattr(settings, ETCD_URL, '0.0.0.0')
        self.etcd_port = getattr(settings, ETCD_PORT, 2379)
        self.etcd_user = getattr(settings, ETCD_USER, None)
        self.etcd_password = getattr(settings, ETCD_PASSWORD, None)

        self.etcd_lease_ttl = getattr(settings, ETCD_LEASE_TTL, 10)

    def run(self):
        if self.server_name:
            etcd_thread = threading.Thread(target=self.register)
            etcd_thread.start()

    def register(self):
        ip = self.server_url
        if not ip:
            ip = socket.gethostbyname_ex(socket.gethostname())[-1][-1]  # IP
        port = self.server_port  # Port
        url = str(ip)  # Url
        if port:
            url = url + ':' + str(port)
        self.put_with_lease(value=url, ttl=self.etcd_lease_ttl)

    @property
    def client(self):
        if self.etcd_client is None:
            self.etcd_client = etcd3.client(self.etcd_url,
                                            port=self.etcd_port, user=self.etcd_user, password=self.etcd_password)
        return self.etcd_client

    def get(self, key, **kwargs):
        return self.client.get(key, **kwargs)

    def put(self, key, value, lease=None, prev_kv=False):
        self.client.put(key, value, lease=lease, prev_kv=prev_kv)

    def put_with_lease(self, value, ttl=10, prev_kv=False):
        while True:
            lease = self.client.lease(ttl)
            key = self.server_name + '_' + str(uuid.uuid4())
            self.client.put(key, value, lease=lease, prev_kv=prev_kv)
            print('lease -', key, '-', ttl, 'sec')
            time.sleep(ttl)

    def delete(self, key, prev_kv=False, return_response=False):
        self.client.delete(key, prev_kv=prev_kv, return_response=return_response)

    def delete_prefix(self, prefix):
        return self.client.delete_prefix(prefix)
