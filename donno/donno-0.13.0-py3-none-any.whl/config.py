import json
from pathlib import Path
from typing import Tuple

CONF_PATH = Path.home() / '.config/donno/config.json'
BASE_DIR = Path.home() / ".donno"
DEFAULT_CONF = {
    'app_home': str(BASE_DIR),
    'repo': str(BASE_DIR / 'repo'),
    'editor': 'nvim',
    'viewer': 'nvim -R',
    'default_notebook': '/Diary',
    'logging_level': 'info',
    'editor_envs': {
        'XDG_CONFIG_HOME': '$HOME/.config',
    },
}

if not CONF_PATH.exists():
    CONF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONF_PATH, 'w') as f:
        json.dump(DEFAULT_CONF, f, indent=4)


def get_attr(attr_name: Tuple = ()):
    with open(CONF_PATH) as f:
        configs = json.load(f)
    if len(attr_name) == 0:
        return configs
    else:
        return configs[attr_name[0]]


def set_attr(attr_name: Tuple) -> str:
    with open(CONF_PATH) as f:
        configs = json.load(f)
    if len(attr_name) < 2:
        return "Add attribute name and value"
    conf_key = attr_name[0]
    conf_value = attr_name[1]
    if conf_key.startswith('editor_envs.'):
        env_name = conf_key.split('editor_envs.')[1]
        configs['editor_envs'][env_name] = conf_value
    else:
        configs[attr_name[0]] = attr_name[1]
    with open(CONF_PATH, 'w') as f:
        json.dump(configs, f, indent=4)
    return configs


def restore() -> str:
    CONF_PATH.unlink(missing_ok=True)
    return DEFAULT_CONF
