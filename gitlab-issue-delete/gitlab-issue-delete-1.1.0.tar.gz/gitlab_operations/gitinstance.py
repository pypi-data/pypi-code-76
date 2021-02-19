import configparser
from pathlib import Path
import os


class GitInstance:
    """
    Remove GitLab issues in blul
    """

    def __init__(self):
        # get xdg user dirs
        _HOME = str(Path.home())
        _CONFIG = '.config'
        _XDG_CONFIG_DIR = os.path.join(_HOME, _CONFIG)
        _config_dir = 'gitlab'
        _config_file = 'config.ini'

        # default setting
        self._git_url = 'https://gitlab.com/'
        self._access_token = False

        _config_dir_path = os.path.join(_XDG_CONFIG_DIR, _config_dir)
        self._config_file_path = os.path.join(_config_dir_path, _config_file)
        self._test_config()

    def _test_config(self):
        path = Path(self._config_file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._get_config()

    def _get_config(self):
        if os.path.isfile(self._config_file_path):
            print('[-] config file exist')
            print('[-] URL:{}'.format(self.url))
            print('[-] ACCESS_TOKEN: {}'.format(self.token))
        else:
            print('[x] config file not found')
            self._default_config()

    def _default_config(self):
        config = configparser.ConfigParser()
        config['GitLab'] = {
            'url': self._git_url,
            'access_token': self._access_token
        }
        with open(self._config_file_path, 'w') as f:
            config.write(f)
        f.close()
        print('[-] user default config added')

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(self._config_file_path)
        git = config['GitLab']
        return git.get('url'), git.get('access_token')

    @property
    def url(self):
        url, _ = self._read_config()
        return url

    @property
    def token(self):
        _, token = self._read_config()
        return token
