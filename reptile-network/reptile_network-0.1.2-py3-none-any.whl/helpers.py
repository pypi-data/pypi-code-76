import sys
from .constants import VERSION


def check_version(requested: str):
    cur_version = VERSION.split('.')
    requested_version = requested.split('.')

    if cur_version[0] != requested_version[0]:
        return False
    elif cur_version[1] != requested_version[1]:
        print('\033[33mWARN: Your minor version can be incompatible with the requested version\033[0m')
        
    return True


def get_setup_param(param_name: str, *other_params):
    ''' Возвращает параметр запуска '''

    for name in [param_name, *other_params]:
        if len(name) > 1:
            param = f'--{name}'
        else:
            param = f'-{name}'

        if param in sys.argv:
            index = sys.argv.index(param)
            if len(sys.argv) > index:
                return sys.argv[index + 1]

    return None
