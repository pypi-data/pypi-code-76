"""Configuration file (sth.cfg) handling"""
import configparser
import inspect

from pathlib import Path


def is_in_module(f):
    return len(list(Path(f).parent.glob('__init__.py')))


def cfgs_gen(p):
    yield from Path(p).glob('*.conf')
    yield from Path(p).glob('*.cfg')


def find_cfg(p, level=2):
    p = Path(p)
    cfgs = list(cfgs_gen(p))
    if len(cfgs) == 0:
        if is_in_module(p) and level > 0:
            return find_cfg(p.parent, level-1)
        else:
            return None
    else:
        return cfgs[0]


def read_config(_filepath='test.cfg') -> dict:
    filepath = Path(_filepath)
    parsed_conf = {}
    if not filepath.exists():
        return parsed_conf

    try:
        file_config = configparser.ConfigParser()
        file_config.read(filepath)
        if 'Clima' in file_config:
            parsed_conf = dict(file_config['Clima'])
        else:
            print('warning: config file found at {}, but it was missing section named [Clima]'.format(str(filepath)))
    except:
        print(f'warning: clima deducted {_filepath} to be a valid config file, but could not read it.')

    return parsed_conf

def get_config_path(_schema):
    """
    Resolve filepath for a config file, if one can be found.

    Args:
        _schema:

    Returns:
        Path of config file or None

    Examples of parsing patterns:
        {}                                  -> glob for any .cfg file at pwd
        {cwd: '../foo'}                     -> glob for any .cfg file using cwd
        {cwd: '/root/foo'}                  -> glob for any .cfg file using cwd
        {cwd: '../foo', CFG: 'my.cfg'}      -> select my.cfg at dir cwd
        {cwd: '/root/foo', CFG: 'my.cfg'}   -> select my.cfg at dir cwd
        {CFG: 'my.cfg'}                     -> select my.cfg at pwd
        {CFG: '/root/foo/my.cfg'}           -> select cfg using absolute path

    """
    # if hasattr cfg and absolute, use cfg
    cfg_filepath = Path(getattr(_schema, 'CFG', ''))
    if not cfg_filepath.is_absolute():
        # concate getattr cwd/'' getattr cfg/''
        cfg_filepath = Path(getattr(_schema, 'cwd', '')) / cfg_filepath
        if not cfg_filepath.is_file():
            cfg_filepath = find_cfg(cfg_filepath)

    return cfg_filepath
