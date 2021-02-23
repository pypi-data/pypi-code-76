"""
Module for managing environment configuration.
"""
from copy import copy
import os
from pathlib import Path
import yaml
import git

from .exception import EnvironmentException

ENV_FILE_NAME = 'declair_env.yaml'

def _contains_nested_key(dict_, key):
    if len(key) > 1:
        if key[0] in dict_:
            try:
                return _contains_nested_key(dict_[key[0]], key[1:])
            except:
                return False
        else:
            return False
    else:
        if key[0] in dict_:
            # Make sure dict_ allows for key[0] to be an index
            # otherwise we might accidentally let the key[0] in dict_ allow
            # dict_ to be an e.g. string
            try:
                dict_[key[0]]
                return True
            except:
                return False
        else:
            return False

def _get_nested_key(dict_, key):
    if not _contains_nested_key(dict_, key):
        raise KeyError(key)
    if len(key) > 1:
        return _get_nested_key(dict_[key[0]], key[1:])
    else:
        return dict_[key[0]]

def _set_nested_key(dict_, key, value):
    if len(key) > 1:
        if key[0] not in dict_ or not hasattr(dict_[key[0]], '__setitem__'):
            dict_[key[0]] = {}
        _set_nested_key(dict_[key[0]], key[1:], value)
    else:
        if not hasattr(dict_, '__setitem__'):
            raise ValueError("Cannot set value of {} in {} since it's not a dict".format(
                key, dict_))
        dict_[key[0]] = value

class Environment:
    """Class for keeping track of environment envuration which can be
    scattered across multiple files.

    For each env entry, it also keeps its source as a string, e.g. file
    path of file from which it was retrieved.
    """
    def __init__(self, dict=None, source='__init__'):
        self._dict = dict if dict else {}
        self._source = {}
        for key, value in self._dict.items():
            self._source[key] = source

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)

    def get_source(self, key):
        return self._source[key]

    def get_dict(self):
        return copy(self._dict)

    def update_from_file(self, filepath):
        with open(filepath) as file_:
            dict_ = yaml.safe_load(file_.read())
        self.update_from_dict(dict_, 'file:{}'.format(filepath))

    def update_from_dict(self, dict_, source):
        for key, value in dict_.items():
            self.set(key, value, source)

    def set(self, key, value, source):
        self._dict[key] = value
        self._source[key] = source

    def dumps(self):
        """Return a yaml representation of contents of this Environment."""
        return yaml.dump(self._dict)

    def dump(self, path):
        """Inserts a yaml representation of convents of this Environment 
        into a file given its path.
        """
        with open(path, 'w') as file_:
            file_.write(self.dumps())

    def __contains__(self, key):
        return key in self._dict

    def contains_nested_key(self, key):
        return _contains_nested_key(self._dict, key)

    def get_nested_key(self, key):
        return _get_nested_key(self._dict, key)

    def set_nested_key(self, key, value, source):
        _set_nested_key(self._dict, key, value)
        self._source[key[0]] = source

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)
        else:
            return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value, '__setitem__')

    @classmethod
    def from_file(cls, path):
        env = cls()
        env.update_from_file(path)
        return env

    @classmethod
    def from_dict(cls, dict_):
        env = cls()
        env.update_from_dict(dict_, '__init__')
        return env

def _get_repo_env_candidate(path=None):
    try:
        repo_path = git.Repo(path, search_parent_directories=True).working_dir
        return Path(repo_path).joinpath(ENV_FILE_NAME)
    except git.InvalidGitRepositoryError:
        return None

def get_repo_env(path=None):
    candidate = _get_repo_env_candidate(path)
    if candidate is not None and Path(candidate).is_file():
        return Environment.from_file(_get_repo_env_candidate(path))

def _get_candidate_env_file_paths(path):
    # In reverse order of importance; first configs get overwritten by 
    # later configs
    path_obj = Path(path)
    candidate_paths = [
        _get_repo_env_candidate(path)
    ]
    if path_obj.name:
        candidate_paths += [path_obj.with_name(ENV_FILE_NAME)]
    candidate_paths += [path_obj.joinpath(ENV_FILE_NAME)]
    return candidate_paths

def get_path_env(path):
    env = Environment()
    for env_path in _get_candidate_env_file_paths(path):
        if env_path is not None and env_path.is_file():
            env.update_from_file(env_path)
    return env

def get_cwd_env():
    return get_path_env(os.getcwd())

