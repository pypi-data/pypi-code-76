import socket
import threading
import time
import uuid

import etcd3
from flask import _app_ctx_stack

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


class EtcdProxy:

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.server_name = self.app.config.get(SERVER_NAME, None)
            self.server_url = self.app.config.get(SERVER_URL, None)
            self.server_port = self.app.config.get(SERVER_PORT, None)

            self.etcd_url = self.app.config.get(ETCD_URL, '0.0.0.0')
            self.etcd_port = self.app.config.get(ETCD_PORT, 2379)
            self.etcd_user = self.app.config.get(ETCD_USER, None)
            self.etcd_password = self.app.config.get(ETCD_PASSWORD, None)

            self.server_key = ''

            self.init_app(app)

    def init_app(self, app):

        if self.server_name:
            self.server_key = self.server_name + '_' + str(uuid.uuid4())

            # register to etcd
            etcd_thread = threading.Thread(target=self.register)
            etcd_thread.start()

            app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        self.delete(self.server_key)

    def register(self):
        ip = self.server_url  # IP
        if not ip:
            ip = socket.gethostbyname_ex(socket.gethostname())[-1][-1]

        port = self.server_port  # Port

        url = str(ip)  # Url
        if port:
            url = url + ':' + str(port)
        self.put_with_lease(self.server_key, value=url, ttl=10)

    @property
    def client(self):
        ctx = _app_ctx_stack.top
        if ctx:
            if not hasattr(ctx, 'etcd'):
                ctx.etcd = etcd3.client(self.etcd_url,
                                        port=self.etcd_port, user=self.etcd_user, password=self.etcd_password)
            return ctx.etcd
        else:
            return etcd3.client(self.etcd_url,
                                port=self.etcd_port, user=self.etcd_user, password=self.etcd_password)

    def get(self, key, **kwargs):
        return self.client.get(key, **kwargs)

    def put(self, key, value, lease=None, prev_kv=False):
        self.client.put(key, value, lease=lease, prev_kv=prev_kv)

    def put_with_lease(self, key, value, ttl=60, prev_kv=False):
        while True:
            lease = self.client.lease(ttl)
            self.client.put(key, value, lease, prev_kv=prev_kv)
            print('lease -', key, '-', ttl, 'sec')
            time.sleep(ttl - 1)
            self.client.revoke_lease(lease.id)

    def delete(self, key, prev_kv=False, return_response=False):
        self.client.delete(key, prev_kv=prev_kv, return_response=return_response)

    def delete_prefix(self, prefix):
        return self.client.delete_prefix(prefix)
