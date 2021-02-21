import os
import torch
import math
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from collections import OrderedDict
from torch import Tensor, device
import json
import random
from functools import partial
import numpy as np
import torch.nn as nn
import torch.nn.functional as F

from unitorch import add_core_pretrained_dict, register_model
from unitorch.core import core_model_class
from unitorch.utils.hf import hf_cached_path
from unitorch.modules.generation_mixin_v2 import GenerationMixinV2
from transformers import PretrainedConfig, PreTrainedModel
from transformers.models.bert.modeling_bert import (
    BertEmbeddings,
    BertIntermediate,
    BertOutput,
    BertPooler,
    BertPreTrainingHeads,
    BertPreTrainedModel,
    BertSelfOutput,
)
from transformers.modeling_outputs import Seq2SeqLMOutput
from transformers.modeling_utils import apply_chunking_to_forward
from transformers.file_utils import ModelOutput

from unitorch.utils.decorators import (
    generation_model_decorator,
    add_default_section_for_init,
    add_default_section_for_instance_function,
    replace,
)

CONFIG_KEY = "config"
CONFIG_NAME = "config.json"

VOCABS_KEY = "vocab"
VOCABS_NAME = "vocab.txt"

CORE_UNILM_PRETRAINED_DICT = {
    "default-unilm": {
        "config": "https://huggingface.co/fuliucansheng/unilm/resolve/main/unilm-base-uncased-config.json",
        "vocab": "https://unilm.blob.core.windows.net/ckpt/unilm1.2-base-uncased-vocab.txt",
    },
    "unilm-base-uncased": {
        "config": "https://huggingface.co/fuliucansheng/unilm/resolve/main/unilm-base-uncased-config.json",
        "vocab": "https://unilm.blob.core.windows.net/ckpt/unilm1.2-base-uncased-vocab.txt",
        "weight": "https://unilm.blob.core.windows.net/ckpt/unilm1.2-base-uncased.bin",
    },
}

add_core_pretrained_dict(CORE_UNILM_PRETRAINED_DICT)


def _reorder_buffer(attn_cache, beam_idx):
    for k, input_buffer_k in attn_cache.items():
        if input_buffer_k is not None and "prefix_" not in k:
            attn_cache[k] = input_buffer_k.index_select(0, beam_idx)
    return attn_cache


def _reorder_buffer_v2(attn_cache, batch_idx, beam_idx):
    for k, input_buffer_k in attn_cache.items():
        if input_buffer_k is not None:
            if "prefix_" in k:
                attn_cache[k] = (
                    input_buffer_k
                    if batch_idx is None
                    else input_buffer_k.index_select(0, batch_idx)
                )
            else:
                attn_cache[k] = (
                    input_buffer_k
                    if beam_idx is None
                    else input_buffer_k.index_select(0, beam_idx)
                )
    return attn_cache


class UnilmConfig(PretrainedConfig):
    def __init__(
        self,
        vocab_size=28996,
        hidden_size=768,
        num_hidden_layers=12,
        num_attention_heads=12,
        intermediate_size=3072,
        hidden_act="gelu",
        hidden_dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        max_position_embeddings=512,
        type_vocab_size=6,
        initializer_range=0.02,
        layer_norm_eps=1e-12,
        source_type_id=0,
        target_type_id=1,
        bos_token_id=101,
        mask_token_id=103,
        eos_token_id=102,
        pad_token_id=0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.bos_token_id = bos_token_id
        self.mask_token_id = mask_token_id
        self.eos_token_id = eos_token_id
        self.pad_token_id = pad_token_id
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.hidden_act = hidden_act
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_position_embeddings = max_position_embeddings
        self.type_vocab_size = type_vocab_size
        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps
        self.source_type_id = source_type_id
        self.target_type_id = target_type_id
        self.use_cache = True

        if isinstance(vocab_size, str) or (
            sys.version_info[0] == 2 and isinstance(vocab_size, unicode)
        ):
            with open(vocab_size, "r", encoding="utf-8") as reader:
                json_config = json.loads(reader.read())
                for key, value in json_config.items():
                    self.__dict__[key] = value
        elif isinstance(vocab_size, int):
            self.vocab_size = vocab_size
        else:
            raise ValueError(
                "First argument must be either a vocabulary size (int)"
                " or the path to a pretrained model config file (str)"
            )


class BertSelfAttention(nn.Module):
    """
    An optimized bert self attn to unilm for faster generation
    """

    def __init__(self, config):
        super(BertSelfAttention, self).__init__()
        if config.hidden_size % config.num_attention_heads != 0:
            raise ValueError(
                "The hidden size (%d) is not a multiple of the number of attention "
                "heads (%d)" % (config.hidden_size, config.num_attention_heads)
            )
        self.output_attentions = config.output_attentions

        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = int(config.hidden_size / config.num_attention_heads)
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Linear(config.hidden_size, self.all_head_size)
        self.key = nn.Linear(config.hidden_size, self.all_head_size)
        self.value = nn.Linear(config.hidden_size, self.all_head_size)

        self.dropout = nn.Dropout(config.attention_probs_dropout_prob)

    def transpose_for_scores(self, x):
        new_x_shape = x.size()[:-1] + (
            self.num_attention_heads,
            self.attention_head_size,
        )
        x = x.view(*new_x_shape)
        return x.permute(0, 2, 1, 3)

    def forward(
        self, hidden_states, attention_mask, head_mask=None, history_states=None
    ):
        """
        Args:
            - hidden_states: last layer output or embedding output
            - attention_mask: mask for tokens per batch
            - history_states: a optimized cache dict for beam search inference
        Shape:
            - hidden_states: (N, S + L, E) for training, (N, 2, E) for cached beam search inference
            - history_states is a optimized cache dict for beam search inference
                - past_prefix_key_layer: (N, S, E)
                - past_prefix_value_layer: (N, S, E)
                - past_key_layer: (N * B, L, E)
                - past_value_layer: (N * B, L, E)
            Note: S is the source sequence length, L is the target sequence length, N is the batch size, E is the embedding dimension, B is the beam size
        """
        new_query_layer = self.query(hidden_states)
        new_key_layer = self.key(hidden_states)
        new_value_layer = self.value(hidden_states)

        past_prefix_key_layer = history_states.get("past_prefix_key_layer")
        past_prefix_value_layer = history_states.get("past_prefix_value_layer")
        past_key_layer = history_states.get("past_key_layer")
        past_value_layer = history_states.get("past_value_layer")

        query_layer = self.transpose_for_scores(new_query_layer)
        key_layer = self.transpose_for_scores(new_key_layer)
        value_layer = self.transpose_for_scores(new_value_layer)
        if past_prefix_key_layer is not None:
            prefix_size = past_prefix_key_layer.size()
            prefix_attention_scores = torch.einsum(
                "bxhtd,bhsd->bxhts",
                query_layer.view(prefix_size[0], -1, *query_layer.size()[1:]),
                past_prefix_key_layer,
            )
            prefix_attention_scores = prefix_attention_scores.reshape(
                -1, *prefix_attention_scores.size()[2:]
            )
            if past_key_layer is not None:
                key_layer = torch.cat((past_key_layer, key_layer), dim=2)
                value_layer = torch.cat((past_value_layer, value_layer), dim=2)
            attention_scores = torch.matmul(
                query_layer, key_layer.transpose(-1, -2)
            )
            prefix_attention_scores = prefix_attention_scores / math.sqrt(
                self.attention_head_size
            )
            attention_scores = attention_scores / math.sqrt(
                self.attention_head_size
            )
            attention_scores = torch.cat(
                (prefix_attention_scores, attention_scores), dim=-1
            )
            attention_scores = attention_scores + attention_mask
            attention_probs = nn.Softmax(dim=-1)(attention_scores)
            attention_probs = self.dropout(attention_probs)

            if head_mask is not None:
                attention_probs = attention_probs * head_mask
            prefix_attention_probs = attention_probs[:, :, :, : prefix_size[2]]
            attention_probs = attention_probs[:, :, :, prefix_size[2] :]
            prefix_attention_probs = prefix_attention_probs.to(past_prefix_value_layer.dtype)
            prefix_context_layer = torch.einsum(
                "bxhtd,bhds->bxhts",
                prefix_attention_probs.view(
                    prefix_size[0], -1, *prefix_attention_probs.size()[1:]
                ),
                past_prefix_value_layer,
            )
            prefix_context_layer = prefix_context_layer.reshape(
                -1, *prefix_context_layer.size()[2:]
            )
            context_layer = torch.matmul(attention_probs, value_layer)
            context_layer = prefix_context_layer + context_layer

        else:
            attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
            attention_scores = attention_scores / math.sqrt(self.attention_head_size)
            attention_scores = attention_scores + attention_mask

            attention_probs = nn.Softmax(dim=-1)(attention_scores)
            attention_probs = self.dropout(attention_probs)

            if head_mask is not None:
                attention_probs = attention_probs * head_mask
            context_layer = torch.matmul(attention_probs, value_layer)

        if history_states is None or len(history_states) == 0:
            history_states.update(
                dict(
                    {
                        "past_prefix_key_layer": key_layer,
                        "past_prefix_value_layer": value_layer,
                    }
                )
            )
        else:
            history_states.update(
                dict(
                    {
                        "past_prefix_key_layer": past_prefix_key_layer,
                        "past_prefix_value_layer": past_prefix_value_layer,
                        "past_key_layer": key_layer[:, :, :-1, :],
                        "past_value_layer": value_layer[:, :, :-1, :],
                    }
                )
            )

        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
        context_layer = context_layer.view(*new_context_layer_shape)

        outputs = (
            (context_layer, attention_probs)
            if self.output_attentions
            else (context_layer,)
        )
        return outputs


class BertAttention(nn.Module):
    """
    Bert Attention from Unilm offical repo
    https://github.com/microsoft/unilm/tree/master/s2s-ft
    """

    def __init__(self, config):
        super(BertAttention, self).__init__()
        self.self = BertSelfAttention(config)
        self.output = BertSelfOutput(config)
        self.pruned_heads = set()

    def prune_heads(self, heads):
        if len(heads) == 0:
            return
        mask = torch.ones(self.self.num_attention_heads, self.self.attention_head_size)
        heads = (
            set(heads) - self.pruned_heads
        )  # Convert to set and emove already pruned heads
        for head in heads:
            # Compute how many pruned heads are before the head and move the index accordingly
            head = head - sum(1 if h < head else 0 for h in self.pruned_heads)
            mask[head] = 0
        mask = mask.view(-1).contiguous().eq(1)
        index = torch.arange(len(mask))[mask].long()

        # Prune linear layers
        self.self.query = prune_linear_layer(self.self.query, index)
        self.self.key = prune_linear_layer(self.self.key, index)
        self.self.value = prune_linear_layer(self.self.value, index)
        self.output.dense = prune_linear_layer(self.output.dense, index, dim=1)

        # Update hyper params and store pruned heads
        self.self.num_attention_heads = self.self.num_attention_heads - len(heads)
        self.self.all_head_size = (
            self.self.attention_head_size * self.self.num_attention_heads
        )
        self.pruned_heads = self.pruned_heads.union(heads)

    def forward(
        self, input_tensor, attention_mask, head_mask=None, history_states=None
    ):
        self_outputs = self.self(
            input_tensor, attention_mask, head_mask, history_states=history_states
        )
        attention_output = self.output(self_outputs[0], input_tensor)
        outputs = (attention_output,) + self_outputs[
            1:
        ]  # add attentions if we output them
        return outputs


class BertLayer(nn.Module):
    """
    Bert Layer from Unilm offical repo
    https://github.com/microsoft/unilm/tree/master/s2s-ft
    """

    def __init__(self, config):
        super(BertLayer, self).__init__()
        self.attention = BertAttention(config)
        self.intermediate = BertIntermediate(config)
        self.output = BertOutput(config)

    def forward(
        self, hidden_states, attention_mask, head_mask=None, history_states=None
    ):
        attention_outputs = self.attention(
            hidden_states, attention_mask, head_mask, history_states=history_states
        )
        attention_output = attention_outputs[0]
        intermediate_output = self.intermediate(attention_output)
        layer_output = self.output(intermediate_output, attention_output)
        outputs = (layer_output,) + attention_outputs[
            1:
        ]  # add attentions if we output them
        return outputs


class BertEncoder(nn.Module):
    """
    Bert Encoder from Unilm offical repo
    https://github.com/microsoft/unilm/tree/master/s2s-ft
    """

    def __init__(self, config):
        super(BertEncoder, self).__init__()
        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.layer = nn.ModuleList(
            [BertLayer(config) for _ in range(config.num_hidden_layers)]
        )

    def forward(
        self, hidden_states, attention_mask, head_mask=None, history_states=None
    ):
        all_hidden_states = ()
        all_attentions = ()

        for i, layer_module in enumerate(self.layer):
            layer_outputs = layer_module(
                hidden_states,
                attention_mask,
                head_mask[i],
                history_states=history_states[i],
            )

            if self.output_hidden_states:
                all_hidden_states = all_hidden_states + (hidden_states,)

            hidden_states = layer_outputs[0]
            if self.output_attentions:
                all_attentions = all_attentions + (layer_outputs[1],)

        # Add last layer
        if self.output_hidden_states:
            all_hidden_states = all_hidden_states + (hidden_states,)

        outputs = (hidden_states,)
        if self.output_hidden_states:
            outputs = outputs + (all_hidden_states,)
        if self.output_attentions:
            outputs = outputs + (all_attentions,)
        return outputs  # last-layer hidden state, (all hidden states), (all attentions), (all encoder layers)


class UnilmModel(BertPreTrainedModel):
    """
    Unilm model structure
    """

    def __init__(self, config):
        super().__init__(config)

        self.embeddings = BertEmbeddings(config)
        self.encoder = BertEncoder(config)
        self.pooler = BertPooler(config)

        self.init_weights()

    def _resize_token_embeddings(self, new_num_tokens):
        old_embeddings = self.embeddings.word_embeddings
        new_embeddings = self._get_resized_embeddings(old_embeddings, new_num_tokens)
        self.embeddings.word_embeddings = new_embeddings
        return self.embeddings.word_embeddings

    def _prune_heads(self, heads_to_prune):
        """Prunes heads of the model.
        heads_to_prune: dict of {layer_num: list of heads to prune in this layer}
        See base class PreTrainedModel
        """
        for layer, heads in heads_to_prune.items():
            self.encoder.layer[layer].attention.prune_heads(heads)

    def forward(
        self,
        input_ids,
        token_type_ids=None,
        attention_mask=None,
        position_ids=None,
        head_mask=None,
        history_states=None,
    ):
        if attention_mask is None:
            attention_mask = torch.ones_like(input_ids)
        if token_type_ids is None:
            token_type_ids = torch.zeros_like(input_ids)

        # We create a 3D attention mask from a 2D tensor mask.
        # Sizes are [batch_size, 1, 1, to_seq_length]
        # So we can broadcast to [batch_size, num_heads, from_seq_length, to_seq_length]
        # this attention mask is more simple than the triangular masking of causal attention
        # used in OpenAI GPT, we just need to prepare the broadcast dimension here.
        if attention_mask.dim() == 2:
            extended_attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)
        elif attention_mask.dim() == 3:
            extended_attention_mask = attention_mask.unsqueeze(1)
        else:
            raise NotImplementedError

        # Since attention_mask is 1.0 for positions we want to attend and 0.0 for
        # masked positions, this operation will create a tensor which is 0.0 for
        # positions we want to attend and -10000.0 for masked positions.
        # Since we are adding it to the raw scores before the softmax, this is
        # effectively the same as removing these entirely.
        extended_attention_mask = extended_attention_mask.to(
            dtype=next(self.parameters()).dtype
        )  # fp16 compatibility
        extended_attention_mask = (1.0 - extended_attention_mask) * -10000.0

        # Prepare head mask if needed
        # 1.0 in head_mask indicate we keep the head
        # attention_probs has shape bsz x n_heads x N x N
        # input head_mask has shape [num_heads] or [num_hidden_layers x num_heads]
        # and head_mask is converted to shape [num_hidden_layers x batch x num_heads x seq_length x seq_length]
        if head_mask is not None:
            if head_mask.dim() == 1:
                head_mask = (
                    head_mask.unsqueeze(0).unsqueeze(0).unsqueeze(-1).unsqueeze(-1)
                )
                head_mask = head_mask.expand(
                    self.config.num_hidden_layers, -1, -1, -1, -1
                )
            elif head_mask.dim() == 2:
                head_mask = (
                    head_mask.unsqueeze(1).unsqueeze(-1).unsqueeze(-1)
                )  # We can specify head_mask for each layer
            head_mask = head_mask.to(
                dtype=next(self.parameters()).dtype
            )  # switch to fload if need + fp16 compatibility
        else:
            head_mask = [None] * self.config.num_hidden_layers

        if history_states is None:
            history_states = [
                dict().copy() for _ in range(self.config.num_hidden_layers)
            ]
        embedding_output = self.embeddings(
            input_ids, position_ids=position_ids, token_type_ids=token_type_ids
        )
        encoder_outputs = self.encoder(
            embedding_output,
            extended_attention_mask,
            head_mask=head_mask,
            history_states=history_states,
        )
        sequence_output = encoder_outputs[0]
        pooled_output = self.pooler(sequence_output)

        outputs = (
            (
                sequence_output,
                pooled_output,
            )
            + encoder_outputs[1:]
            + (history_states,)
        )  # add hidden_states and attentions if they are here
        return outputs  # sequence_output, pooled_output, (hidden_states), (attentions), (history_states)


class Unilm(core_model_class):
    def __init__(self, config_path, **kwargs):
        super().__init__()
        self.config_path = config_path
        self.config = UnilmConfig(config_path)

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


@register_model("core/model/unilm_for_generation", generation_model_decorator)
class UnilmForGeneration(Unilm, GenerationMixinV2):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.bert = UnilmModel(self.config)
        self.cls = BertPreTrainingHeads(self.config)
        self.init_weights()

        self.hist_index = (
            int(self.config.output_hidden_states)
            + int(self.config.output_attentions)
            + 2
        )
        self.bert.embeddings.word_embeddings.weight = (
            self.cls.predictions.decoder.weight
        )

    @property
    def device(self) -> device:
        """
        :obj:`torch.device`: The device on which the module is (assuming that all the module parameters are on the same
        device).
        """
        try:
            return next(self.parameters()).device
        except StopIteration:
            # For nn.DataParallel compatibility in PyTorch 1.5

            def find_tensor_attributes(module: nn.Module) -> List[Tuple[str, Tensor]]:
                tuples = [
                    (k, v) for k, v in module.__dict__.items() if torch.is_tensor(v)
                ]
                return tuples

            gen = self._named_members(get_members_fn=find_tensor_attributes)
            first_tuple = next(gen)
            return first_tuple[1].device

    @classmethod
    @add_default_section_for_init("core/model/unilm")
    def init_from_core_configure(cls, cfg, **kwargs):
        pretrained_name = cfg.getdefault(
            "core/model/unilm", "pretrained_name", "default-unilm"
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
        inst = cls(config_path)

        if pretrained_name is not None:
            inst.from_pretrained(pretrained_name)

        return inst

    def forward(
        self,
        tokens_ids=None,
        attn_mask=None,
        seg_ids=None,
        pos_ids=None,
        decoder_input_ids=None,
        decoder_pos_ids=None,
        decoder_seg_ids=None,
        decoder_attn_mask=None,
        decoder_mask_ids=None,
        past_key_values=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        if self.training:
            outputs = self.bert(
                tokens_ids,
                seg_ids,
                attn_mask,
                pos_ids,
            )
            logits = self.cls(outputs[0], outputs[1])[0]
            return logits
        decoder_token = torch.cat([decoder_input_ids, decoder_mask_ids], dim=1)
        decoder_len = decoder_token.size(1)
        decoder_token = decoder_token[:, -2:]
        decoder_mask = decoder_attn_mask[
            :, decoder_len - 2 : decoder_len, : self.prefix_state["prefix_len"] + decoder_len
        ]
        decoder_pos = decoder_pos_ids[:, decoder_len - 2 : decoder_len]
        outputs = self.bert(
            decoder_token,
            decoder_seg_ids,
            decoder_mask,
            decoder_pos,
            history_states=past_key_values,
        )
        logits = self.cls(outputs[0], outputs[1])[0]
        state4cache = [
            decoder_pos_ids,
            decoder_attn_mask,
            decoder_mask_ids,
            decoder_seg_ids,
        ] + outputs[self.hist_index]
        return Seq2SeqLMOutput(logits=logits, past_key_values=state4cache)

    @staticmethod
    def _reorder_cache(past, beam_idx):
        """
        For beam search in huggingface generation mixin
        """
        pos_ids, token_mask, decoder_mask_token, decoder_seg, history_states = (
            past[0],
            past[1],
            past[2],
            past[3],
            past[4:],
        )
        reordered_past = []
        for layer_past in history_states:
            reordered_past.append(_reorder_buffer(layer_past, beam_idx))
        newpast = [pos_ids, token_mask, decoder_mask_token, decoder_seg] + reordered_past
        return newpast

    @staticmethod
    def _reorder_cache_v2(past, batch_idx, beam_idx):
        """
        For faster inference by optimized beam search in generation mixin v2
        """
        pos_ids, token_mask, decoder_mask_token, decoder_seg, history_states = (
            past[0],
            past[1],
            past[2],
            past[3],
            past[4:],
        )
        reordered_past = []
        for layer_past in history_states:
            reordered_past.append(_reorder_buffer_v2(layer_past, batch_idx, beam_idx))
        pos_ids = pos_ids[beam_idx]
        token_mask = token_mask[beam_idx]
        decoder_mask_token = decoder_mask_token[beam_idx]
        decoder_seg = decoder_seg[beam_idx]
        newpast = [pos_ids, token_mask, decoder_mask_token, decoder_seg] + reordered_past
        return newpast

    def prepare_inputs_for_generation(
        self,
        decoder_input_ids,
        past=None,
        **kwargs,
    ):
        if past is None:
            active_batch_size, _ = decoder_input_ids.size()
            prefix_token, prefix_seg, prefix_pos, prefix_mask = (
                self.prefix_state["prefix_token"],
                self.prefix_state["prefix_seg"],
                self.prefix_state["prefix_pos"],
                self.prefix_state["prefix_mask"],
            )
            prefix_len = self.prefix_state["prefix_len"]
            outputs = self.bert(
                prefix_token[:, :prefix_len],
                prefix_seg[:, :prefix_len],
                prefix_mask[:, :prefix_len, :prefix_len],
                prefix_pos[:, :prefix_len],
            )
            token_pos = prefix_pos.repeat(1, self.num_beams).view(
                active_batch_size, prefix_pos.size(1)
            )
            token_pos = token_pos[:, prefix_len:]
            token_mask = (
                prefix_mask.unsqueeze(1)
                .repeat(1, self.num_beams, 1, 1)
                .view(active_batch_size, prefix_mask.size(1), prefix_mask.size(1))
            )
            token_mask = token_mask[:, prefix_len:, :]
            history_states = outputs[self.hist_index]
            decoder_mask_token = (
                torch.ones(active_batch_size, 1).to(decoder_input_ids)
                * self.config.mask_token_id
            )
            decoder_seg_ids = (
                torch.ones(active_batch_size, 2).to(decoder_input_ids)
                * self.config.target_type_id
            )
        else:
            token_pos, token_mask, decoder_mask_token, decoder_seg_ids, history_states = (
                past[0],
                past[1],
                past[2],
                past[3],
                past[4:],
            )
        return {
            "decoder_input_ids": decoder_input_ids,
            "decoder_mask_ids": decoder_mask_token,
            "decoder_attn_mask": token_mask,
            "decoder_seg_ids": decoder_seg_ids,
            "decoder_pos_ids": token_pos,
            "past_key_values": history_states,
        }

    @add_default_section_for_instance_function("core/model/unilm")
    def generate(
        self,
        tokens_ids,
        num_beams=5,
        decoder_start_token_id=101,
        decoder_end_token_id=102,
        num_return_sequences=1,
        min_gen_seq_length=0,
        max_gen_seq_length=48,
        repetition_penalty=1.0,
        no_repeat_ngram_size=0,
        early_stopping=True,
        length_penalty=1.0,
        num_beam_groups=1,
        diversity_penalty=0.0,
        diverse_rate=0.0,
    ):
        self.num_beams = num_beams
        prefix_token = tokens_ids
        prefix_mask1 = tokens_ids.ne(self.config.pad_token_id).long()
        batch_size, prefix_len = prefix_token.size()
        total_seq_length = max_gen_seq_length + prefix_len + 1
        prefix_mask = prefix_mask1[:, None, :].repeat(1, total_seq_length, 1)
        new_mask = torch.zeros(batch_size, total_seq_length, max_gen_seq_length + 1).to(
            prefix_mask
        )
        tri_mask = torch.ones(batch_size, total_seq_length, max_gen_seq_length + 1).to(
            prefix_mask
        )
        new_mask[:, prefix_len:, :] = torch.tril(tri_mask[:, prefix_len:, :])
        new_mask[:, :, 0] = 0
        prefix_mask = torch.cat((prefix_mask, new_mask), dim=-1)
        prefix_seg = torch.tensor([0] * prefix_len).to(prefix_token)
        prefix_seg = prefix_seg[None, :].repeat(batch_size, 1)
        prefix_pos0 = torch.ones(batch_size, max_gen_seq_length + 1).to(tokens_ids)
        prefix_pos0[:, 0] = 0
        prefix_pos = torch.cat((tokens_ids, prefix_pos0.to(tokens_ids)), dim=-1).ne(
            self.config.pad_token_id
        )
        prefix_pos = torch.cumsum(prefix_pos, dim=-1) - 1
        self.prefix_state = dict(
            {
                "prefix_len": prefix_len,
                "prefix_token": prefix_token,
                "prefix_seg": prefix_seg,
                "prefix_mask": prefix_mask,
                "prefix_pos": prefix_pos,
            }
        )
        decoder_seg = torch.ones(batch_size * self.num_beams, 1).to(prefix_token)
        decoder_seg[:, 0] = 0
        decoder_mask_token = torch.ones(batch_size * self.num_beams, 1).to(prefix_token) * self.config.mask_token_id
        if decoder_start_token_id is not None:
            self.config.bos_token_id = decoder_start_token_id
        decoder_input_ids = torch.ones(batch_size, 1).to(prefix_token) * self.config.bos_token_id
        batch_hyp = super().generate(
            decoder_input_ids,
            max_length=max_gen_seq_length - 1,
            min_length=min_gen_seq_length,
            num_beams=num_beams,
            do_sample=False,
            decoder_start_token_id=decoder_start_token_id,
            no_repeat_ngram_size=no_repeat_ngram_size,
            early_stopping=early_stopping,
            length_penalty=length_penalty,
            repetition_penalty=repetition_penalty,
            num_return_sequences=num_return_sequences,
            bos_token_id=decoder_start_token_id,
            eos_token_id=decoder_end_token_id,
            num_beam_groups=num_beam_groups,
            diversity_penalty=diversity_penalty,
        )
        batch_hyp = batch_hyp.reshape(-1, num_return_sequences, batch_hyp.size(-1))
        if batch_hyp.size(-1) >= max_gen_seq_length:
            return batch_hyp[:, :, :max_gen_seq_length].long()
        batch_ret = torch.zeros(
            batch_hyp.size(0), num_return_sequences, max_gen_seq_length
        )
        batch_ret[:, :, : batch_hyp.size(-1)].copy_(batch_hyp)
        return batch_ret.long()
