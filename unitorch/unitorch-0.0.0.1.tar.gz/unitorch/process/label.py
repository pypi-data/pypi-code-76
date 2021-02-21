import re

import torch
from unitorch.functions import pop_first_non_none_value
from unitorch.utils.decorators import (
    add_key_group_info_for_process,
    add_default_section_for_init,
)
from unitorch import register_process
from unitorch.core import core_class


def _text_process(text, map_dict, sep=","):
    _text = text.split(sep)
    if all(t.strip() in map_dict for t in _text):
        _text = [map_dict[t.strip()] for t in _text]
        text = sep.join(map(str, _text))
    return text


class Label(core_class):
    def __init__(self, num_class=1, map_dict=dict(), sep=",", max_seq_length=64):
        self.num_class = num_class
        self.map_dict = map_dict
        self.sep = sep
        self.re4float = re.compile(r"^[-+]?[0-9]+\.[0-9]+$")
        self.max_seq_length = max_seq_length

    @classmethod
    @add_default_section_for_init("core/process/label")
    def init_from_core_configure(cls, cfg, **kwargs):
        map_dict = cfg.getdefault("core/process/label", "map_dict", None)
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

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/label_for_bce", net_targets=["label", "sample_weight"]
        )
    )
    @register_process("core/process/label_for_bce")
    def for_bce(self, text, sample_weight=None):
        """
        text: "0, 1"
        label: tensor([1, 1, 0, 0 ,0]) # num_class=5
        """
        text = _text_process(text, self.map_dict, self.sep)
        assert all(t.isdigit() for t in text.split(self.sep))
        label = torch.zeros(self.num_class)
        if self.num_class > 1:
            label[list(map(int, text.split(self.sep)))] = 1
        else:
            assert text.count(self.sep) == 0 and int(text) in (0, 1)
            label.data[0] = int(text)
        if sample_weight is None:
            sample_weight = 1.0
        return dict(
            {"label": label, "sample_weight": torch.tensor(float(sample_weight))}
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/label_for_int", net_targets=["label", "sample_weight"]
        )
    )
    @register_process("core/process/label_for_int")
    def for_int(self, text, sample_weight=None):
        """
        text: "1002"
        label: tensor(1002)
        """
        if text.strip() in self.map_dict:
            text = self.map_dict.get(text)
        assert text.isdigit()
        if sample_weight is None:
            sample_weight = 1.0
        return dict(
            {
                "label": torch.tensor(int(text)),
                "sample_weight": torch.tensor(float(sample_weight)),
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/label_for_float", net_targets=["label", "sample_weight"]
        )
    )
    @register_process("core/process/label_for_float")
    def for_float(self, text, sample_weight=None):
        """
        text: "0.3"
        label: tensor(0.3)
        """
        if text.strip() in self.map_dict:
            text = self.map_dict.get(text)
        assert self.re4float.match(text)
        if sample_weight is None:
            sample_weight = 1.0
        return dict(
            {
                "label": torch.tensor(float(text)),
                "sample_weight": torch.tensor(float(sample_weight)),
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/label_for_seq",
            net_targets=["label", "label_mask", "sample_weight"],
        )
    )
    @register_process("core/process/label_for_seq")
    def for_seq(self, text, sample_weight=None):
        """
        text: "good, bad, bad, good"
        label: tensor([1, 0, 0, 1])
        """
        text = _text_process(text, self.map_dict, self.sep)
        assert all(
            (t.isdigit() or self.re4float.match(t)) for t in text.split(self.sep)
        )
        label = torch.zeros(self.max_seq_length)
        text = text.split(self.sep)
        for idx, l in enumerate(text[: self.max_seq_length]):
            assert int(l) < self.num_class
            label.data[idx] = int(l)
        mask = [1] * min(len(text), self.max_seq_length) + [0] * (
            self.max_seq_length - len(text)
        )
        return dict(
            {
                "label": torch.tensor(label, dtype=torch.long),
                "label_mask": torch.tensor(mask),
            }
        )
