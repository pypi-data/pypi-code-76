import os
import random
from functools import partial
from random import randint, shuffle, choice

import numpy as np
import torch
from transformers import BertTokenizer

from unitorch.functions import pop_first_non_none_value
from unitorch.utils.decorators import (
    add_default_section_for_init,
    add_key_group_info_for_process,
)
from unitorch import register_process
from unitorch.core import core_class
from unitorch.utils.hf import hf_cached_path
from unitorch.classification.bert import CORE_BERT_PRETRAINED_DICT, VOCABS_KEY


def get_special_vocab(tokenizer, special_tokens):
    extra_map = dict()
    for i in range(len(special_tokens)):
        extra_map["[unused{}]".format(990 - i)] = special_tokens[i]
    for k, v in extra_map.items():
        if k in tokenizer.vocab.keys():
            tokenizer.vocab[v] = tokenizer.vocab[k]
    return tokenizer, extra_map


def get_random_word(vocab_words):
    i = randint(0, len(vocab_words) - 1)
    return vocab_words[i]


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""

    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


def get_random_mask_indexes(
    tokens,
    masked_lm_prob=0.15,
    do_whole_word_mask=True,
    max_predictions_per_seq=20,
    special_tokens=[],
):
    cand_indexes = []
    for (i, token) in enumerate(tokens):
        if token in special_tokens:
            continue
        if (
            do_whole_word_mask and len(cand_indexes) >= 1 and token.startswith("##")
        ) and cand_indexes[-1][-1] == i - 1:
            cand_indexes[-1].append(i)
        else:
            cand_indexes.append([i])
    random.shuffle(cand_indexes)
    num_to_predict = min(
        max_predictions_per_seq, max(1, int(round(len(tokens) * masked_lm_prob)))
    )
    covered_indexes = set()
    for index_set in cand_indexes:
        if len(covered_indexes) >= num_to_predict:
            break
        if len(covered_indexes) + len(index_set) > num_to_predict or any(
            i in covered_indexes for i in index_set
        ):
            continue
        covered_indexes.update(index_set)
    return covered_indexes


def get_bert_tokenizer(
    vocab_path, never_split_tokens=[], do_lower_case=True, do_basic_tokenize=True
):
    never_split_tokens = list(filter(lambda x: x != "", never_split_tokens))
    assert os.path.exists(vocab_path)
    tokenizer = BertTokenizer(
        vocab_path,
        do_lower_case=do_lower_case,
        do_basic_tokenize=do_basic_tokenize,
        never_split=never_split_tokens,
    )
    special_tokens_map = dict()
    if len(never_split_tokens) > 0:
        tokenizer, special_tokens_map = get_special_vocab(tokenizer, never_split_tokens)
    return dict({"tokenizer": tokenizer, "special_tokens_map": special_tokens_map})


class Bert(core_class):
    def __init__(
        self,
        vocab_path,
        max_seq_length=128,
        never_split_tokens=[],
        do_lower_case=True,
        do_whole_word_mask=True,
        masked_lm_prob=0.15,
        max_predictions_per_seq=20,
    ):
        self.max_seq_length = max_seq_length
        tokenizer_and_special_token_map = get_bert_tokenizer(
            vocab_path, never_split_tokens, do_lower_case
        )
        self.tokenizer = tokenizer_and_special_token_map.get("tokenizer")
        self.special_tokens_map = tokenizer_and_special_token_map.get(
            "special_tokens_map"
        )
        self.do_whole_word_mask = do_whole_word_mask
        self.masked_lm_prob = masked_lm_prob
        self.max_predictions_per_seq = max_predictions_per_seq
        self.vocab_words = list(self.tokenizer.vocab.keys())

    @classmethod
    @add_default_section_for_init("core/process/bert")
    def init_from_core_configure(cls, cfg, **kwargs):
        never_split_tokens = cfg.getdefault(
            "core/process/bert", "never_split_tokens", None
        )
        if never_split_tokens is not None:
            never_split_tokens = eval(never_split_tokens)
        else:
            never_split_tokens = []

        pretrained_name = cfg.getdefault(
            "core/process/bert", "pretrained_name", "default-bert"
        )
        vocab_name_or_path = cfg.getdefault(
            "core/process/bert", "vocab_name_or_path", pretrained_name
        )
        vocab_path = (
            CORE_BERT_PRETRAINED_DICT[vocab_name_or_path][VOCABS_KEY]
            if vocab_name_or_path in CORE_BERT_PRETRAINED_DICT
            else vocab_name_or_path
        )

        vocab_path = hf_cached_path(vocab_path)

        return dict(
            {
                "vocab_path": vocab_path,
                "never_split_tokens": never_split_tokens,
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/bert_for_seq",
            net_inputs=["tokens_ids", "seg_ids", "attn_mask", "pos_ids"],
        )
    )
    @register_process("core/process/bert_for_seq")
    def for_seq(self, text, max_seq_length=None):
        max_seq_length = int(
            pop_first_non_none_value(max_seq_length, self.max_seq_length)
        )
        tokens = self.tokenizer.tokenize(text)
        tokens = tokens[: max_seq_length - 2]
        tokens = ["[CLS]"] + tokens + ["[SEP]"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segment_ids = [0] * len(tokens_ids)
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding
        segment_ids += len(padding) * [1]

        assert len(tokens_ids) == max_seq_length
        assert len(tokens_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        return dict(
            {
                "tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "seg_ids": torch.tensor(segment_ids, dtype=torch.long),
                "attn_mask": torch.tensor(tokens_mask, dtype=torch.long),
                "pos_ids": torch.tensor(list(range(max_seq_length)), dtype=torch.long),
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/bert_for_pair",
            net_inputs=["tokens_ids", "seg_ids", "attn_mask", "pos_ids"],
        )
    )
    @register_process("core/process/bert_for_pair")
    def for_pair(self, text_a, text_b, max_seq_length=None):
        max_seq_length = int(
            pop_first_non_none_value(max_seq_length, self.max_seq_length)
        )
        tokens_a = self.tokenizer.tokenize(text_a)
        tokens_b = self.tokenizer.tokenize(text_b)
        _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        tokens = ["[CLS]"] + tokens_a + ["[SEP]"] + tokens_b + ["[SEP]"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segment_ids = [0] + [0] * len(tokens_a) + [0] + [1] * len(tokens_b) + [1]
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding
        segment_ids += len(padding) * [1]

        assert len(tokens_ids) == max_seq_length
        assert len(tokens_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        return dict(
            {
                "tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "seg_ids": torch.tensor(segment_ids, dtype=torch.long),
                "attn_mask": torch.tensor(tokens_mask, dtype=torch.long),
                "pos_ids": torch.tensor(list(range(max_seq_length)), dtype=torch.long),
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/bert_for_pretrain",
            net_inputs=["tokens_ids", "seg_ids", "attn_mask", "pos_ids"],
            net_targets=["nsp_label", "mlm_label", "mlm_label_mask"],
        )
    )
    @register_process("core/process/bert_for_pretrain")
    def for_pretrain(self, text_a, text_b, nsp_label, max_seq_length=None):
        max_seq_length = int(
            pop_first_non_none_value(max_seq_length, self.max_seq_length)
        )
        tokens_a = self.tokenizer.tokenize(text_a)
        tokens_b = self.tokenizer.tokenize(text_b)
        _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        tokens = ["[CLS]"] + tokens_a + ["[SEP]"] + tokens_b + ["[SEP]"]

        covered_indexes = get_random_mask_indexes(
            tokens,
            self.masked_lm_prob,
            do_whole_word_mask,
            max_predictions_per_seq,
            special_tokens=["[CLS]", "[SEP]"],
        )
        label = [
            tokens[pos] if pos in covered_indexes else "[PAD]"
            for pos in range(max_seq_length)
        ]
        label_mask = [
            1 if pos in covered_indexes else 0 for pos in range(max_seq_length)
        ]
        label = self.tokenizer.convert_tokens_to_ids(label)

        for index in covered_indexes:
            masked_token = None
            if random.random() < 0.8:
                masked_token = "[MASK]"
            else:
                masked_token = (
                    tokens[index]
                    if random.random() < 0.5
                    else get_random_word(self.vocab_words)
                )
            tokens[index] = masked_token

        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segment_ids = [0] + [0] * len(tokens_a) + [0] + [1] * len(tokens_b) + [1]
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding
        segment_ids += len(padding) * [1]

        assert len(tokens_ids) == max_seq_length
        assert len(tokens_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        return dict(
            {
                "tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "seg_ids": torch.tensor(segment_ids, dtype=torch.long),
                "attn_mask": torch.tensor(tokens_mask, dtype=torch.long),
                "pos_ids": torch.tensor(list(range(max_seq_length)), dtype=torch.long),
                "nsp_label": torch.tensor(int(nsp_label), dtype=torch.long),
                "mlm_label": torch.tensor(label, dtype=torch.long),
                "mlm_label_mask": torch.tensor(label_mask, dtype=torch.long),
            }
        )
