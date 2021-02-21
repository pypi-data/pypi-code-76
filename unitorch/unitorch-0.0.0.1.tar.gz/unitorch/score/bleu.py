from unitorch.utils.decorators import add_default_section_for_init
from unitorch.functions import pop_first_non_none_value
from unitorch import register_score, core_process
from unitorch.core import core_class

import collections
import math


def _get_ngrams(segment, max_order):
    """Extracts all n-grams upto a given maximum order from an input segment.
    Args:
        segment: text segment from which n-grams will be extracted.
        max_order: maximum length in tokens of the n-grams returned by this
            methods.
    Returns:
        The Counter containing all n-grams upto max_order in segment
        with a count of how many times each n-gram occurred.
    """
    ngram_counts = collections.Counter()
    for order in range(1, max_order + 1):
        for i in range(0, len(segment) - order + 1):
            ngram = tuple(segment[i : i + order])
            ngram_counts[ngram] += 1
    return ngram_counts


def compute_bleu(reference_corpus, translation_corpus, max_order=4, smooth=False):
    """Computes BLEU score of translated segments against one or more references.
    Args:
        reference_corpus: list of lists of references for each translation. Each
            reference should be tokenized into a list of tokens.
        translation_corpus: list of translations to score. Each translation
            should be tokenized into a list of tokens.
        max_order: Maximum n-gram order to use when computing BLEU score.
        smooth: Whether or not to apply Lin et al. 2004 smoothing.
    Returns:
        3-Tuple with the BLEU score, n-gram precisions, geometric mean of n-gram
        precisions and brevity penalty.
    """
    matches_by_order = [0] * max_order
    possible_matches_by_order = [0] * max_order
    reference_length = 0
    translation_length = 0
    for (references, translation) in zip(reference_corpus, translation_corpus):
        reference_length += min(len(r) for r in references)
        translation_length += len(translation)

        merged_ref_ngram_counts = collections.Counter()
        for reference in references:
            merged_ref_ngram_counts |= _get_ngrams(reference, max_order)
            translation_ngram_counts = _get_ngrams(translation, max_order)
            overlap = translation_ngram_counts & merged_ref_ngram_counts
        for ngram in overlap:
            matches_by_order[len(ngram) - 1] += overlap[ngram]
        for order in range(1, max_order + 1):
            possible_matches = len(translation) - order + 1
            if possible_matches > 0:
                possible_matches_by_order[order - 1] += possible_matches

    precisions = [0] * max_order
    for i in range(0, max_order):
        if smooth:
            precisions[i] = (matches_by_order[i] + 1.0) / (
                possible_matches_by_order[i] + 1.0
            )
        else:
            if possible_matches_by_order[i] > 0:
                precisions[i] = (
                    float(matches_by_order[i]) / possible_matches_by_order[i]
                )
            else:
                precisions[i] = 0.0

    if min(precisions) > 0:
        p_log_sum = sum((1.0 / max_order) * math.log(p) for p in precisions)
        geo_mean = math.exp(p_log_sum)
    else:
        geo_mean = 0

    ratio = float(translation_length) / reference_length

    if ratio > 1.0:
        bp = 1.0
    else:
        bp = math.exp(1 - 1.0 / ratio)

    bleu = geo_mean * bp

    return (bleu, precisions, bp, ratio, translation_length, reference_length)


@register_score("core/score/bleu")
class core_bleu_score(core_class):
    def __init__(self, process_fn=None, pad_token_id=0):
        self.process_fn = process_fn
        self.keys_for_label = ["tokens_ids", "next_tokens_ids"]
        self.pad_token_id = pad_token_id

    @classmethod
    @add_default_section_for_init("core/score/bleu")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def default_process_fn(self, tensor):
        if tensor.dim() == 3:
            ret = [
                list(
                    [
                        list(
                            map(
                                lambda x: str(int(x)),
                                filter(lambda x: x != self.pad_token_id, t2),
                            )
                        )
                        for t2 in t1
                    ]
                )
                for t1 in tensor
            ]
        elif tensor.dim() == 2:
            ret = [
                [
                    list(
                        map(
                            lambda x: str(int(x)),
                            filter(lambda x: x != self.pad_token_id, t1),
                        )
                    )
                ]
                for t1 in tensor
            ]
        else:
            raise f"tensor dim extracted 2-dim or 3-dim, but get size of {tensor.size()}"
        return ret

    def __call__(self, net_outputs, net_targets):
        net_targets = pop_first_non_none_value(
            *[net_targets.get(k) for k in self.keys_for_label]
        )
        # net_outputs / net_targets is 2dim or 3dim
        if self.process_fn is not None:
            net_outputs = self.process_fn(net_outputs)
            net_targets = self.process_fn(net_targets)
        else:
            net_outputs = self.default_process_fn(net_outputs)
            net_targets = self.default_process_fn(net_targets)
        net_outputs = [output[0] for output in net_outputs]
        return compute_bleu(net_targets, net_outputs)[0]
