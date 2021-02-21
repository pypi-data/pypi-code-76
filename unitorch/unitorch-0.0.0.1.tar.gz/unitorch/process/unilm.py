import os
import random
from functools import partial
from random import randint, shuffle, choice
from random import random as rand

import numpy as np
import torch
from transformers import BertTokenizer

from unitorch.functions import pop_first_non_none_value
from unitorch.utils.decorators import (
    add_default_section_for_init,
    add_key_group_info_for_process,
    add_group_prefix_suffix_for_key,
)
from unitorch import register_process
from unitorch.core import core_class
from unitorch.utils.hf import hf_cached_path
from unitorch.generation.unilm import (
    UnilmConfig,
    CORE_UNILM_PRETRAINED_DICT,
    VOCABS_KEY,
    CONFIG_KEY,
)
from unitorch.process.bert import (
    get_bert_tokenizer,
    get_special_vocab,
    get_random_word,
    _truncate_seq_pair,
)


def get_unilm_vocab(tokenizer):
    extra_map = dict()
    extra_map["[unused1]"] = "[X_SEP]"
    for i in range(10):
        extra_map["[unused{}]".format(i + 2)] = "[SEP_{}]".format(i)
    extra_map["[unused12]"] = "[S2S_SEP]"
    extra_map["[unused13]"] = "[S2S_CLS]"
    extra_map["[unused14]"] = "[L2R_SEP]"
    extra_map["[unused15]"] = "[L2R_CLS]"
    extra_map["[unused16]"] = "[R2L_SEP]"
    extra_map["[unused17]"] = "[R2L_CLS]"
    extra_map["[unused18]"] = "[S2S_SOS]"
    for k, v in extra_map.items():
        if k in tokenizer.vocab.keys():
            tokenizer.vocab[v] = tokenizer.vocab[k]
    return tokenizer, extra_map


class Unilm(core_class):
    def __init__(
        self,
        config_path,
        vocab_path,
        max_seq_length=128,
        max_gen_seq_length=128,
        never_split_tokens=[],
        do_lower_case=True,
        do_basic_tokenize=True,
    ):
        self.config = UnilmConfig(config_path)
        self.max_seq_length = max_seq_length
        self.max_gen_seq_length = max_gen_seq_length
        tokenizer_and_special_token_map = get_bert_tokenizer(
            vocab_path, never_split_tokens, do_lower_case, do_basic_tokenize
        )
        self.tokenizer = tokenizer_and_special_token_map.get("tokenizer")
        self.special_tokens_map = tokenizer_and_special_token_map.get(
            "special_tokens_map"
        )
        self.tokenizer, unilm_tokens_map = get_unilm_vocab(self.tokenizer)
        self.special_tokens_map.update(unilm_tokens_map)
        self.vocab_words = list(self.tokenizer.vocab.keys())
        self._tril_matrix = torch.tril(torch.ones((1024, 1024), dtype=torch.long))
        self.source_type_id = getattr(self.config, "source_type_id", 0)
        self.target_type_id = getattr(self.config, "target_type_id", 1)

    @classmethod
    @add_default_section_for_init("core/process/unilm")
    def init_from_core_configure(cls, cfg, **kwargs):
        never_split_tokens = cfg.getdefault(
            "core/process/bert", "never_split_tokens", None
        )
        if never_split_tokens is not None:
            never_split_tokens = eval(never_split_tokens)
        else:
            never_split_tokens = []

        pretrained_name = cfg.getdefault(
            "core/process/unilm", "pretrained_name", "default-unilm"
        )
        config_name_or_path = cfg.getdefault(
            "core/model/unilm", "config_name_or_path", pretrained_name
        )
        config_path = (
            CORE_UNILM_PRETRAINED_DICT[config_name_or_path][CONFIG_KEY]
            if config_name_or_path in CORE_UNILM_PRETRAINED_DICT
            else config_name_or_path
        )

        config_path = hf_cached_path(config_path)

        vocab_name_or_path = cfg.getdefault(
            "core/process/unilm", "vocab_name_or_path", pretrained_name
        )
        vocab_path = (
            CORE_UNILM_PRETRAINED_DICT[vocab_name_or_path][VOCABS_KEY]
            if vocab_name_or_path in CORE_UNILM_PRETRAINED_DICT
            else vocab_name_or_path
        )

        vocab_path = hf_cached_path(vocab_path)

        return dict(
            {
                "config_path": config_path,
                "vocab_path": vocab_path,
                "never_split_tokens": never_split_tokens,
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/unilm_for_seq",
            net_inputs=["tokens_ids", "seg_ids", "attn_mask", "pos_ids"],
        )
    )
    @register_process("core/process/unilm_for_seq")
    def for_seq(self, text, max_seq_length=None):
        max_seq_length = int(
            pop_first_non_none_value(max_seq_length, self.max_seq_length)
        )
        tokens = self.tokenizer.tokenize(text)
        tokens = tokens[: max_seq_length - 2]
        tokens = ["[CLS]"] + tokens + ["[SEP]"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segment_ids = [self.source_type_id] * len(tokens_ids)
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding
        segment_ids += len(padding) * [self.target_type_id]

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
            name="core/process/unilm_for_pair",
            net_inputs=["tokens_ids", "seg_ids", "attn_mask", "pos_ids"],
        )
    )
    @register_process("core/process/unilm_for_pair")
    def for_pair(self, text_a, text_b, max_seq_length=None):
        max_seq_length = int(
            pop_first_non_none_value(max_seq_length, self.max_seq_length)
        )
        tokens_a = self.tokenizer.tokenize(text_a)
        tokens_b = self.tokenizer.tokenize(text_b)
        _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        tokens = ["[CLS]"] + tokens_a + ["[SEP]"] + tokens_b + ["[SEP]"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segment_ids = (
            [self.source_type_id]
            + [self.source_type_id] * len(tokens_a)
            + [self.source_type_id]
            + [self.target_type_id] * len(tokens_b)
            + [self.target_type_id]
        )
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding
        segment_ids += len(padding) * [self.target_type_id]

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
            name="core/process/unilm_for_generation",
            net_inputs=["tokens_ids", "attn_mask", "seg_ids", "pos_ids"],
            net_targets=["next_tokens_ids", "next_tokens_mask"],
        )
    )
    @register_process("core/process/unilm_for_generation")
    def for_generation(
        self,
        text_a,
        text_b,
        max_seq_length=None,
        max_gen_seq_length=None,
        mask_prob=0.5,
    ):
        max_seq_length = int(
            pop_first_non_none_value(max_seq_length, self.max_seq_length)
        )
        max_gen_seq_length = pop_first_non_none_value(
            max_gen_seq_length, self.max_gen_seq_length
        )
        max_seq_length = max_seq_length + max_gen_seq_length
        tokens_a = self.tokenizer.tokenize(text_a)
        tokens_b = self.tokenizer.tokenize(text_b)
        _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        tokens = ["[CLS]"] + tokens_a + ["[SEP]"] + tokens_b + ["[SEP]"]

        n_pred = min(max_gen_seq_length, max(1, int(round(len(tokens_b) * mask_prob))))
        cand_pos = [i for i in range(len(tokens_a) + 2, len(tokens))]
        shuffle(cand_pos)

        def _expand_whole_word(st, end):
            new_st, new_end = st, end
            while (new_st >= 0) and tokens[new_st].startswith("##"):
                new_st -= 1
            while (new_end < len(tokens)) and tokens[new_end].startswith("##"):
                new_end += 1
            return new_st, new_end

        skipgram_size = 5
        masked_pos = set()
        max_cand_pos = max(cand_pos)
        for pos in cand_pos:
            if len(masked_pos) >= n_pred:
                break
            if pos in masked_pos:
                continue

            st_pos, end_pos = _expand_whole_word(pos, pos + 1)
            for mp in range(st_pos, end_pos):
                if 0 < mp <= max_cand_pos:
                    masked_pos.add(mp)
                else:
                    break

        masked_pos = list(masked_pos)
        if len(masked_pos) > n_pred:
            shuffle(masked_pos)
            masked_pos = masked_pos[:n_pred]

        masked_tokens = [tokens[pos] for pos in masked_pos]
        next_tokens = [
            tokens[pos] if pos in masked_pos else "[PAD]"
            for pos in range(max_seq_length)
        ]
        next_tokens_mask = [
            1 if pos in masked_pos else 0 for pos in range(max_seq_length)
        ]
        for pos in masked_pos:
            if rand() < 0.8:  # 80%
                tokens[pos] = "[MASK]"
            elif rand() < 0.5:  # 10%
                tokens[pos] = get_random_word(self.vocab_words)
        next_tokens_ids = self.tokenizer.convert_tokens_to_ids(next_tokens)
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        tokens_mask = torch.zeros(max_seq_length, max_seq_length, dtype=torch.long)
        tokens_mask[:, : len(tokens_a) + 2].fill_(1)
        second_st, second_end = len(tokens_a) + 2, len(tokens_a) + len(tokens_b) + 3
        tokens_mask[second_st:second_end, second_st:second_end].copy_(
            self._tril_matrix[: second_end - second_st, : second_end - second_st]
        )

        segment_ids = (
            [self.source_type_id]
            + [self.source_type_id] * len(tokens_a)
            + [self.source_type_id]
            + [self.target_type_id] * len(tokens_b)
            + [self.target_type_id]
        )
        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        segment_ids += padding

        assert len(tokens_ids) == max_seq_length
        assert len(segment_ids) == max_seq_length

        return dict(
            {
                "tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "seg_ids": torch.tensor(segment_ids, dtype=torch.long),
                "attn_mask": torch.tensor(tokens_mask, dtype=torch.long),
                "pos_ids": torch.tensor(list(range(max_seq_length)), dtype=torch.long),
                "next_tokens_ids": torch.tensor(next_tokens_ids, dtype=torch.long),
                "next_tokens_mask": torch.tensor(next_tokens_mask, dtype=torch.long),
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/unilm_for_faster_generation",
            net_inputs=["tokens_ids", "attn_mask", "seg_ids", "pos_ids"],
            net_targets=["next_tokens_ids", "next_tokens_mask"],
        )
    )
    @register_process("core/process/unilm_for_faster_generation")
    def for_faster_generation(
        self, text_a, text_b, max_seq_length=None, max_gen_seq_length=None
    ):
        max_seq_length = int(
            pop_first_non_none_value(max_seq_length, self.max_seq_length)
        )
        max_gen_seq_length = pop_first_non_none_value(
            max_gen_seq_length, self.max_gen_seq_length
        )
        max_seq_length = max_seq_length + max_gen_seq_length

        tokens_a = self.tokenizer.tokenize(text_a)
        tokens_b = self.tokenizer.tokenize(text_b)
        _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
        tokens = ["[CLS]"] + tokens_a + ["[SEP]"] + tokens_b + ["[SEP]"]

        tokens_b = tokens_b + ["[SEP]"]
        next_tokens = tokens_b[:max_gen_seq_length] + ["[PAD]"] * (
            max_gen_seq_length - len(tokens_b)
        )
        next_tokens_mask = [1] * len(tokens_b[:max_gen_seq_length]) + [0] * (
            max_gen_seq_length - len(tokens_b)
        )
        next_tokens_ids = self.tokenizer.convert_tokens_to_ids(next_tokens)
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        tokens_mask = torch.zeros(
            max_seq_length + max_gen_seq_length,
            max_seq_length + max_gen_seq_length,
            dtype=torch.long,
        )
        tokens_mask[:, : len(tokens_a) + 1].fill_(1)
        second_st, second_end = len(tokens_a) + 1, len(tokens_a) + len(tokens_b) + 3
        tokens_mask[second_st:second_end, second_st:second_end].copy_(
            self._tril_matrix[: second_end - second_st, : second_end - second_st]
        )

        segment_ids = (
            [self.source_type_id]
            + [self.source_type_id] * len(tokens_a)
            + [self.source_type_id]
            + [self.target_type_id] * len(tokens_b)
        )
        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        segment_ids += padding
        position_ids = list(range(len(tokens_ids))) + list(
            range(len(tokens_a) + 2, len(tokens_a) + 2 + max_gen_seq_length)
        )

        tokens_ids += self.tokenizer.convert_tokens_to_ids(
            ["[MASK]"] * max_gen_seq_length
        )
        segment_ids += [self.target_type_id] * max_gen_seq_length
        next_tokens_ids = [0] * max_seq_length + next_tokens_ids
        next_tokens_mask = [0] * max_seq_length + next_tokens_mask
        mask_st, mask_end = max_seq_length, max_seq_length + max_gen_seq_length
        tokens_mask[mask_st:mask_end, second_st:second_end].copy_(
            self._tril_matrix[: mask_end - mask_st, : second_end - second_st]
        )
        tokens_mask[mask_st:mask_end, mask_st:mask_end].copy_(
            torch.eye(mask_end - mask_st)
        )
        return dict(
            {
                "tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "seg_ids": torch.tensor(segment_ids, dtype=torch.long),
                "attn_mask": torch.tensor(tokens_mask, dtype=torch.long),
                "pos_ids": torch.tensor(position_ids, dtype=torch.long),
                "next_tokens_ids": torch.tensor(next_tokens_ids, dtype=torch.long),
                "next_tokens_mask": torch.tensor(next_tokens_mask, dtype=torch.long),
            }
        )

    @register_process("core/process/unilm_for_tokens")
    @add_group_prefix_suffix_for_key
    def for_tokens(self, text, max_seq_length=None, group_for_key="net_inputs"):
        max_seq_length = pop_first_non_none_value(max_seq_length, self.max_seq_length)
        tokens = self.tokenizer.tokenize(text)
        tokens = tokens[: max_seq_length - 2]
        tokens = ["[CLS]"] + tokens + ["[SEP]"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        tokens_ids = tokens_ids[: max_seq_length - 1]

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding

        assert len(tokens_ids) == max_seq_length
        return dict({"tokens_ids": torch.tensor(tokens_ids, dtype=torch.long)})

    @register_process("core/process/unilm_for_next_tokens")
    @add_group_prefix_suffix_for_key
    def for_next_tokens(self, text, max_seq_length=None, group_for_key="net_targets"):
        max_seq_length = pop_first_non_none_value(
            max_seq_length, self.max_gen_seq_length
        )
        tokens = self.tokenizer.tokenize(text)
        tokens = tokens[: max_seq_length - 2]
        tokens = ["[CLS]"] + tokens + ["[SEP]"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        tokens_ids = tokens_ids[1:max_seq_length]
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding

        assert len(tokens_ids) == max_seq_length
        return dict(
            {
                "next_tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "next_tokens_mask": torch.tensor(tokens_mask, dtype=torch.long),
            }
        )

    @register_process("core/process/unilm_for_decode")
    def for_decode(self, tensor, key="hyp"):
        batch_size, num_return_sequences, seq_len = tensor.size()
        tensor = tensor.reshape(-1, seq_len)
        hyp = self.tokenizer.batch_decode(tensor, skip_special_tokens=True)
        hyp = [
            hyp[i : i + num_return_sequences]
            for i in range(0, len(hyp), num_return_sequences)
        ]
        return dict({key: hyp})
