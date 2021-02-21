from itertools import groupby
from datetime import datetime
from yaml import load, SafeLoader
import calendar


class Map(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def get_time_now():
    d = datetime.utcnow()
    return calendar.timegm(d.utctimetuple())


def destructure(dict): return (item[1] for item in dict.items())


def destructure_keys(
    dict, *args): return (dict[arg] if arg in dict else None for arg in args)


def chunks(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def print_separator(logger, char='-'):
    logger.info(char * 50)


def dynamic_import(package, modules=[]):
    return __import__(
        package,
        globals(),
        locals(),
        modules
    )


def get_yaml_file(filename):
    with open(filename) as file:
        return load(file, Loader=SafeLoader)


def print_message(message, logger, char='-'):
    print_separator(logger, char)
    logger.info(message)
    print_separator(logger, char)


def download_s3_file(event, s3_client, temporal_path='/tmp'):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    filename = key.split('/')[-1]
    download_path = f'{temporal_path}/{filename}'
    s3_client.download_file(bucket, key, download_path)

    return filename, download_path


def concat(messages):
    return ' '.join(messages)


def group_dict_keys(obj):
    keys = [key.split('_')[0] for key in obj.keys() if len(key) > 0]
    keys.sort()
    prefixes = [key for key, group in groupby(
        keys) if len(list(group)) > 1 and len(key) > 0]

    for prefix in prefixes:
        keys_to_delete = [
            key for key, _ in obj.items() if key.startswith(prefix)
        ]
        cols = dict(
            [
                (key[len(f'{prefix}_'):], value)
                for key, value in obj.items() if key.startswith(prefix)
            ]
        )
        obj = {
            key: value
            for key, value in obj.items() if key not in keys_to_delete
        }
        obj[prefix] = cols

    return obj


def named_tuple(row, cols):
    model = {}

    cols = list(reversed(cols))
    for col in row:
        model[cols.pop()] = col

    return Map(model)
