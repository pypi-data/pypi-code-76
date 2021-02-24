import os


class GlobalConfig:
    def __init__(self):
        self.server_url = None
        self.minio_host = None
        self.minio_access_key = None
        self.minio_secret_key = None
        self.minio_secure = None
        self.mysql_host = None
        self.mysql_port = None
        self.mysql_user = None
        self.mysql_password = None
        self.num_worker = int(os.environ.get('MLP_CLIENT_WORKER', 5))
        self.num_thread = int(os.environ.get('MLP_CLIENT_THREAD', 10))


global_config = GlobalConfig()
