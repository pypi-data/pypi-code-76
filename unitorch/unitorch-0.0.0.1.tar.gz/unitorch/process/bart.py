import os
from functools import partial

import torch
from transformers import BartTokenizer

from unitorch.functions import pop_first_non_none_value
from unitorch.utils.decorators import (
    add_default_section_for_init,
    add_key_group_info_for_process,
    add_group_prefix_suffix_for_key,
)
from unitorch import register_process
from unitorch.core import core_class
from unitorch.utils.hf import hf_cached_path
from unitorch.generation.bart import CORE_BART_PRETRAINED_DICT, VOCABS_KEY, MERGES_KEY


def get_bart_tokenizer(vocab_path, merge_path):
    assert os.path.exists(vocab_path) and os.path.exists(merge_path)
    tokenizer = BartTokenizer(vocab_path, merge_path)
    return tokenizer


class Bart(core_class):
    def __init__(
        self,
        vocab_path=None,
        merge_path=None,
        max_seq_length=128,
        max_gen_seq_length=48,
    ):
        self.tokenizer = get_bart_tokenizer(
            vocab_path,
            merge_path,
        )
        self.max_seq_length = max_seq_length
        self.max_gen_seq_length = max_gen_seq_length

    @classmethod
    @add_default_section_for_init("core/process/bart")
    def init_from_core_configure(cls, cfg, **kwargs):
        pretrained_name = cfg.getdefault(
            "core/process/bart", "pretrained_name", "default-bart"
        )
        vocab_name_or_path = cfg.getdefault(
            "core/process/bart", "vocab_name_or_path", pretrained_name
        )
        vocab_path = (
            CORE_BART_PRETRAINED_DICT[vocab_name_or_path][VOCABS_KEY]
            if vocab_name_or_path in CORE_BART_PRETRAINED_DICT
            else vocab_name_or_path
        )
        vocab_path = hf_cached_path(vocab_path)

        merge_name_or_path = cfg.getdefault(
            "core/process/bart", "merge_name_or_path", pretrained_name
        )
        merge_path = (
            CORE_BART_PRETRAINED_DICT[merge_name_or_path][MERGES_KEY]
            if merge_name_or_path in CORE_BART_PRETRAINED_DICT
            else merge_name_or_path
        )

        merge_path = hf_cached_path(merge_path)
        return dict(
            {
                "vocab_path": vocab_path,
                "merge_path": merge_path,
            }
        )

    @add_key_group_info_for_process(
        group_info=dict(
            name="core/process/bart_for_generation",
            net_inputs=[
                "tokens_ids_a",
                "tokens_mask_a",
                "tokens_ids_b",
                "tokens_mask_b",
            ],
            net_targets=["next_tokens_ids", "next_tokens_mask"],
        )
    )
    @register_process("core/process/bart_for_generation")
    def for_generation(
        self, text_a, text_b=None, max_seq_length=None, max_gen_seq_length=None
    ):
        max_seq_length = pop_first_non_none_value(max_seq_length, self.max_seq_length)
        max_gen_seq_length = pop_first_non_none_value(
            max_gen_seq_length, self.max_gen_seq_length
        )
        tokens_a = self.tokenizer.tokenize(text_a)
        tokens_a = ["<s>"] + tokens_a[: max_seq_length - 2] + ["</s>"]
        tokens_ids_a = self.tokenizer.convert_tokens_to_ids(tokens_a)

        tokens_mask_a = [1] * len(tokens_ids_a)
        padding_a = [0] * (max_seq_length - len(tokens_ids_a))
        tokens_ids_a += [1] * len(padding_a)
        tokens_mask_a += padding_a

        assert len(tokens_ids_a) == max_seq_length
        if text_b is None:
            return dict(
                {
                    "tokens_ids_a": torch.tensor(tokens_ids_a, dtype=torch.long),
                    "tokens_mask_a": torch.tensor(tokens_mask_a, dtype=torch.long),
                }
            )

        tokens_b = self.tokenizer.tokenize(text_b)
        tokens_b = ["</s>"] + tokens_b[: max_gen_seq_length - 2] + ["</s>"]
        tokens_ids_b = self.tokenizer.convert_tokens_to_ids(tokens_b)
        tokens_b_len = len(tokens_ids_b)

        _tokens_ids_b = tokens_ids_b[: tokens_b_len - 1]
        _next_tokens_ids_b = tokens_ids_b[1:tokens_b_len]
        _next_tokens_mask_b = [1] * len(_tokens_ids_b)

        padding_b = [0] * (max_gen_seq_length - len(_tokens_ids_b))
        _tokens_ids_b += [1] * len(padding_b)
        _tokens_mask_b = [1] * (tokens_b_len - 1) + padding_b
        _next_tokens_ids_b += [1] * len(padding_b)
        _next_tokens_mask_b += padding_b
        assert len(_tokens_ids_b) == max_gen_seq_length
        assert len(_next_tokens_ids_b) == max_gen_seq_length
        assert len(_next_tokens_mask_b) == max_gen_seq_length

        return dict(
            {
                "tokens_ids_a": torch.tensor(tokens_ids_a, dtype=torch.long),
                "tokens_mask_a": torch.tensor(tokens_mask_a, dtype=torch.long),
                "tokens_ids_b": torch.tensor(_tokens_ids_b, dtype=torch.long),
                "tokens_mask_b": torch.tensor(_tokens_mask_b, dtype=torch.long),
                "next_tokens_ids": torch.tensor(_next_tokens_ids_b, dtype=torch.long),
                "next_tokens_mask": torch.tensor(_next_tokens_mask_b, dtype=torch.long),
            }
        )

    @register_process("core/process/bart_for_tokens")
    @add_group_prefix_suffix_for_key
    def for_tokens(self, text, max_seq_length=None, group_for_key="net_inputs"):
        max_seq_length = pop_first_non_none_value(max_seq_length, self.max_seq_length)
        tokens = self.tokenizer.tokenize(text)
        tokens = tokens[: max_seq_length - 2]
        tokens = ["</s>"] + tokens + ["</s>"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        tokens_ids = tokens_ids[: max_seq_length - 1]
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding

        assert len(tokens_ids) == max_seq_length
        assert len(tokens_mask) == max_seq_length
        return dict(
            {
                "tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "tokens_mask": torch.tensor(tokens_mask, dtype=torch.long),
            }
        )

    @register_process("core/process/bart_for_next_tokens")
    @add_group_prefix_suffix_for_key
    def for_next_tokens(
        self, text, max_gen_seq_length=None, group_for_key="net_targets"
    ):
        max_gen_seq_length = pop_first_non_none_value(
            max_gen_seq_length, self.max_gen_seq_length
        )
        tokens = self.tokenizer.tokenize(text)
        tokens = tokens[: max_gen_seq_length - 2]
        tokens = ["</s>"] + tokens + ["</s>"]
        tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        tokens_ids = tokens_ids[1:max_gen_seq_length]
        tokens_mask = [1] * len(tokens_ids)

        padding = [0] * (max_gen_seq_length - len(tokens_ids))
        tokens_ids += padding
        tokens_mask += padding

        assert len(tokens_ids) == max_gen_seq_length
        assert len(tokens_mask) == max_gen_seq_length
        return dict(
            {
                "next_tokens_ids": torch.tensor(tokens_ids, dtype=torch.long),
                "next_tokens_mask": torch.tensor(tokens_mask, dtype=torch.long),
            }
        )

    @register_process("core/process/bart_for_decode")
    def for_decode(self, tensor, key="hyp"):
        batch_size, num_return_sequences, seq_len = tensor.size()
        tensor = tensor.reshape(-1, seq_len)
        hyp = self.tokenizer.batch_decode(tensor)
        hyp = [
            hyp[i : i + num_return_sequences]
            for i in range(0, len(hyp), num_return_sequences)
        ]
        return dict({key: hyp})
