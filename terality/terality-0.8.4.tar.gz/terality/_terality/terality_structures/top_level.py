from functools import partial
from uuid import uuid4

import pandas as pd

from .. import UploadRequest, upload_local_files, upload_s3_files
from . import call_pandas_function


def make_upload(path: str) -> UploadRequest:
    transfer_id = str(uuid4())
    if path.startswith('s3://'):
        aws_region = upload_s3_files(path, transfer_id)
    else:
        upload_local_files(path, transfer_id)
        aws_region = None
    return UploadRequest(transfer_id=transfer_id, aws_region=aws_region)


def _treat_read_job(method_name, *args, **kwargs):
    """ Special job to intercept file arguments and upload them to Terality for pd.read_xxx() jobs"""
    if 'path' in kwargs:
        kwargs['path'] = make_upload(kwargs['path'])
    else:
        path, *others = args
        args = [make_upload(path)] + others
    return call_pandas_function('free_function', None, method_name, *args, **kwargs)


_read_top_level_functions = {'read_parquet', 'read_csv'}


_top_level_functions = _read_top_level_functions | set()


def _get_top_level_attribute(attribute: str):
    if callable(pd.__getattribute__(attribute)):
        if attribute in _read_top_level_functions:
            return partial(_treat_read_job, attribute)
        return partial(call_pandas_function, 'free_function', None, attribute)
    raise AttributeError(f'Name {attribute!r} is not defined')
