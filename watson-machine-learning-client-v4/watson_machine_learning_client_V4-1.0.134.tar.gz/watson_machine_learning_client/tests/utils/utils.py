import json
import os
from configparser import ConfigParser
from functools import wraps

__all__ = [
    "get_wml_credentials",
    "get_cos_credentials",
    "get_env",
    "is_cp4d",
    "bucket_exists",
    "bucket_name_gen",
    'print_test_separators',
    "get_space_id"
]


if "ENV" in os.environ:
    environment = os.environ['ENV']
else:
    environment = "YP_QA"


timeouts = "TIMEOUTS"
credentials = "CREDENTIALS"
training_data = "TRAINING_DATA"
configDir = "./config.ini"

config = ConfigParser()
config.read(configDir)


def get_env():
    return environment


def get_wml_credentials(env=environment):
    return json.loads(config.get(env, 'wml_credentials'))


def get_cos_credentials(env=environment):
    return json.loads(config.get(env, 'cos_credentials'))


def is_cp4d():
    if "CP4D" in get_env():
        return True
    elif "ICP" in get_env():
        return True
    elif "OPEN_SHIFT" in get_env():
        return True
    elif "CPD" in get_env():
        return True

    return False


def bucket_exists(cos_resource, bucket_name):
    """
    Return True if bucket with `bucket_name` exists. Else False.
    """
    buckets = cos_resource.buckets.all()
    for bucket in buckets:
        if bucket.name == bucket_name:
            return True
    print("Bucket {0} not found".format(bucket_name))
    return False


def bucket_name_gen(prefix='bucket-tests', id_size=8):
    import random
    import string

    return prefix + "-" + ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(id_size))


def print_test_separators(method):
    """Printing visual separators for tests."""
    @wraps(method)
    def _method(*method_args, **method_kwargs):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        method_output = method(*method_args, **method_kwargs)
        print("________________________________________________________________________")

        return method_output

    return _method


def get_space_id(wml_client, space_name):
    """
    Return space id of existed or just created space named as `space_name`.
    """
    spaces_details = wml_client.spaces.get_details().get('resources')
    space_id = None
    for space_d in spaces_details:
        if space_d['metadata']['name'] == space_name:
            space_id = space_d['metadata']['id']

    if not space_id:
        # create new space for tests
        details = wml_client.spaces.store(meta_props={wml_client.spaces.ConfigurationMetaNames.NAME: space_name})
        space_id = details['metadata'].get('id')
        print(f"New space `{space_name}` has been created, space_id={space_id}")

    return space_id

