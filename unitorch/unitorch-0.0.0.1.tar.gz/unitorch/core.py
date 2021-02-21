import os
import logging
from abc import ABCMeta
from abc import abstractmethod
import torch
import torch.nn as nn
from transformers.file_utils import is_remote_url
from unitorch import CORE_PRETRAINED_DICT
from unitorch.utils.hf import hf_cached_path

WEIGHT_NAME = "pytorch_model.bin"
WEIGHT_KEY = "weight"

# core class
class core_class(metaclass=ABCMeta):
    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def __call__(self):
        pass


class core_model_class(nn.Module):
    def __init__(self):
        super().__init__()
        pass

    def init_weights(self):
        pass

    def from_checkpoint(self, ckpt_dir="./cache", **kwargs):
        weight_name = kwargs.pop("weight_name", WEIGHT_NAME)
        weight_path = os.path.join(ckpt_dir, weight_name)
        if not os.path.exists(weight_path):
            return
        state_dict = torch.load(weight_path, map_location="cpu")
        self.load_state_dict(state_dict)
        logging.info(
            f"{self.__class__.__name__} model load weight from checkpoint {weight_path}"
        )

    def save_checkpoint(self, ckpt_dir="./cache", **kwargs):
        weight_name = kwargs.pop("weight_name", WEIGHT_NAME)
        state_dict = self.state_dict()
        weight_path = os.path.join(ckpt_dir, weight_name)
        torch.save(state_dict, weight_path)
        logging.info(
            f"{self.__class__.__name__} model save checkpoint to {weight_path}"
        )

    def from_pretrained(self, pretrain_weight_name_or_path=None, **kwargs):
        if "state_dict" in kwargs:
            state_dict = kwargs.pop(state_dict)
            self.load_state_dict(state_dict, False)
            return

        if pretrain_weight_name_or_path in CORE_PRETRAINED_DICT:
            weight_path = CORE_PRETRAINED_DICT[pretrain_weight_name_or_path]
            if isinstance(weight_path, dict) and WEIGHT_KEY in weight_path.keys():
                weight_path = weight_path.get(WEIGHT_KEY)
            elif isinstance(weight_path, dict):
                return
        elif os.path.isfile(pretrain_weight_name_or_path):
            weight_path = pretrain_weight_name_or_path
        else:
            return

        if not (is_remote_url(weight_path) or os.path.exists(weight_path)):
            return

        weight_path = hf_cached_path(weight_path)
        state_dict = torch.load(weight_path, map_location="cpu")
        old_keys = []
        new_keys = []
        for key in state_dict.keys():
            new_key = None
            if "gamma" in key:
                new_key = key.replace("gamma", "weight")
            if "beta" in key:
                new_key = key.replace("beta", "bias")
            if new_key:
                old_keys.append(key)
                new_keys.append(new_key)
        for old_key, new_key in zip(old_keys, new_keys):
            state_dict[new_key] = state_dict.pop(old_key)
        self.load_state_dict(state_dict, False)
        logging.info(
            f"{self.__class__.__name__} model load weight from pretrain {pretrain_weight_name_or_path}"
        )

    def init_weights(self):
        pass

    def to_onnx(self):
        pass

    def to_protobuf(self):
        pass
