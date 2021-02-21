import os
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from torch import device
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BartModel, BartConfig
from transformers.models.bart.modeling_bart import (
    BartAttention,
    BartEncoder,
    BartDecoder,
)
from unitorch.modules.generation_mixin_v2 import GenerationMixinV2
from transformers.modeling_outputs import Seq2SeqLMOutput
from unitorch import add_core_pretrained_dict, register_model
from unitorch.utils.decorators import (
    generation_model_decorator,
    add_net_outputs_for_core_model,
    add_default_section_for_init,
    add_default_section_for_instance_function,
    replace,
)
from unitorch.core import core_model_class
from unitorch.utils.hf import hf_cached_path

CONFIG_KEY = "config"
CONFIG_NAME = "config.json"

MERGES_KEY = "merge"
MERGES_NAME = "merge.txt"

VOCABS_KEY = "vocab"
VOCABS_NAME = "vocab.json"

CORE_BART_PRETRAINED_DICT = {
    "default-bart": {
        "config": "https://huggingface.co/facebook/bart-base/resolve/main/config.json",
        "vocab": "https://huggingface.co/facebook/bart-base/resolve/main/vocab.json",
        "merge": "https://huggingface.co/facebook/bart-base/resolve/main/merges.txt",
    },
    "bart-base": {
        "config": "https://huggingface.co/facebook/bart-base/resolve/main/config.json",
        "vocab": "https://huggingface.co/facebook/bart-base/resolve/main/vocab.json",
        "merge": "https://huggingface.co/facebook/bart-base/resolve/main/merges.txt",
        "weight": "https://huggingface.co/facebook/bart-base/resolve/main/pytorch_model.bin",
    },
    "bart-large": {
        "config": "https://huggingface.co/facebook/bart-large/resolve/main/config.json",
        "vocab": "https://huggingface.co/facebook/bart-large/resolve/main/vocab.json",
        "merge": "https://huggingface.co/facebook/bart-large/resolve/main/merges.txt",
        "weight": "https://huggingface.co/facebook/bart-large/resolve/main/pytorch_model.bin",
    },
}

add_core_pretrained_dict(CORE_BART_PRETRAINED_DICT)


@replace(BartAttention)
class BartAttentionV2(BartAttention):
    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        dropout: float = 0.0,
        is_decoder: bool = False,
        bias: bool = True,
    ):
        super().__init__(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout=dropout,
            is_decoder=is_decoder,
            bias=bias,
        )

    def forward(
        self,
        hidden_states: torch.Tensor,
        key_value_states: Optional[torch.Tensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor]] = None,
        attention_mask: Optional[torch.Tensor] = None,
        layer_head_mask: Optional[torch.Tensor] = None,
        output_attentions: bool = False,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor]]]:
        """Input shape: Batch x Time x Channel"""

        # if key_value_states are provided this layer is used as a cross-attention layer
        # for the decoder
        is_cross_attention = key_value_states is not None
        bsz, tgt_len, embed_dim = hidden_states.size()
        kv_bsz = bsz

        # get query proj
        query_states = self.q_proj(hidden_states) * self.scaling
        # get key, value proj
        if is_cross_attention and past_key_value is not None:
            # reuse k,v, cross_attentions
            key_states = past_key_value[0]
            value_states = past_key_value[1]
            kv_bsz = key_states.size(0)
        elif is_cross_attention:
            # cross_attentions
            kv_bsz = key_value_states.size(0)
            key_states = self._shape(self.k_proj(key_value_states), -1, kv_bsz)
            value_states = self._shape(self.v_proj(key_value_states), -1, kv_bsz)
        elif past_key_value is not None:
            # reuse k, v, self_attention
            key_states = self._shape(self.k_proj(hidden_states), -1, bsz)
            value_states = self._shape(self.v_proj(hidden_states), -1, bsz)
            key_states = torch.cat([past_key_value[0], key_states], dim=2)
            value_states = torch.cat([past_key_value[1], value_states], dim=2)
        else:
            # self_attention
            key_states = self._shape(self.k_proj(hidden_states), -1, bsz)
            value_states = self._shape(self.v_proj(hidden_states), -1, bsz)

        if self.is_decoder:
            # if cross_attention save Tuple(torch.Tensor, torch.Tensor) of all cross attention key/value_states.
            # Further calls to cross_attention layer can then reuse all cross-attention
            # key/value_states (first "if" case)
            # if uni-directional self-attention (decoder) save Tuple(torch.Tensor, torch.Tensor) of
            # all previous decoder key/value_states. Further calls to uni-directional self-attention
            # can concat previous decoder key/value_states to current projected key/value_states (third "elif" case)
            # if encoder bi-directional self-attention `past_key_value` is always `None`
            past_key_value = (key_states, value_states)

        proj_shape = (bsz * self.num_heads, -1, self.head_dim)
        query_states = self._shape(query_states, tgt_len, bsz).view(*proj_shape)
        kv_proj_shape = (kv_bsz * self.num_heads, -1, self.head_dim)
        key_states = key_states.view(*kv_proj_shape)
        value_states = value_states.view(*kv_proj_shape)

        src_len = key_states.size(1)

        if is_cross_attention and kv_bsz != bsz:
            attn_weights = torch.einsum(
                "bxhtd,bhsd->bxhts",
                query_states.view(kv_bsz, -1, self.num_heads, *query_states.size()[1:]),
                key_states.view(kv_bsz, self.num_heads, *key_states.size()[1:]),
            )
            attn_weights = attn_weights.reshape(-1, *attn_weights.size()[-2:])
        else:
            attn_weights = torch.bmm(query_states, key_states.transpose(1, 2))

        assert attn_weights.size() == (
            bsz * self.num_heads,
            tgt_len,
            src_len,
        ), f"Attention weights should be of size {(bsz * self.num_heads, tgt_len, src_len)}, but is {attn_weights.size()}"

        if attention_mask is not None:
            assert attention_mask.size() == (
                bsz,
                1,
                tgt_len,
                src_len,
            ), f"Attention mask should be of size {(bsz, 1, tgt_len, src_len)}, but is {attention_mask.size()}"
            attn_weights = (
                attn_weights.view(bsz, self.num_heads, tgt_len, src_len)
                + attention_mask
            )
            attn_weights = attn_weights.view(bsz * self.num_heads, tgt_len, src_len)

        attn_weights = F.softmax(attn_weights, dim=-1)

        if layer_head_mask is not None:
            assert layer_head_mask.size() == (
                self.num_heads,
            ), f"Head mask for a single layer should be of size {(self.num_heads,)}, but is {layer_head_mask.size()}"
            attn_weights = layer_head_mask.view(1, -1, 1, 1) * attn_weights.view(
                bsz, self.num_heads, tgt_len, src_len
            )
            attn_weights = attn_weights.view(bsz * self.num_heads, tgt_len, src_len)

        if output_attentions:
            # this operation is a bit akward, but it's required to
            # make sure that attn_weights keeps its gradient.
            # In order to do so, attn_weights have to reshaped
            # twice and have to be reused in the following
            attn_weights_reshaped = attn_weights.view(
                bsz, self.num_heads, tgt_len, src_len
            )
            attn_weights = attn_weights_reshaped.view(
                bsz * self.num_heads, tgt_len, src_len
            )
        else:
            attn_weights_reshaped = None

        attn_probs = F.dropout(attn_weights, p=self.dropout, training=self.training)

        if is_cross_attention and bsz != kv_bsz:
            attn_probs = attn_probs.to(value_states.dtype)
            attn_output = torch.einsum(
                "bxhts,bhsd->bxhtd",
                attn_probs.view(kv_bsz, -1, self.num_heads, *attn_probs.size()[1:]),
                value_states.view(kv_bsz, self.num_heads, *value_states.size()[1:]),
            )
            attn_output = attn_output.reshape(-1, *attn_output.size()[-2:])
        else:
            attn_probs = attn_probs.to(value_states.dtype)
            attn_output = torch.bmm(attn_probs, value_states)

        assert attn_output.size() == (
            bsz * self.num_heads,
            tgt_len,
            self.head_dim,
        ), f"`attn_output` should be of size {(bsz, self.num_heads, tgt_len, self.head_dim)}, but is {attn_output.size()}"

        attn_output = (
            attn_output.view(bsz, self.num_heads, tgt_len, self.head_dim)
            .transpose(1, 2)
            .reshape(bsz, tgt_len, embed_dim)
        )

        attn_output = self.out_proj(attn_output)

        return attn_output, attn_weights_reshaped, past_key_value


class Bart(core_model_class):
    def __init__(self, config_path, **kwargs):
        super().__init__()
        self.config_path = config_path
        params = json.load(open(self.config_path, "r"))
        self.config = BartConfig(**params)

    def save_checkpoint(self, ckpt_dir="./cache", **kwargs):
        if not os.path.exists(ckpt_dir):
            os.mkdir(ckpt_dir)
        config_path = os.path.join(ckpt_dir, CONFIG_NAME)
        with open(config_path, "w") as f:
            f.write(open(self.config_path, "r").read())

        super().save_checkpoint(ckpt_dir=ckpt_dir, **kwargs)

    def from_checkpoint(self, ckpt_dir="./cache", **kwargs):
        super().from_checkpoint(ckpt_dir=ckpt_dir, **kwargs)


@register_model("core/model/bart_for_generation", generation_model_decorator)
class BartForGeneration(Bart, GenerationMixinV2):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.shared = nn.Embedding(
            self.config.vocab_size, self.config.d_model, self.config.pad_token_id
        )
        self.encoder = BartEncoder(self.config, self.shared)
        self.decoder = BartDecoder(self.config, self.shared)

        self.init_weights()

    def get_input_embeddings(self):
        return self.shared

    def set_input_embeddings(self, value):
        self.shared = value
        self.encoder.embed_tokens = self.shared
        self.decoder.embed_tokens = self.shared

    def get_encoder(self):
        return self.encoder

    def get_decoder(self):
        return self.decoder

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
    @add_default_section_for_init("core/model/bart")
    def init_from_core_configure(cls, cfg, **kwargs):
        pretrained_name = cfg.getdefault(
            "core/model/bart", "pretrained_name", "default-bart"
        )
        config_name_or_path = cfg.getdefault(
            "core/model/bart", "config_name_or_path", pretrained_name
        )
        config_path = (
            CORE_BART_PRETRAINED_DICT[config_name_or_path][CONFIG_KEY]
            if config_name_or_path in CORE_BART_PRETRAINED_DICT
            else config_name_or_path
        )

        config_path = hf_cached_path(config_path)

        inst = cls(config_path)
        if pretrained_name is not None:
            inst.from_pretrained(pretrained_name)

        return inst

    def prepare_inputs_for_generation(
        self,
        decoder_input_ids,
        past=None,
        attention_mask=None,
        head_mask=None,
        use_cache=None,
        encoder_outputs=None,
        **kwargs,
    ):
        decoder_length = decoder_input_ids.size(1)
        if past is not None:
            decoder_input_ids = decoder_input_ids[:, -1:]

        if decoder_length == 1:
            encoder_hidden_states = encoder_outputs.last_hidden_state
            encoder_hidden_states = encoder_hidden_states.view(
                -1, self.num_beams, *encoder_hidden_states.size()[1:]
            )
            encoder_hidden_states = encoder_hidden_states[:, 0]
            encoder_outputs.last_hidden_state = encoder_hidden_states

        return {
            "decoder_input_ids": decoder_input_ids,
            "attention_mask": attention_mask,
            "encoder_outputs": encoder_outputs,
            "decoder_length": decoder_length,
            "past_key_values": past,
        }

    @staticmethod
    def _reorder_cache(past, beam_idx):
        reordered_past = ()
        for layer_past in past:
            # cached cross_attention states don't have to be reordered -> they are always the same
            reordered_past += (
                tuple(
                    past_state.index_select(0, beam_idx)
                    for past_state in layer_past[:2]
                )
                + layer_past[2:],
            )
        return reordered_past

    @staticmethod
    def _reorder_cache_v2(past, batch_idx, beam_idx):
        if batch_idx is None:
            return _reorder_cache(past, beam_idx)
        reordered_past = ()
        for layer_past in past:
            # cached cross_attention states don't have to be reordered -> they are always the same
            past_state1 = tuple(
                [past_state.index_select(0, beam_idx) for past_state in layer_past[:2]]
            )
            past_state2 = tuple(
                [past_state.index_select(0, batch_idx) for past_state in layer_past[2:]]
            )
            reordered_past += (past_state1 + past_state2,)

        return reordered_past

    def forward(
        self,
        tokens_ids_a=None,
        tokens_mask_a=None,
        tokens_ids_b=None,
        tokens_mask_b=None,
        decoder_input_ids=None,
        attention_mask=None,
        encoder_outputs=None,
        past_key_values=None,
        output_attentions=None,
        output_hidden_states=None,
        decoder_length=None,
        return_dict=None,
    ):
        if self.training:
            encoder_outputs = self.encoder(tokens_ids_a, attention_mask=tokens_mask_a)
            decoder_outputs = self.decoder(
                input_ids=tokens_ids_b,
                attention_mask=tokens_mask_b,
                encoder_hidden_states=encoder_outputs[0],
                encoder_attention_mask=tokens_mask_a,
            )
            logits = F.linear(decoder_outputs[0], self.shared.weight)
            return logits
        batch_size = decoder_input_ids.size(0)
        decoder_attention_mask = torch.ones(batch_size, decoder_length).to(
            decoder_input_ids
        )
        outputs = self.decoder(
            input_ids=decoder_input_ids,
            attention_mask=decoder_attention_mask,
            encoder_hidden_states=encoder_outputs.last_hidden_state,
            encoder_attention_mask=attention_mask,
            use_cache=True,
            past_key_values=past_key_values,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        logits = F.linear(outputs[0], self.shared.weight)
        past_key_values = outputs[1]
        return Seq2SeqLMOutput(logits=logits, past_key_values=past_key_values)

    @add_default_section_for_instance_function("core/model/bart")
    def generate(
        self,
        tokens_ids,
        tokens_mask,
        num_beams=5,
        decoder_start_token_id=2,
        decoder_end_token_id=2,
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
        batch_hyp = super().generate(
            tokens_ids,
            max_length=max_gen_seq_length,
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
            return batch_hyp[:, :, :max_gen_seq_length]
        batch_ret = torch.zeros(
            batch_hyp.size(0), num_return_sequences, max_gen_seq_length
        )
        batch_ret[:, :, : batch_hyp.size(-1)].copy_(batch_hyp)
        return batch_ret.long()
