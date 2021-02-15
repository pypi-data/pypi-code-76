# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

import math
import re
import sys
import unicodedata

import six
import torch
from torch.nn import functional as F

from mlbench_core.models.pytorch.transformer.decoder import TransformerDecoder


class UnicodeRegex(object):
    """Ad-hoc hack to recognize all punctuation and symbols."""

    def __init__(self):
        punctuation = self.property_chars("P")
        self.nondigit_punct_re = re.compile(r"([^\d])([" + punctuation + r"])")
        self.punct_nondigit_re = re.compile(r"([" + punctuation + r"])([^\d])")
        self.symbol_re = re.compile("([" + self.property_chars("S") + "])")

    def property_chars(self, prefix):
        return "".join(
            six.unichr(x)
            for x in range(sys.maxunicode)
            if unicodedata.category(six.unichr(x)).startswith(prefix)
        )


uregex = UnicodeRegex()


def strip_pad(tensor, pad):
    return tensor[tensor.ne(pad)]


def post_process_prediction(hypo_tokens, alignment, align_dict, tgt_dict, remove_bpe):
    hypo_str = tgt_dict.string(hypo_tokens, remove_bpe)

    assert not align_dict

    return hypo_tokens, hypo_str, alignment


def detokenize_subtokenized_sentence(subtokenized_sentence):
    l1 = " ".join("".join(subtokenized_sentence.strip().split()).split("_"))
    l1 = l1.replace(" ,", ",")
    l1 = l1.replace(" .", ".")
    l1 = l1.replace(" !", "!")
    l1 = l1.replace(" ?", "?")
    l1 = l1.replace(" ' ", "'")
    l1 = l1.replace(" - ", "-")
    l1 = l1.strip()
    return l1


def bleu_tokenize(string):
    r"""Tokenize a string following the official BLEU implementation.
    See https://github.com/moses-smt/mosesdecoder/'
    'blob/master/scripts/generic/mteval-v14.pl#L954-L983
    In our case, the input string is expected to be just one line
    and no HTML entities de-escaping is needed.
    So we just tokenize on punctuation and symbols,
    except when a punctuation is preceded and followed by a digit
    (e.g. a comma/dot as a thousand/decimal separator).
    Note that a numer (e.g. a year) followed by a dot at the end of sentence
    is NOT tokenized,
    i.e. the dot stays with the number because `s/(\p{P})(\P{N})/ $1 $2/g`
    does not match this case (unless we add a space after each sentence).
    However, this error is already in the original mteval-v14.pl
    and we want to be consistent with it.
    Args:
    string: the input string
    Returns:
    a list of tokens
    """
    string = uregex.nondigit_punct_re.sub(r"\1 \2 ", string)
    string = uregex.punct_nondigit_re.sub(r" \1 \2", string)
    string = uregex.symbol_re.sub(r" \1 ", string)
    return string


class UnicodeRegex(object):
    """Ad-hoc hack to recognize all punctuation and symbols."""

    def __init__(self):
        punctuation = self.property_chars("P")
        self.nondigit_punct_re = re.compile(r"([^\d])([" + punctuation + r"])")
        self.punct_nondigit_re = re.compile(r"([" + punctuation + r"])([^\d])")
        self.symbol_re = re.compile("([" + self.property_chars("S") + "])")

    def property_chars(self, prefix):
        return "".join(
            six.unichr(x)
            for x in range(sys.maxunicode)
            if unicodedata.category(six.unichr(x)).startswith(prefix)
        )


class SequenceGenerator(object):
    """Generates translations of a given source sentence.

    Args:
        model (:obj:`torch.nn.Module`): The model to predict on. Should be instance of `TransformerModel`
        src_dict (:obj:`mlbench_core.dataset.nlp.pytorch.wmt17.Dictionary`): Source dictionary
        trg_dict (:obj:`mlbench_core.dataset.nlp.pytorch.wmt17.Dictionary`): Target dictionary
        beam_size (int): Size of the beam. Default 1
        minlen (int): Minimum generation length. Default 1
        maxlen (int): Maximum generation length. If `None`, takes value of model.max_decoder_positions().
            Default `None`
        stop_early (bool): Stop generation immediately after we finalize beam_size
            hypotheses, even though longer hypotheses might have better
            normalized scores. Default `True`
        normalize_scores (bool): Normalize scores by the length of the output. Default `True`
        len_penalty (float): length penalty: <1.0 favors shorter, >1.0 favors longer sentences.
            Default 1
        retain_dropout (bool): Keep dropout layers. Default `False`
        sampling (bool): sample hypotheses instead of using beam search. Default `False`
        sampling_topk (int): sample from top K likely next words instead of all words. Default -1
        sampling_temperature (int): temperature for random sampling. Default 1
    """

    def __init__(
        self,
        model,
        src_dict,
        trg_dict,
        beam_size=1,
        minlen=1,
        maxlen=None,
        stop_early=True,
        normalize_scores=True,
        len_penalty=1,
        retain_dropout=False,
        sampling=False,
        sampling_topk=-1,
        sampling_temperature=1,
    ):
        self.model = model
        self.pad = trg_dict.pad()
        self.eos = trg_dict.eos()
        self.vocab_size = len(trg_dict)
        self.src_dict = src_dict
        self.trg_dict = trg_dict
        self.beam_size = beam_size
        self.minlen = minlen
        max_decoder_len = self.model.max_decoder_positions()
        max_decoder_len -= 1  # we define maxlen not including the EOS marker
        self.maxlen = (
            max_decoder_len if maxlen is None else min(maxlen, max_decoder_len)
        )
        self.stop_early = stop_early
        self.normalize_scores = normalize_scores
        self.len_penalty = len_penalty
        self.retain_dropout = retain_dropout
        self.sampling = sampling
        self.sampling_topk = sampling_topk
        self.sampling_temperature = sampling_temperature

    def generate_batch_translations(
        self,
        batch,
        maxlen_a=0.0,
        maxlen_b=None,
        prefix_size=0,
    ):
        """Yield individual translations of a batch.

        Args:
            batch (dict): The model input batch. Must have keys `net_input`, `target` and `ntokens`
            maxlen_a (float):
            maxlen_b (Optional[int]): Generate sequences of max lengths `maxlen_a*x + maxlen_b` where `x = input sentence length`
            prefix_size (int): Prefix size
        """
        if maxlen_b is None:
            maxlen_b = self.maxlen

        if "net_input" not in batch:
            return
        input = batch["net_input"]
        srclen = input["src_tokens"].size(1)
        with torch.no_grad():
            hypos = self.generate(
                input["src_tokens"],
                input["src_lengths"],
                maxlen=int(maxlen_a * srclen + maxlen_b),
                prefix_tokens=batch["target"][:, :prefix_size]
                if prefix_size > 0
                else None,
            )
        for i, id in enumerate(batch["id"].data):
            # remove padding
            src = strip_pad(input["src_tokens"].data[i, :], self.pad)
            ref = (
                strip_pad(batch["target"].data[i, :], self.pad)
                if batch["target"] is not None
                else None
            )
            yield id, src, ref, hypos[i]

    def generate(self, src_tokens, src_lengths, maxlen=None, prefix_tokens=None):
        """Generate a batch of translations."""
        with torch.no_grad():
            return self._generate(src_tokens, src_lengths, maxlen, prefix_tokens)

    def _generate(self, src_tokens, src_lengths, maxlen=None, prefix_tokens=None):
        bsz, srclen = src_tokens.size()
        maxlen = min(maxlen, self.maxlen) if maxlen is not None else self.maxlen

        # the max beam size is the dictionary size - 1, since we never select pad
        beam_size = self.beam_size
        beam_size = min(beam_size, self.vocab_size - 1)

        incremental_state = None
        if not self.retain_dropout:
            self.model.eval()
        if isinstance(self.model.decoder, TransformerDecoder):
            incremental_state = {}

        # compute the encoder output for each beam
        encoder_out = self.model.encoder(
            src_tokens.repeat(1, beam_size).view(-1, srclen)
        )

        # initialize buffers
        scores = src_tokens.data.new(bsz * beam_size, maxlen + 1).float().fill_(0)
        scores_buf = scores.clone()
        tokens = src_tokens.data.new(bsz * beam_size, maxlen + 2).fill_(self.pad)
        tokens_buf = tokens.clone()
        tokens[:, 0] = self.eos
        attn, attn_buf = None, None
        nonpad_idxs = None

        # list of completed sentences
        finalized = [[] for i in range(bsz)]
        finished = [False for i in range(bsz)]
        worst_finalized = [{"idx": None, "score": -math.inf} for i in range(bsz)]
        num_remaining_sent = bsz

        # number of candidate hypos per step
        cand_size = 2 * beam_size  # 2 x beam size in case half are EOS

        # offset arrays for converting between different indexing schemes
        bbsz_offsets = (torch.arange(0, bsz) * beam_size).unsqueeze(1).type_as(tokens)
        cand_offsets = torch.arange(0, cand_size).type_as(tokens)

        # helper function for allocating buffers on the fly
        buffers = {}

        def buffer(name, type_of=tokens):  # noqa
            if name not in buffers:
                buffers[name] = type_of.new()
            return buffers[name]

        def is_finished(sent, step, unfinalized_scores=None):
            """
            Check whether we've finished generation for a given sentence, by
            comparing the worst score among finalized hypotheses to the best
            possible score among unfinalized hypotheses.
            """
            assert len(finalized[sent]) <= beam_size
            if len(finalized[sent]) == beam_size:
                if self.stop_early or step == maxlen or unfinalized_scores is None:
                    return True
                # stop if the best unfinalized score is worse than the worst
                # finalized one
                best_unfinalized_score = unfinalized_scores[sent].max()
                if self.normalize_scores:
                    # We don't know why the reference adds 5 and divides by 6, perhaps for rounding
                    best_unfinalized_score /= ((maxlen + 5) / 6) ** self.len_penalty
                if worst_finalized[sent]["score"] >= best_unfinalized_score:
                    return True
            return False

        def finalize_hypos(step, bbsz_idx, eos_scores, unfinalized_scores=None):
            """
            Finalize the given hypotheses at this step, while keeping the total
            number of finalized hypotheses per sentence <= beam_size.
            Note: the input must be in the desired finalization order, so that
            hypotheses that appear earlier in the input are preferred to those
            that appear later.
            Args:
                step: current time step
                bbsz_idx: A vector of indices in the range [0, bsz*beam_size),
                    indicating which hypotheses to finalize
                eos_scores: A vector of the same size as bbsz_idx containing
                    scores for each hypothesis
                unfinalized_scores: A vector containing scores for all
                    unfinalized hypotheses
            """
            assert bbsz_idx.numel() == eos_scores.numel()

            # clone relevant token and attention tensors
            tokens_clone = tokens.index_select(0, bbsz_idx)
            tokens_clone = tokens_clone[
                :, 1 : step + 2
            ]  # skip the first index, which is EOS
            tokens_clone[:, step] = self.eos
            attn_clone = (
                attn.index_select(0, bbsz_idx)[:, :, 1 : step + 2]
                if attn is not None
                else None
            )

            # compute scores per token position
            pos_scores = scores.index_select(0, bbsz_idx)[:, : step + 1]
            pos_scores[:, step] = eos_scores
            # convert from cumulative to per-position scores
            pos_scores[:, 1:] = pos_scores[:, 1:] - pos_scores[:, :-1]

            # normalize sentence-level scores
            if self.normalize_scores:
                # We don't know why the reference adds 5 and divides by 6, perhaps for rounding
                eos_scores /= (((step + 1) + 5) / 6) ** self.len_penalty

            cum_unfin = []
            prev = 0
            for f in finished:
                if f:
                    prev += 1
                else:
                    cum_unfin.append(prev)

            sents_seen = set()
            for i, (idx, score) in enumerate(
                zip(bbsz_idx.tolist(), eos_scores.tolist())
            ):
                unfin_idx = idx // beam_size
                sent = unfin_idx + cum_unfin[unfin_idx]

                sents_seen.add((sent, unfin_idx))

                def get_hypo():

                    if attn_clone is not None:
                        # remove padding tokens from attn scores
                        hypo_attn = attn_clone[i][nonpad_idxs[sent]]
                        _, alignment = hypo_attn.max(dim=0)
                    else:
                        hypo_attn = None
                        alignment = None

                    return {
                        "tokens": tokens_clone[i],
                        "score": score,
                        "attention": hypo_attn,  # src_len x tgt_len
                        "alignment": alignment,
                        "positional_scores": pos_scores[i],
                    }

                if len(finalized[sent]) < beam_size:
                    finalized[sent].append(get_hypo())
                elif not self.stop_early and score > worst_finalized[sent]["score"]:
                    # replace worst hypo for this sentence with new/better one
                    worst_idx = worst_finalized[sent]["idx"]
                    if worst_idx is not None:
                        finalized[sent][worst_idx] = get_hypo()

                    # find new worst finalized hypo for this sentence
                    idx, s = min(
                        enumerate(finalized[sent]), key=lambda r: r[1]["score"]
                    )
                    worst_finalized[sent] = {
                        "score": s["score"],
                        "idx": idx,
                    }

            newly_finished = []
            for sent, unfin_idx in sents_seen:
                # check termination conditions for this sentence
                if not finished[sent] and is_finished(sent, step, unfinalized_scores):
                    finished[sent] = True
                    newly_finished.append(unfin_idx)
            return newly_finished

        reorder_state = None
        batch_idxs = None
        for step in range(maxlen + 1):  # one extra step for EOS marker
            if reorder_state is not None:
                if batch_idxs is not None:
                    # update beam indices to take into account removed sentences
                    corr = batch_idxs - torch.arange(batch_idxs.numel()).type_as(
                        batch_idxs
                    )
                    reorder_state.view(-1, beam_size).add_(
                        corr.unsqueeze(-1) * beam_size
                    )
                if isinstance(self.model.decoder, TransformerDecoder):
                    self.model.decoder.reorder_incremental_state(
                        incremental_state, reorder_state
                    )
                encoder_out = self.model.encoder.reorder_encoder_out(
                    encoder_out, reorder_state
                )

            probs, avg_attn_scores = self._decode_one(
                tokens[:, : step + 1],
                self.model,
                encoder_out,
                incremental_state,
                log_probs=True,
            )
            if step == 0:
                # at the first step all hypotheses are equally likely, so use
                # only the first beam
                probs = probs.unfold(0, 1, beam_size).squeeze(2).contiguous()
                scores = scores.type_as(probs)
                scores_buf = scores_buf.type_as(probs)
            elif not self.sampling:
                # make probs contain cumulative scores for each hypothesis
                probs.add_(scores[:, step - 1].view(-1, 1))

            probs[:, self.pad] = -math.inf  # never select pad

            # Record attention scores
            if avg_attn_scores is not None:
                if attn is None:
                    attn = scores.new(bsz * beam_size, src_tokens.size(1), maxlen + 2)
                    attn_buf = attn.clone()
                    nonpad_idxs = src_tokens.ne(self.pad)
                attn[:, :, step + 1].copy_(avg_attn_scores)

            cand_scores = buffer("cand_scores", type_of=scores)
            cand_indices = buffer("cand_indices")
            cand_beams = buffer("cand_beams")
            eos_bbsz_idx = buffer("eos_bbsz_idx")
            eos_scores = buffer("eos_scores", type_of=scores)
            if step < maxlen:
                if prefix_tokens is not None and step < prefix_tokens.size(1):
                    probs_slice = probs.view(bsz, -1, probs.size(-1))[:, 0, :]
                    cand_scores = torch.gather(
                        probs_slice,
                        dim=1,
                        index=prefix_tokens[:, step].view(-1, 1).data,
                    ).expand(-1, cand_size)
                    cand_indices = (
                        prefix_tokens[:, step].view(-1, 1).expand(bsz, cand_size).data
                    )
                    cand_beams.resize_as_(cand_indices).fill_(0)
                elif self.sampling:
                    assert (
                        self.pad == 1
                    ), "sampling assumes the first two symbols can be ignored"

                    if self.sampling_topk > 0:
                        values, indices = probs[:, 2:].topk(self.sampling_topk)
                        exp_probs = values.div_(self.sampling_temperature).exp()
                        if step == 0:
                            torch.multinomial(
                                exp_probs, beam_size, replacement=True, out=cand_indices
                            )
                        else:
                            torch.multinomial(
                                exp_probs, 1, replacement=True, out=cand_indices
                            )
                        torch.gather(
                            exp_probs, dim=1, index=cand_indices, out=cand_scores
                        )
                        torch.gather(
                            indices, dim=1, index=cand_indices, out=cand_indices
                        )
                        cand_indices.add_(2)
                    else:
                        exp_probs = (
                            probs.div_(self.sampling_temperature)
                            .exp_()
                            .view(-1, self.vocab_size)
                        )

                        if step == 0:
                            # we exclude the first two vocab items, one of which is pad
                            torch.multinomial(
                                exp_probs[:, 2:],
                                beam_size,
                                replacement=True,
                                out=cand_indices,
                            )
                        else:
                            torch.multinomial(
                                exp_probs[:, 2:], 1, replacement=True, out=cand_indices
                            )

                        cand_indices.add_(2)
                        torch.gather(
                            exp_probs, dim=1, index=cand_indices, out=cand_scores
                        )

                    cand_scores.log_()
                    cand_indices = cand_indices.view(bsz, -1).repeat(1, 2)
                    cand_scores = cand_scores.view(bsz, -1).repeat(1, 2)
                    if step == 0:
                        cand_beams = torch.zeros(bsz, cand_size).type_as(cand_indices)
                    else:
                        cand_beams = (
                            torch.arange(0, beam_size)
                            .repeat(bsz, 2)
                            .type_as(cand_indices)
                        )
                        # make scores cumulative
                        cand_scores.add_(
                            torch.gather(
                                scores[:, step - 1].view(bsz, beam_size),
                                dim=1,
                                index=cand_beams,
                            )
                        )
                else:
                    # take the best 2 x beam_size predictions. We'll choose the first
                    # beam_size of these which don't predict eos to continue with.
                    torch.topk(
                        probs.view(bsz, -1),
                        k=min(
                            cand_size, probs.view(bsz, -1).size(1) - 1
                        ),  # -1 so we never select pad
                        out=(cand_scores, cand_indices),
                    )
                    torch.floor_divide(
                        cand_indices, self.vocab_size, out=cand_beams.resize_(0)
                    )
                    cand_indices.fmod_(self.vocab_size)
            else:
                # finalize all active hypotheses once we hit maxlen
                # pick the hypothesis with the highest prob of EOS right now
                torch.sort(
                    probs[:, self.eos],
                    descending=True,
                    out=(eos_scores, eos_bbsz_idx),
                )
                num_remaining_sent -= len(
                    finalize_hypos(step, eos_bbsz_idx, eos_scores)
                )
                assert num_remaining_sent == 0
                break

            # cand_bbsz_idx contains beam indices for the top candidate
            # hypotheses, with a range of values: [0, bsz*beam_size),
            # and dimensions: [bsz, cand_size]
            cand_bbsz_idx = cand_beams.add(bbsz_offsets)

            # finalize hypotheses that end in eos
            eos_mask = cand_indices.eq(self.eos)

            finalized_sents = set()
            if step >= self.minlen:
                # only consider eos when it's among the top beam_size indices
                torch.masked_select(
                    cand_bbsz_idx[:, :beam_size],
                    mask=eos_mask[:, :beam_size],
                    out=eos_bbsz_idx.resize_(0),
                )
                if eos_bbsz_idx.numel() > 0:
                    torch.masked_select(
                        cand_scores[:, :beam_size],
                        mask=eos_mask[:, :beam_size],
                        out=eos_scores.resize_(0),
                    )
                    finalized_sents = finalize_hypos(
                        step, eos_bbsz_idx, eos_scores, cand_scores
                    )
                    num_remaining_sent -= len(finalized_sents)

            assert num_remaining_sent >= 0
            if num_remaining_sent == 0:
                break
            assert step < maxlen

            if len(finalized_sents) > 0:
                new_bsz = bsz - len(finalized_sents)

                # construct batch_idxs which holds indices of batches to keep for the next pass
                batch_mask = torch.ones(bsz).type_as(cand_indices)
                batch_mask[cand_indices.new(finalized_sents)] = 0
                batch_idxs = torch.nonzero(batch_mask).squeeze(-1)
                # batch_idxs = batch_mask.nonzero().squeeze(-1)

                eos_mask = eos_mask[batch_idxs]
                cand_beams = cand_beams[batch_idxs]
                bbsz_offsets.resize_(new_bsz, 1)
                cand_bbsz_idx = cand_beams.add(bbsz_offsets)

                cand_scores = cand_scores[batch_idxs]
                cand_indices = cand_indices[batch_idxs]
                if prefix_tokens is not None:
                    prefix_tokens = prefix_tokens[batch_idxs]

                scores = scores.view(bsz, -1)[batch_idxs].view(new_bsz * beam_size, -1)
                scores_buf.resize_as_(scores)
                tokens = tokens.view(bsz, -1)[batch_idxs].view(new_bsz * beam_size, -1)
                tokens_buf.resize_as_(tokens)
                if attn is not None:
                    attn = attn.view(bsz, -1)[batch_idxs].view(
                        new_bsz * beam_size, attn.size(1), -1
                    )
                    attn_buf.resize_as_(attn)
                bsz = new_bsz
            else:
                batch_idxs = None

            # set active_mask so that values > cand_size indicate eos hypos
            # and values < cand_size indicate candidate active hypos.
            # After, the min values per row are the top candidate active hypos
            active_mask = buffer("active_mask")
            torch.add(
                eos_mask.type_as(cand_offsets) * cand_size,
                cand_offsets[: eos_mask.size(1)],
                out=active_mask.resize_(0),
            )

            # get the top beam_size active hypotheses, which are just the hypos
            # with the smallest values in active_mask
            active_hypos, _ignore = buffer("active_hypos"), buffer("_ignore")
            torch.topk(
                active_mask,
                k=beam_size,
                dim=1,
                largest=False,
                out=(_ignore, active_hypos),
            )
            active_bbsz_idx = buffer("active_bbsz_idx")
            torch.gather(
                cand_bbsz_idx,
                dim=1,
                index=active_hypos,
                out=active_bbsz_idx,
            )
            active_scores = torch.gather(
                cand_scores,
                dim=1,
                index=active_hypos,
                out=scores[:, step].view(bsz, beam_size),
            )

            active_bbsz_idx = active_bbsz_idx.view(-1)
            active_scores = active_scores.view(-1)

            # copy tokens and scores for active hypotheses
            torch.index_select(
                tokens[:, : step + 1],
                dim=0,
                index=active_bbsz_idx,
                out=tokens_buf[:, : step + 1],
            )
            torch.gather(
                cand_indices,
                dim=1,
                index=active_hypos,
                out=tokens_buf.view(bsz, beam_size, -1)[:, :, step + 1],
            )
            if step > 0:
                torch.index_select(
                    scores[:, :step],
                    dim=0,
                    index=active_bbsz_idx,
                    out=scores_buf[:, :step],
                )
            torch.gather(
                cand_scores,
                dim=1,
                index=active_hypos,
                out=scores_buf.view(bsz, beam_size, -1)[:, :, step],
            )

            # copy attention for active hypotheses
            if attn is not None:
                torch.index_select(
                    attn[:, :, : step + 2],
                    dim=0,
                    index=active_bbsz_idx,
                    out=attn_buf[:, :, : step + 2],
                )

            # swap buffers
            tokens, tokens_buf = tokens_buf, tokens
            scores, scores_buf = scores_buf, scores
            if attn is not None:
                attn, attn_buf = attn_buf, attn

            # reorder incremental state in decoder
            reorder_state = active_bbsz_idx

        # sort by score descending
        for sent in range(len(finalized)):
            finalized[sent] = sorted(
                finalized[sent], key=lambda r: r["score"], reverse=True
            )

        return finalized

    def _decode_one(self, tokens, model, encoder_out, incremental_state, log_probs):
        with torch.no_grad():
            if incremental_state is not None:
                decoder_out = list(
                    model.decoder(
                        tokens, encoder_out, incremental_state=incremental_state
                    )
                )
            else:
                decoder_out = list(model.decoder(tokens, encoder_out))
            decoder_out[0] = decoder_out[0][:, -1, :]
            attn = decoder_out[1]
            if attn is not None:
                attn = attn[:, -1, :]
        probs = get_normalized_probs(decoder_out, log_probs=log_probs)
        return probs, attn

    def translate_batch(
        self,
        batch,
        maxlen_a=1.0,
        maxlen_b=50,
        prefix_size=0,
        remove_bpe=None,
        nbest=1,
        ignore_case=True,
    ):
        """
        Args:
            batch (dict): The model input batch. Must have keys `net_input`, `target` and `ntokens`
            maxlen_a (float): Default 1.0
            maxlen_b (Optional[int]): Generate sequences of max lengths `maxlen_a*x + maxlen_b` where `x = input sentence length`.
                Default 50
            prefix_size (int): Prefix size. Default 0
            remove_bpe (Optional[str]): BPE token. Default `None`
            nbest (int): Number of hypotheses to output. Default 1
            ignore_case (bool): Ignore case druing online eval. Default `True`

        Returns:
            (list[str], list[str]): The translations and their targets for the given batch
        """
        translations = self.generate_batch_translations(
            batch,
            maxlen_a=maxlen_a,
            maxlen_b=maxlen_b,
            prefix_size=prefix_size,
        )

        ref_toks = []
        sys_toks = []
        for sample_id, src_tokens, target_tokens, hypos in translations:
            # Process input and ground truth
            has_target = target_tokens is not None
            target_tokens = target_tokens.int().cpu() if has_target else None

            src_str = self.src_dict.string(src_tokens, remove_bpe)
            if has_target:
                target_str = self.trg_dict.string(target_tokens, remove_bpe)

            # Process top predictions
            for i, hypo in enumerate(hypos[: min(len(hypos), nbest)]):
                hypo_tokens, hypo_str, alignment = post_process_prediction(
                    hypo_tokens=hypo["tokens"].int().cpu(),
                    alignment=hypo["alignment"].int().cpu()
                    if hypo["alignment"] is not None
                    else None,
                    align_dict=None,
                    tgt_dict=self.trg_dict,
                    remove_bpe=remove_bpe,
                )

                # Score only the top hypothesis
                if has_target and i == 0:
                    src_str = detokenize_subtokenized_sentence(src_str)
                    target_str = detokenize_subtokenized_sentence(target_str)
                    hypo_str = detokenize_subtokenized_sentence(hypo_str)
                    sys_tok = bleu_tokenize(
                        hypo_str.lower() if ignore_case else hypo_str
                    )
                    ref_tok = bleu_tokenize(
                        target_str.lower() if ignore_case else target_str
                    )
                    sys_toks.append(sys_tok)
                    ref_toks.append(ref_tok)

        return sys_toks, ref_toks


def get_normalized_probs(net_output, log_probs):
    """Get normalized probabilities (or log probs) from a net's output."""
    logits = net_output[0]
    if log_probs:
        return F.log_softmax(logits, dim=-1, dtype=torch.float32)
    else:
        return F.softmax(logits, dim=-1, dtype=torch.float32)
