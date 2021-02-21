import os
import json
import random
from functools import partial

import numpy as np
import torch
import torch.nn as nn
from transformers import BertModel

from unitorch import add_core_pretrained_dict, register_model
from unitorch.core import core_model_class
from unitorch.utils.decorators import (
    add_net_outputs_for_core_model,
    add_default_section_for_init,
)
from unitorch.utils.hf import hf_cached_path

from transformers import BertConfig, BertModel

CONFIG_KEY = "config"
CONFIG_NAME = "config.json"

VOCABS_KEY = "vocab"
VOCABS_NAME = "vocab.txt"

CORE_BERT_PRETRAINED_DICT = {
    "default-bert": {
        "config": "https://huggingface.co/bert-base-uncased/resolve/main/config.json",
        "vocab": "https://huggingface.co/bert-base-uncased/resolve/main/vocab.txt",
    },
    "bert-base-uncased": {
        "config": "https://huggingface.co/bert-base-uncased/resolve/main/config.json",
        "vocab": "https://huggingface.co/bert-base-uncased/resolve/main/vocab.txt",
        "weight": "https://huggingface.co/bert-base-uncased/resolve/main/pytorch_model.bin",
    },
}

add_core_pretrained_dict(CORE_BERT_PRETRAINED_DICT)


class Bert(core_model_class):
    def __init__(self, config_path, **kwargs):
        super().__init__()
        self.config_path = config_path
        params = json.load(open(self.config_path, "r"))
        self.config = BertConfig(**params)

    @classmethod
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def save_checkpoint(self, ckpt_dir="./cache", **kwargs):
        if not os.path.exists(ckpt_dir):
            os.mkdir(ckpt_dir)
        config_path = os.path.join(ckpt_dir, CONFIG_NAME)
        with open(config_path, "w") as f:
            f.write(open(self.config_path, "r").read())

        super().save_checkpoint(ckpt_dir=ckpt_dir, **kwargs)

    def from_checkpoint(self, ckpt_dir="./cache", **kwargs):
        super().from_checkpoint(ckpt_dir=ckpt_dir, **kwargs)


@register_model("core/model/bert_for_classification")
class BertForClassifcation(Bert):
    def __init__(self, config_path, num_class=1):
        super().__init__(config_path)
        self.bert = BertModel(self.config)
        self.dropout = nn.Dropout(self.config.hidden_dropout_prob)
        self.classifier = nn.Linear(self.config.hidden_size, num_class)
        self.init_weights()

    @classmethod
    def init_from_core_configure(cls, cfg, **kwargs):
        pretrained_name = cfg.getdefault(
            "core/model/bert", "pretrained_name", "default-bert"
        )
        config_name_or_path = cfg.getdefault(
            "core/model/bert", "config_name_or_path", pretrained_name
        )
        config_path = (
            CORE_BERT_PRETRAINED_DICT[config_name_or_path][CONFIG_KEY]
            if config_name_or_path in CORE_BERT_PRETRAINED_DICT
            else config_name_or_path
        )

        config_path = hf_cached_path(config_path)
        inst = cls(
            config_path, num_class=cfg.getdefault("core/model/bert", "num_class", 1)
        )

        if pretrained_name is not None:
            inst.from_pretrained(pretrained_name)

        return inst

    @add_net_outputs_for_core_model
    def forward(self, tokens_ids, attn_mask, seg_ids, pos_ids):
        outputs = self.bert(
            tokens_ids,
            attention_mask=attn_mask,
            token_type_ids=seg_ids,
            position_ids=pos_ids,
        )
        pooled_output = outputs[1]

        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits


# @register_model("core/model/bert_for_question_answer")
class BertForQuestionAnswer(Bert):
    pass


# @register_model("core/model/bert_for_token_classification")
class BertForTokenClassification(Bert):
    pass


# @register_model("core/model/bert_for_pretrain")
class BertForPretrain(Bert):
    pass
