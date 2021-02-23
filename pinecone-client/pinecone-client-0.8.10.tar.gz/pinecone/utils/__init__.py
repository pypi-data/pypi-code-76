#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pathlib import Path
import inspect


from pinecone.protos import core_pb2
import numpy as np
from loguru import logger
import hashlib
import os



# import lz4.frame


def load_numpy(proto_arr: 'core_pb2.NdArray') -> 'np.ndarray':
    """
    Load numpy array from protobuf
    :param proto_arr:
    :return:
    """
    if len(proto_arr.shape) == 0:
        return np.array([])
    # if proto_arr.compressed:
    #     numpy_arr = np.frombuffer(lz4.frame.decompress(proto_arr.buffer), dtype=proto_arr.dtype)
    # else:
    numpy_arr = np.frombuffer(proto_arr.buffer, dtype=proto_arr.dtype)
    return numpy_arr.reshape(proto_arr.shape)


def dump_numpy(np_array: 'np.ndarray', compressed: bool = False) -> 'core_pb2.NdArray':
    """
    Dump numpy array to protobuf
    :param np_array:
    :param compressed: whether to use lz4 compression
    :return:
    """
    protobuf_arr = core_pb2.NdArray()
    protobuf_arr.dtype = str(np_array.dtype)
    protobuf_arr.shape.extend(np_array.shape)
    # if compressed:
    #     protobuf_arr.buffer = lz4.frame.compress(np_array.tobytes())
    #     protobuf_arr.compressed = True
    # else:
    protobuf_arr.buffer = np_array.tobytes()
    return protobuf_arr


HUB_CLASSES = set()


def hubify(cls):
    global HUB_CLASSES
    HUB_CLASSES.add(cls)
    return cls


def load_hub_service(module):
    global HUB_CLASSES
    subclasses = [getattr(module, d) for d in dir(module)
                  if inspect.isclass(getattr(module, d)) and getattr(module, d) in HUB_CLASSES]
    if len(subclasses) > 1:
        logger.error(f'Found more than one hub service, unable to load: {subclasses}.')
    elif len(subclasses) == 0:
        logger.error(f'No implementations of {HUB_CLASSES} found.')
    else:
        return subclasses[0]


def module_name(module):
    return module.__class__.__module__ + '.' + module.__class__.__name__


def get_version():
    return Path(__file__).parent.parent.joinpath('__version__').read_text().strip()


def clear_pb_repeated(field):
    while len(field) > 0:
        field.pop()


def get_native_port(name: str):
    return 6000 + int(hashlib.sha1(name.encode()).hexdigest(), 16) % 20000


def shard_name(name: str, shard_id: int):
    if shard_id > 0:
        return name + '-s' + str(shard_id)
    return name


def replica_from_shard_name(name: str, replica_id: int = None):
    if replica_id is not None:
        return name + '-' + str(replica_id)
    return name


def replica_name(name: str, shard_id: int, replica_id: int = None):  # shard == 0 is router
    svc_name = shard_name(name, shard_id)
    return replica_from_shard_name(svc_name, replica_id)


def replica_kube_hostname(name: str, shard_id: int, replica_id: int):
    return replica_name(name, shard_id, replica_id) + '.' + shard_name(name, shard_id)


def replica_kube_hostname_from_shard(name: str, replica_id: int):
    return replica_from_shard_name(name, replica_id) + '.' + name


def parse_hostname(function_name: str, hostname: str):
    hostname_list = hostname.replace(function_name, '').split('-')
    shard_id = None
    replica_id = None

    if 'deployment' in hostname:
        return shard_id, replica_id

    for item in hostname_list[1:]:
        if item[0] == 's':
            try:
                shard_id = int(item[1:])
            except ValueError:
                pass
        else:
            try:
                replica_id = int(item)
            except ValueError:
                pass
    return shard_id, replica_id


def open_or_create(path: str, truncate: int = None):
    if os.path.exists(path):
        file = open(path, 'r+b')
    else:
        file = open(path, 'w+b')
    if truncate:
        file.truncate(truncate)
    return file


def get_hostname():
    return os.environ.get("HOSTNAME")


def get_memory_usage():
    with open('/sys/fs/cgroup/memory/memory.stat') as stat_file:
        rss_line = stat_file.readlines()[1].strip()
        return int(rss_line.split()[1])

