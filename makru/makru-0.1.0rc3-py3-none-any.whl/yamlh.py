from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def yaml_load(stream):
    return load(stream, Loader=Loader)


def yaml_dump(data):
    return dump(data, Dumper=Dumper)
