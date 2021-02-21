import sys
import torch.nn as nn
import logging
import inspect
from unitorch.data.dataset_for_preprocess import add_key_group_info

OPTIMIZED_CLASSES = dict()
"""
core class init decorations
"""


def add_default_section_for_init(section, extra_default_params=dict()):
    """
    section: default section for core configuration
    extra_default_params: dict(key1=value1)
    """

    def default_init_func(cls, cfg, **kwargs):
        sign = inspect.signature(cls)
        params = sign.parameters
        for k, v in params.items():
            dvalue = v.default
            if kwargs.get(k):
                continue
            kwargs[k] = cfg.getdefault(section, k, dvalue)
        for k, v in extra_default_params.items():
            kwargs[k] = cfg.getdefault(section, k, v)
        obj = cls(**kwargs)
        setattr(obj, "_core_config", cfg)
        return obj

    def add_func(init_func):
        def _init_func(cls, cfg, **kwargs):
            ret = init_func(cls, cfg, **kwargs)
            if isinstance(ret, cls):
                setattr(ret, "_core_config", cfg)
                return ret
            assert isinstance(ret, dict) or ret is None
            if ret is not None:
                kwargs.update(ret)
            ret = default_init_func(cls, cfg, **kwargs)
            return ret

        return _init_func

    return add_func


def add_default_section_for_instance_function(section, extra_default_params=dict()):
    """
    section: default section for core configuration
    extra_default_params: dict(key1=value1)
    """

    def get_inst_func_params(inst_func, cfg, args, kwargs):
        sign = inspect.signature(inst_func)
        params = sign.parameters
        for k, v in extra_default_params.items():
            if k in kwargs:
                continue
            kwargs[k] = cfg.getdefault(section, k, v)

        for i, (k, v) in enumerate(params.items()):
            if k == "self" or k in kwargs:
                continue
            dvalue = args[i] if i < len(args) else v.default
            kwargs[k] = cfg.getdefault(section, k, dvalue)
        return kwargs

    def add_func(inst_func):
        def _inst_func(self, *args, **kwargs):
            if hasattr(self, "_core_config"):
                kwargs = get_inst_func_params(
                    inst_func, self._core_config, args, kwargs
                )
                ret = inst_func(self, **kwargs)
            else:
                ret = inst_func(self, *args, **kwargs)
            return ret

        return _inst_func

    return add_func


def add_net_outputs_for_core_model(func):
    def add_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        if isinstance(ret, dict) and "net_outputs" in ret:
            return ret
        return dict(net_outputs=ret)

    return add_func


"""
process functions decorations
"""


def add_key_group_info_for_process(group_info: dict):
    """
    add static group info for process
    name: process function name
    net_inputs: [key1, key2]
    net_targets: [key3, key4]
    """

    add_key_group_info(**group_info)

    def actual_func(fn):
        return fn

    return actual_func


def add_group_prefix_suffix_for_key(process_func):
    """
    add daynamic group info for process
    group_for_key is in ['net_inputs', 'net_targets']
    """

    def add_prefix_suffix_func(*args, **kwargs):
        sign = inspect.signature(process_func)
        params = sign.parameters
        for i, (k, v) in enumerate(params.items()):
            if v.default is inspect._empty or k in kwargs:
                continue
            kwargs[k] = v.default

        group_for_key = kwargs.pop("group_for_key", None)
        prefix_for_key = kwargs.pop("prefix_for_key", None)
        suffix_for_key = kwargs.pop("suffix_for_key", None)
        ret_dict = process_func(*args, **kwargs)
        group_for_key = "" if group_for_key is None else f"{group_for_key}/"
        prefix_for_key = "" if prefix_for_key is None else f"{prefix_for_key}_"
        suffix_for_key = "" if suffix_for_key is None else f"_{suffix_for_key}"
        new_ret_dict = {
            f"{group_for_key}{prefix_for_key}{k}{suffix_for_key}": v
            for k, v in ret_dict.items()
        }
        return new_ret_dict

    return add_prefix_suffix_func


def generation_model_decorator(cls):
    class generation_model(nn.Module):
        def __init__(self, *args, **kwargs):
            super().__init__()
            if "_generation_model" in kwargs:
                self.model = kwargs.pop("_generation_model")
            else:
                self.model = cls(*args, **kwargs)

        @add_net_outputs_for_core_model
        def forward(self, *args, **kwargs):
            if self.training:
                return self.model(*args, **kwargs)
            return self.model.generate(*args, **kwargs)

        @classmethod
        def init_from_core_configure(_cls, cfg, **kwargs):
            model = cls.init_from_core_configure(cfg, **kwargs)
            return _cls(_generation_model=model)

        def load_state_dict(self, state_dict):
            self.model.load_state_dict(state_dict)

        def state_dict(self):
            return self.model.state_dict()

        def save_checkpoint(self, ckpt_dir, **kwargs):
            return self.model.save_checkpoint(ckpt_dir, **kwargs)

        def from_checkpoint(self, ckpt_dir, **kwargs):
            return self.model.from_checkpoint(ckpt_dir, **kwargs)

        def from_pretrained(self, pretrain_weight_name_or_path, **kwargs):
            return self.model.from_pretrained(pretrain_weight_name_or_path, **kwargs)

    return generation_model


# replace decorator from fastseq
def replace(target_obj):
    """A decorator to replace the specified obj.

    `target_obj` can be a class or a function.

    Example:

    ```python
    class A:
        def f(self):
            print('class A')
    @replace(A)
    class B:
        def f(self):
            print('class B')
    ```

    Args:
        target_obj (class/func/method): a class, method, or function to be
                                        replaced.

    Returns:
        A decorator function to replace the input object.
    """

    def decorator(new_obj):
        if target_obj in OPTIMIZED_CLASSES:
            logging.warning("{} has been optimized again.".format(target_obj))
        setattr(new_obj, "__replaced_class__", target_obj)
        OPTIMIZED_CLASSES[target_obj] = new_obj
        for k, v in list(sys.modules.items()):
            if (
                target_obj.__name__ in v.__dict__
                and v.__dict__[target_obj.__name__] is target_obj
            ):
                delattr(sys.modules[k], target_obj.__name__)
                setattr(sys.modules[k], target_obj.__name__, new_obj)
                logging.debug(
                    "In module {}, {} is replaced by {}".format(k, target_obj, new_obj)
                )
            # replace target_obj if it is used as the base classes.
            for key in list(v.__dict__.keys()):
                if (
                    inspect.isclass(v.__dict__[key])
                    and v.__dict__[key] != new_obj
                    and target_obj in v.__dict__[key].__bases__
                ):
                    idx = v.__dict__[key].__bases__.index(target_obj)
                    bases = list(v.__dict__[key].__bases__)
                    bases[idx] = new_obj
                    v.__dict__[key].__bases__ = tuple(bases)
                    logging.debug(
                        "In module {}, the base class of {} is replaced by {}".format(
                            k, v.__dict__[key], new_obj
                        )
                    )
        return new_obj

    return decorator
