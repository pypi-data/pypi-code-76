import re

import torch
from unitorch.functions import pop_first_non_none_value
from unitorch.utils.decorators import (
    add_default_section_for_init,
    add_group_prefix_suffix_for_key,
)
from unitorch import register_process
from unitorch.core import core_class


class Base(core_class):
    def __init__(self, map_dict=dict()):
        self.map_dict = map_dict
        self.re4float = re.compile(r"^[-+]?[0-9]+\.[0-9]+$")

    @classmethod
    @add_default_section_for_init("core/process/base")
    def init_from_core_configure(cls, cfg, **kwargs):
        map_dict = cfg.getdefault("core/process/base", "map_dict", None)
        if map_dict is not None:
            map_dict = eval(map_dict)
        else:
            map_dict = dict()

        assert isinstance(map_dict, dict)

        return dict(
            {
                "map_dict": map_dict,
            }
        )

    @register_process("core/process/base_for_int")
    @add_group_prefix_suffix_for_key
    def for_int(self, text, key="dint"):
        if text.strip() in self.map_dict:
            text = self.map_dict.get(text)
        assert text.isdigit()
        return dict(
            {
                key: torch.tensor(int(text)),
            }
        )

    @register_process("core/process/base_for_float")
    @add_group_prefix_suffix_for_key
    def for_float(self, text, key="dfloat"):
        if text.strip() in self.map_dict:
            text = self.map_dict.get(text)
        assert self.re4float.match(text)
        return dict(
            {
                key: torch.tensor(float(text)),
            }
        )

    @register_process("core/process/base_post_for_string")
    def post_for_string(self, tensor, sep=",", key="score", actfn=None):
        if actfn is not None:
            tensor = actfn(tensor.float())
        tensor = tensor.squeeze()
        if tensor.dim() == 1:
            tensor = list(map(lambda x: str(float(x)), tensor))
        elif tensor.dim() == 2:
            tensor = [sep.join(map(lambda x: str(float(x)), t)) for t in tensor]
        else:
            raise "tensor dim is greater than 2"
        return dict({key: tensor})
