from ml_platform_client.config import global_config
from ml_platform_client.dispatcher import register, set_config
from ml_platform_client.server import app
from ml_platform_client.server import set_preload_models
from example.basic.algorithms import MyAlgorithm, FakeAlgorithm

minio_host = '172.16.100.130:9000'
minio_access_key = '24WTCKX23M0MRI6BA72Y'
minio_secret_key = '6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX'
minio_secure = False
mysql_host = '172.16.100.130'
mysql_port = 3306
mysql_user = 'root'
mysql_password = 'password'

if __name__ == '__main__':
    global_config.minio_host = minio_host
    global_config.minio_access_key = minio_access_key
    global_config.minio_secret_key = minio_secret_key
    global_config.minio_secure = minio_secure

    global_config.mysql_host = mysql_host
    global_config.mysql_port = mysql_port
    global_config.mysql_user = mysql_user
    global_config.mysql_password = mysql_password

    register('my_alg', MyAlgorithm)
    register('fake_alg', FakeAlgorithm)
    set_preload_models('my_alg', ['pretrain_model_id1', 'pretrain_model_id2'])

    # checker.start()

    set_config(global_config)
    app.run()
