# import common libs
import os
import sys
import logging
import traceback
import importlib
from functools import partial
from transformers import cached_path
from unitorch.configuration import core_configure_parser
from unitorch.functions import set_core_seed, registry_func

CORE_PRETRAINED_DICT = dict()


def add_core_pretrained_dict(pretrained_dict: dict):
    assert len(CORE_PRETRAINED_DICT.keys() & pretrained_dict.keys()) == 0
    CORE_PRETRAINED_DICT.update(pretrained_dict)


# register
def init_core_module_group(cfg, register_group: dict, core_group: dict):
    for k, v in register_group.items():
        core_group[k] = v.init_from_core_configure(cfg)


core_modules = ["score", "dataset", "loss", "model", "optim", "scheduler", "task"]

for module in core_modules:
    globals()[f"REGISTER_{module.upper()}"] = dict()
    globals()[f"register_{module.lower()}"] = partial(
        registry_func, save_dict=globals()[f"REGISTER_{module.upper()}"]
    )
    globals()[f"core_{module.lower()}"] = dict()
    globals()[f"init_core_{module.lower()}_group"] = partial(
        init_core_module_group,
        register_group=globals()[f"REGISTER_{module.upper()}"],
        core_group=globals()[f"core_{module.lower()}"],
    )

REGISTER_PROCESS = dict()
core_process = dict()


def get_import_module_from_file(import_file):
    for k, v in sys.modules.items():
        if hasattr(v, "__file__") and v.__file__ == import_file:
            return v
    raise "can't find the module"


def register_process(name):
    def actual_func(obj):
        trace_stacks = traceback.extract_stack()
        import_file = trace_stacks[-2][0]
        import_cls_name = trace_stacks[-2][2]
        import_module = get_import_module_from_file(import_file)
        REGISTER_PROCESS[name] = dict(
            {"cls": {"module": import_module, "name": import_cls_name}, "obj": obj}
        )
        return obj

    return actual_func


def rpartial(func, *args, **kwargs):
    return lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))


def init_core_process_group(cfg):
    for k, v in REGISTER_PROCESS.items():
        cls = getattr(v["cls"]["module"], v["cls"]["name"])
        inst = cls.init_from_core_configure(cfg)
        core_process[k] = rpartial(v["obj"], inst)


# import for core modules
import unitorch.auto
import unitorch.classification
import unitorch.generation
import unitorch.modules
import unitorch.loss
import unitorch.optim
import unitorch.score
import unitorch.process
import unitorch.data
from unitorch.auto import AUTO_CONFIG_FROM_HUB_DICT
from unitorch.data.dataset_for_preprocess import NET_INPUTS_KEYS, NET_TARGETS_KEYS


def init_core_group(cfg):
    init_core_process_group(cfg)
    for module in core_modules:
        globals()[f"init_core_{module.lower()}_group"](cfg)
