import torch
import numpy as np
import torch.nn.functional as F
from itertools import accumulate
from collections import UserDict
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union
from transformers.generation_beam_search import BeamScorer, BeamSearchScorer
from transformers.generation_logits_process import (
    LogitsProcessorList,
    NoRepeatNGramLogitsProcessor,
    LogitsProcessor,
)
from transformers.generation_utils import GenerationMixin, BeamSearchOutput
from unitorch.utils.decorators import replace
from unitorch.ops.ngram_repeat_block import NGramRepeatBlock


@replace(NoRepeatNGramLogitsProcessor)
class NoRepeatNGramLogitsProcessorV2(LogitsProcessor):
    r"""
    :class:`transformers.LogitsProcessor` that enforces no repetition of n-grams. See `Fairseq
    <https://github.com/pytorch/fairseq/blob/a07cb6f40480928c9e0548b737aadd36ee66ac76/fairseq/sequence_generator.py#L345>`__.
    Args:
        ngram_size (:obj:`int`):
            All ngrams of size :obj:`ngram_size` can only occur once.
    """

    def __init__(self, ngram_size: int):
        if not isinstance(ngram_size, int) or ngram_size <= 0:
            raise ValueError(
                f"`ngram_size` has to be a strictly positive integer, but is {ngram_size}"
            )
        self.ngram_size = ngram_size
        self.no_repeat_ngram_op = NGramRepeatBlock()

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor
    ) -> torch.FloatTensor:
        num_batch_hypotheses = scores.shape[0]
        cur_len = input_ids.shape[-1]
        """
        banned_batch_tokens = _calc_banned_ngram_tokens(self.ngram_size, input_ids, num_batch_hypotheses, cur_len)

        for i, banned_tokens in enumerate(banned_batch_tokens):
            scores[i, banned_tokens] = -float("inf")
        """
        scores = self.no_repeat_ngram_op(
            input_ids,
            scores.float(),
            num_batch_hypotheses,
            cur_len - 1,
            1,
            self.ngram_size,
        )

        return scores


@replace(BeamSearchScorer)
class BeamSearchScorerV2(BeamSearchScorer):
    def __init__(
        self,
        batch_size: int,
        max_length: int,
        num_beams: int,
        device: torch.device,
        length_penalty: Optional[float] = 1.0,
        do_early_stopping: Optional[bool] = False,
        num_beam_hyps_to_keep: Optional[int] = 1,
        num_beam_groups: Optional[int] = 1,
        use_reorder_cache_v2: Optional[bool] = False,
    ):
        super().__init__(
            batch_size,
            max_length,
            num_beams,
            device,
            length_penalty,
            do_early_stopping,
            num_beam_hyps_to_keep,
            num_beam_groups,
        )
        self.use_reorder_cache_v2 = use_reorder_cache_v2
        self.beams_offset = (
            (torch.arange(0, batch_size) * num_beams).unsqueeze(1).to(device)
        )
        self.cand_size = 2 * num_beams
        self.cand_offsets = torch.arange(0, self.cand_size).to(device)

    def process(
        self,
        input_ids: torch.LongTensor,
        next_scores: torch.FloatTensor,
        next_tokens: torch.LongTensor,
        next_indices: torch.LongTensor,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
    ) -> Tuple[torch.Tensor]:
        cur_len = input_ids.shape[-1]
        batch_size = input_ids.shape[0] // self.group_size

        next_tokens_id = next_tokens
        next_beams_id = next_indices
        effective_beam_id = next_beams_id + self.beams_offset

        if eos_token_id is not None:
            eos_mask = next_tokens.eq(eos_token_id)
        else:
            eos_mask = torch.zeros_like(next_tokens).bool()
        eos_effective_idx = torch.masked_select(
            effective_beam_id[:, : self.num_beams], mask=eos_mask[:, : self.num_beams]
        )

        finished_batch_idxs = []
        if self.use_reorder_cache_v2 and eos_effective_idx.numel() > 0:
            eos_effective_scores = torch.masked_select(
                next_scores[:, : self.num_beams], mask=eos_mask[:, : self.num_beams]
            )
            input_clone = input_ids.index_select(0, eos_effective_idx)
            unfin_offset = np.array(list(accumulate(map(int, self._done))))[
                np.array(list(map(int, self._done))) == 0
            ]
            for i in range(eos_effective_idx.size(0)):
                eos_idx = eos_effective_idx[i]
                eos_score = eos_effective_scores[i]
                unfin_batch_idx = eos_idx // self.num_beams
                batch_idx = unfin_batch_idx + unfin_offset[unfin_batch_idx]
                if not self._done[batch_idx]:
                    self._beam_hyps[batch_idx.item()].add(
                        input_clone[i], eos_score.item()
                    )
                is_done = bool(self._done[batch_idx])
                self._done[batch_idx] = self._done[batch_idx] or self._beam_hyps[
                    batch_idx
                ].is_done(next_scores[unfin_batch_idx].max().item(), cur_len)
                if is_done != bool(self._done[batch_idx]):
                    finished_batch_idxs.append(unfin_batch_idx)

        if not self.use_reorder_cache_v2:
            eos_effective_scores = torch.masked_select(
                next_scores[:, : self.num_beams], mask=eos_mask[:, : self.num_beams]
            )
            input_ids_cpu = input_ids.cpu()
            eos_effective_idx_cpu = eos_effective_idx.cpu()
            eos_effective_scores_cpu = eos_effective_scores.cpu()
            for i in range(0, eos_effective_idx_cpu.size()[-1]):
                batch_idx = eos_effective_idx_cpu[i] // self.num_beams
                if not self._done[batch_idx]:
                    self._beam_hyps[batch_idx.item()].add(
                        input_ids_cpu[eos_effective_idx_cpu[i]].clone(),
                        eos_effective_scores_cpu[i],
                    )
                self._done[batch_idx] = self._done[batch_idx] or self._beam_hyps[
                    batch_idx
                ].is_done(next_scores[batch_idx].max().item(), cur_len)

        if self.use_reorder_cache_v2 and len(finished_batch_idxs) > 0:
            new_batch_size = batch_size - len(finished_batch_idxs)
            batch_mask = torch.ones(batch_size).to(next_tokens_id)
            batch_mask[torch.tensor(finished_batch_idxs)] = 0
            batch_idxs = batch_mask.nonzero().squeeze(-1)
            eos_mask = eos_mask[batch_idxs]
            next_beams_id = next_beams_id[batch_idxs]
            self.beams_offset.resize_(new_batch_size, 1)
            effective_beam_id = next_beams_id.add(self.beams_offset)
            next_scores = next_scores[batch_idxs]
            next_tokens = next_tokens[batch_idxs]
            next_tokens_id = next_tokens_id[batch_idxs]
            before_batch_size = batch_size
            batch_size = new_batch_size
        else:
            before_batch_size = batch_size
            batch_idxs = None

        active_mask = torch.add(
            eos_mask.type_as(self.cand_offsets) * self.cand_size,
            self.cand_offsets[: eos_mask.size(1)],
        )
        _, active_hypos = torch.topk(
            active_mask, k=self.num_beams, dim=1, largest=False
        )
        active_effective_beam_id = torch.gather(
            effective_beam_id, dim=1, index=active_hypos
        )
        active_scores = torch.gather(next_scores, dim=1, index=active_hypos)
        active_tokens = torch.gather(next_tokens_id, dim=1, index=active_hypos)
        beam_idxs = active_effective_beam_id.view(-1)
        beam_scores = active_scores.view(-1)
        beam_tokens = active_tokens.view(-1)

        if batch_idxs is not None:
            new_beam_idxs = (
                torch.arange(before_batch_size * self.num_beams)
                .reshape(before_batch_size, self.num_beams)
                .to(input_ids)
            )
            beam_idxs = new_beam_idxs[batch_idxs].reshape(-1)[beam_idxs]

        userdict = UserDict(
            {
                "next_beam_scores": beam_scores.view(-1),
                "next_beam_tokens": beam_tokens.view(-1),
                "next_beam_indices": beam_idxs.view(-1),
            }
        )
        if self.use_reorder_cache_v2:
            userdict["next_batch_indices"] = batch_idxs

        return userdict

    def finalize(
        self,
        input_ids: torch.LongTensor,
        final_beam_scores: torch.FloatTensor,
        final_beam_tokens: torch.LongTensor,
        final_beam_indices: torch.LongTensor,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
    ) -> Tuple[torch.LongTensor]:
        batch_size = len(self._beam_hyps)

        unfin_offset = np.array(list(accumulate(map(int, self._done))))[
            np.array(list(map(int, self._done))) == 0
        ]
        if self.use_reorder_cache_v2:
            batch_size = len(unfin_offset)
        for batch_idx in range(batch_size):
            if not self.use_reorder_cache_v2 and self._done[batch_idx]:
                continue
            if self.use_reorder_cache_v2:
                final_batch_idx = batch_idx + unfin_offset[batch_idx]
            else:
                final_batch_idx = batch_idx
            # need to add best num_beams hypotheses to generated hyps
            for beam_id in range(self.num_beams):
                effective_beam_id = batch_idx * self.num_beams + beam_id
                final_score = final_beam_scores[effective_beam_id].item()
                final_tokens = input_ids[effective_beam_id]
                self._beam_hyps[final_batch_idx].add(final_tokens, final_score)

        batch_size = len(self._beam_hyps)

        # select the best hypotheses
        sent_lengths = input_ids.new(batch_size * self.num_beam_hyps_to_keep)
        best = []
        best_scores = torch.zeros(
            batch_size * self.num_beam_hyps_to_keep,
            device=self.device,
            dtype=torch.float32,
        )

        # retrieve best hypotheses
        for i, beam_hyp in enumerate(self._beam_hyps):
            sorted_hyps = sorted(beam_hyp.beams, key=lambda x: x[0])
            for j in range(self.num_beam_hyps_to_keep):
                best_hyp_tuple = sorted_hyps.pop()
                best_score = best_hyp_tuple[0]
                best_hyp = best_hyp_tuple[1]
                sent_lengths[self.num_beam_hyps_to_keep * i + j] = len(best_hyp)

                # append to lists
                best.append(best_hyp)
                best_scores[i * self.num_beam_hyps_to_keep + j] = best_score

        # prepare for adding eos
        sent_max_len = min(sent_lengths.max().item() + 1, self.max_length)
        decoded: torch.LongTensor = input_ids.new(
            batch_size * self.num_beam_hyps_to_keep, sent_max_len
        )
        # shorter batches are padded if needed
        if sent_lengths.min().item() != sent_lengths.max().item():
            assert pad_token_id is not None, "`pad_token_id` has to be defined"
            decoded.fill_(pad_token_id)

        # fill with hypotheses and eos_token_id if the latter fits in
        for i, hypo in enumerate(best):
            decoded[i, : sent_lengths[i]] = hypo
            if sent_lengths[i] < self.max_length:
                decoded[i, sent_lengths[i]] = eos_token_id
        return UserDict(
            {
                "sequences": decoded,
                "sequence_scores": best_scores,
            }
        )


class GenerationMixinV2(GenerationMixin):
    def beam_search(
        self,
        input_ids: torch.LongTensor,
        beam_scorer: BeamScorer,
        logits_processor: Optional[LogitsProcessorList] = None,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        output_scores: Optional[bool] = None,
        return_dict_in_generate: Optional[bool] = None,
        **model_kwargs,
    ) -> Union[BeamSearchOutput, torch.LongTensor]:
        r"""
        Generates sequences for models with a language modeling head using beam search decoding.
        Parameters:
            input_ids (:obj:`torch.LongTensor` of shape :obj:`(batch_size, sequence_length)`, `optional`):
                The sequence used as a prompt for the generation. If :obj:`None` the method initializes it as an empty
                :obj:`torch.LongTensor` of shape :obj:`(1,)`.
            beam_scorer (:obj:`BeamScorer`):
                An derived instance of :class:`~transformers.BeamScorer` that defines how beam hypotheses are
                constructed, stored and sorted during generation. For more information, the documentation of
                :class:`~transformers.BeamScorer` should be read.
            logits_processor (:obj:`LogitsProcessorList`, `optional`):
                An instance of :class:`~transformers.LogitsProcessorList`. List of instances of class derived from
                :class:`~transformers.LogitsProcessor` used to modify the prediction scores of the language modeling
                head applied at each generation step.
            max_length (:obj:`int`, `optional`, defaults to 20):
                The maximum length of the sequence to be generated.
            pad_token_id (:obj:`int`, `optional`):
                The id of the `padding` token.
            eos_token_id (:obj:`int`, `optional`):
                The id of the `end-of-sequence` token.
            output_attentions (:obj:`bool`, `optional`, defaults to `False`):
                Whether or not to return the attentions tensors of all attention layers. See ``attentions`` under
                returned tensors for more details.
            output_hidden_states (:obj:`bool`, `optional`, defaults to `False`):
                Whether or not to return trhe hidden states of all layers. See ``hidden_states`` under returned tensors
                for more details.
            output_scores (:obj:`bool`, `optional`, defaults to `False`):
                Whether or not to return the prediction scores. See ``scores`` under returned tensors for more details.
            return_dict_in_generate (:obj:`bool`, `optional`, defaults to `False`):
                Whether or not to return a :class:`~transformers.file_utils.ModelOutput` instead of a plain tuple.
            model_kwargs:
                Additional model specific kwargs will be forwarded to the :obj:`forward` function of the model. If
                model is an encoder-decoder model the kwargs should include :obj:`encoder_outputs`.
        Return:
            :class:`~transformers.generation_utilsBeamSearchDecoderOnlyOutput`,
            :class:`~transformers.generation_utils.BeamSearchEncoderDecoderOutput` or obj:`torch.LongTensor`: A
            :obj:`torch.LongTensor` containing the generated tokens (default behaviour) or a
            :class:`~transformers.generation_utils.BeamSearchDecoderOnlyOutput` if
            ``model.config.is_encoder_decoder=False`` and ``return_dict_in_generate=True`` or a
            :class:`~transformers.generation_utils.BeamSearchEncoderDecoderOutput` if
            ``model.config.is_encoder_decoder=True``.
        Examples::
            >>> from transformers import (
            ...    AutoTokenizer,
            ...    AutoModelForSeq2SeqLM,
            ...    LogitsProcessorList,
            ...    MinLengthLogitsProcessor,
            ...    BeamSearchScorer,
            ... )
            >>> import torch
            >>> tokenizer = AutoTokenizer.from_pretrained("t5-base")
            >>> model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
            >>> encoder_input_str = "translate English to German: How old are you?"
            >>> encoder_input_ids = tokenizer(encoder_input_str, return_tensors="pt").input_ids
            >>> # lets run beam search using 3 beams
            >>> num_beams = 3
            >>> # define decoder start token ids
            >>> input_ids = torch.ones((num_beams, 1), device=model.device, dtype=torch.long)
            >>> input_ids = input_ids * model.config.decoder_start_token_id
            >>> # add encoder_outputs to model keyword arguments
            >>> model_kwargs = {
            ...     "encoder_outputs": model.get_encoder()(encoder_input_ids.repeat_interleave(num_beams, dim=0), return_dict=True)
            ... }
            >>> # instantiate beam scorer
            >>> beam_scorer = BeamSearchScorer(
            ...     batch_size=1,
            ...     max_length=model.config.max_length,
            ...     num_beams=num_beams,
            ...     device=model.device,
            ... )
            >>> # instantiate logits processors
            >>> logits_processor = LogitsProcessorList([
            ...     MinLengthLogitsProcessor(5, eos_token_id=model.config.eos_token_id),
            ... ])
            >>> outputs = model.beam_search(input_ids, beam_scorer, logits_processor=logits_processor, **model_kwargs)
            >>> print("Generated:", tokenizer.batch_decode(outputs, skip_special_tokens=True))
        """

        # init values
        logits_processor = (
            logits_processor if logits_processor is not None else LogitsProcessorList()
        )
        max_length = max_length if max_length is not None else self.config.max_length
        pad_token_id = (
            pad_token_id if pad_token_id is not None else self.config.pad_token_id
        )
        eos_token_id = (
            eos_token_id if eos_token_id is not None else self.config.eos_token_id
        )
        output_scores = (
            output_scores if output_scores is not None else self.config.output_scores
        )
        output_attentions = (
            output_attentions
            if output_attentions is not None
            else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        return_dict_in_generate = (
            return_dict_in_generate
            if return_dict_in_generate is not None
            else self.config.return_dict_in_generate
        )

        # init attention / hidden states / scores tuples
        scores = () if (return_dict_in_generate and output_scores) else None
        decoder_attentions = (
            () if (return_dict_in_generate and output_attentions) else None
        )
        decoder_hidden_states = (
            () if (return_dict_in_generate and output_hidden_states) else None
        )

        # if model is an encoder-decoder, retrieve encoder attention weights and hidden states
        if return_dict_in_generate and self.config.is_encoder_decoder:
            encoder_attentions = (
                model_kwargs["encoder_outputs"].get("attentions")
                if output_attentions
                else None
            )
            encoder_hidden_states = (
                model_kwargs["encoder_outputs"].get("hidden_states")
                if output_hidden_states
                else None
            )

        batch_size = len(beam_scorer._beam_hyps)
        num_beams = beam_scorer.num_beams

        if hasattr(beam_scorer, "use_reorder_cache_v2"):
            beam_scorer.use_reorder_cache_v2 = hasattr(self, "_reorder_cache_v2")

        batch_beam_size, cur_len = input_ids.shape

        assert (
            num_beams * batch_size == batch_beam_size
        ), "Batch dimension of `input_ids` should be {num_beams * batch_size}, but is {batch_beam_size}."

        beam_scores = torch.zeros(
            (batch_size, num_beams), dtype=torch.float, device=input_ids.device
        )
        beam_scores[:, 1:] = -1e9
        beam_scores = beam_scores.view((batch_size * num_beams,))

        while cur_len < max_length:
            model_inputs = self.prepare_inputs_for_generation(input_ids, **model_kwargs)

            outputs = self(
                **model_inputs,
                return_dict=True,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )
            next_token_logits = outputs.logits[:, -1, :]

            # hack: adjust tokens for Marian. For Marian we have to make sure that the `pad_token_id`
            # cannot be generated both before and after the `F.log_softmax` operation.
            next_token_logits = self.adjust_logits_during_generation(
                next_token_logits, cur_len=cur_len, max_length=max_length
            )

            next_token_scores = F.log_softmax(
                next_token_logits, dim=-1
            )  # (batch_size * num_beams, vocab_size)

            next_token_scores = logits_processor(input_ids, next_token_scores)
            next_token_scores = next_token_scores + beam_scores[:, None].expand_as(
                next_token_scores
            )

            # Store scores, attentions and hidden_states when required
            if return_dict_in_generate:
                if output_scores:
                    scores += (next_token_scores,)
                if output_attentions:
                    decoder_attentions += (
                        (outputs.decoder_attentions,)
                        if self.config.is_encoder_decoder
                        else (outputs.attentions,)
                    )

                if output_hidden_states:
                    decoder_hidden_states += (
                        (outputs.decoder_hidden_states,)
                        if self.config.is_encoder_decoder
                        else (outputs.hidden_states,)
                    )

            # reshape for beam search
            vocab_size = next_token_scores.shape[-1]
            next_token_scores = next_token_scores.view(
                batch_size, num_beams * vocab_size
            )

            next_token_scores, next_tokens = torch.topk(
                next_token_scores, 2 * num_beams, dim=1, largest=True, sorted=True
            )

            next_indices = next_tokens // vocab_size
            next_tokens = next_tokens % vocab_size

            # stateless
            beam_outputs = beam_scorer.process(
                input_ids,
                next_token_scores,
                next_tokens,
                next_indices,
                pad_token_id=pad_token_id,
                eos_token_id=eos_token_id,
            )
            beam_scores = beam_outputs["next_beam_scores"]
            beam_next_tokens = beam_outputs["next_beam_tokens"]
            beam_idx = beam_outputs["next_beam_indices"]
            batch_idx = (
                beam_outputs["next_batch_indices"]
                if "next_batch_indices" in beam_outputs
                else None
            )

            input_ids = torch.cat(
                [input_ids[beam_idx, :], beam_next_tokens.unsqueeze(-1)], dim=-1
            )

            if batch_idx is not None:
                batch_size = batch_idx.shape[0]

            if model_kwargs.get("attention_mask") is not None:
                model_kwargs["attention_mask"] = model_kwargs[
                    "attention_mask"
                ].index_select(0, beam_idx)

            cur_len = cur_len + 1

            model_kwargs = self._update_model_kwargs_for_generation(
                outputs, model_kwargs, is_encoder_decoder=self.config.is_encoder_decoder
            )
            if model_kwargs["past"] is not None:
                if batch_idx is not None:
                    model_kwargs["past"] = self._reorder_cache_v2(
                        model_kwargs["past"], batch_idx, beam_idx
                    )
                else:
                    model_kwargs["past"] = self._reorder_cache(
                        model_kwargs["past"], beam_idx
                    )

            if beam_scorer.is_done:
                break

        sequence_outputs = beam_scorer.finalize(
            input_ids,
            beam_scores,
            next_tokens,
            next_indices,
            pad_token_id=pad_token_id,
            eos_token_id=eos_token_id,
        )

        if return_dict_in_generate:
            if not output_scores:
                sequence_outputs["sequence_scores"] = None
            if self.config.is_encoder_decoder:
                return BeamSearchEncoderDecoderOutput(
                    sequences=sequence_outputs["sequences"],
                    sequences_scores=sequence_outputs["sequence_scores"],
                    scores=scores,
                    encoder_attentions=encoder_attentions,
                    encoder_hidden_states=encoder_hidden_states,
                    decoder_attentions=decoder_attentions,
                    decoder_hidden_states=decoder_hidden_states,
                )
            else:
                return BeamSearchDecoderOnlyOutput(
                    sequences=sequence_outputs["sequences"],
                    sequences_scores=sequence_outputs["sequence_scores"],
                    scores=scores,
                    attentions=decoder_attentions,
                    hidden_states=decoder_hidden_states,
                )
        else:
            return sequence_outputs["sequences"]
