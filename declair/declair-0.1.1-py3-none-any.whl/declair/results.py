"""
Functions that help with storing experiment results.
"""
from tempfile import NamedTemporaryFile
from time import sleep

import pymongo
from sacred.observers import FileStorageObserver, MongoObserver

from .exception import InvalidConfigException, EnvironmentException

def _check_mongo_server(uri):
    try:
        pymongo.MongoClient(uri,
                            serverSelectionTimeoutMS=1000*5).server_info()
        return True
    except pymongo.errors.ConnectionFailure:
        return False

def _append_file_storage_observer(experiment, env):
    obs = env['observers']['file']
    if not 'path' in obs:
        raise InvalidConfigException('Environment config missing path for file')
    experiment.observers.append(FileStorageObserver(obs['path']))

def _append_mongo_observer(experiment, env,
                           connection_attempts=3,
                           connection_attempt_sleep_time=10):
    obs = env['observers']['mongo']
    if not 'url' in obs:
        raise InvalidConfigException('Environment config missing url for mongo')
    connected = False
    for _ in range(connection_attempts):
        if _check_mongo_server(obs['url']):
            connected = True
            break
        else:
            sleep(connection_attempt_sleep_time)
    if not connected:
        raise EnvironmentException(
            ("Failed to connect to MongoDB at {} as configured in {}. "
             "If you'd like to run without MongoDB, remove it from the config file").format(
                 obs['url'], env.get_source('observers')))
    experiment.observers.append(MongoObserver(obs['url']))

_ENV_TO_FUNC = {
    'file': _append_file_storage_observer,
    'mongo': _append_mongo_observer
}

def append_observers_to_experiment(experiment, env):
    """Adds observers to a Sacred experiment as defined in environment env."""
    _dict = env.get_dict()
    if 'observers' not in _dict:
        return
    obs = _dict['observers']
    for key in obs:
        if key in _ENV_TO_FUNC:
            _ENV_TO_FUNC[key](experiment, env)
        else:
            raise InvalidConfigException(
                'Unknown observer in config: {}'.format(key))

def add_artifact_string(run, string, artifact_name):
    """Adds a string as an artifact to a Sacred run or experiment."""
    with NamedTemporaryFile(mode='w') as tmp_file:
        tmp_file.write(string)
        tmp_file.flush()
        run.add_artifact(tmp_file.name, artifact_name)

def add_artifact_fig(run, fig, artifact_name):
    """Adds a matplotlib figure as an artifact to Sacred run or experiment."""
    with NamedTemporaryFile(mode='w', suffix='.png') as tmp_file:
        fig.savefig(tmp_file.name)
        run.add_artifact(tmp_file.name, artifact_name)
