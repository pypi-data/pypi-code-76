import torch
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from unitorch import register_score
from unitorch.core import core_class
from unitorch.functions import pop_first_non_none_value

from unitorch.utils.decorators import add_default_section_for_init


def reshape_tensor_or_ndarray(tensor_or_ndarray, shape=(-1), mask=None):
    if isinstance(tensor_or_ndarray, torch.Tensor):
        ndarray = tensor_or_ndarray.numpy()
    else:
        ndarray = tensor_or_ndarray

    ndarray = ndarray.reshape(shape)
    if mask is not None:
        ndarray = ndarray[mask]
    return ndarray


class core_base_score(core_class):
    def __init__(self, score_fn, gate=None):
        self.gate = gate
        self.keys_for_label = ["label", "next_tokens_ids"]
        self.keys_for_label_mask = ["label_mask", "next_tokens_mask"]
        self.score_fn = score_fn

    @classmethod
    @add_default_section_for_init("core/score/acc")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def get_net_outputs(self, net_outputs):
        return net_outputs

    def get_net_targets(self, net_targets):
        return net_targets

    def __call__(self, net_outputs, net_targets):
        net_outputs = self.get_net_outputs(net_outputs)
        net_targets = self.get_net_targets(net_targets)

        label = pop_first_non_none_value(
            *[net_targets.get(k) for k in self.keys_for_label]
        )

        _mask = [net_targets.get(k) for k in self.keys_for_label_mask]
        mask = pop_first_non_none_value(*_mask) if any(_mask) else None
        if mask is not None:
            mask = reshape_tensor_or_ndarray(mask)

        net_outputs = net_outputs.squeeze()
        label = label.squeeze()
        if mask is not None:
            mask = mask.squeeze()

        net_outputs_shape = tuple(net_outputs.shape)
        label_shape = tuple(label.shape)
        if net_outputs_shape == label_shape:
            if self.gate is not None:
                net_outputs = net_outputs > self.gate
        elif net_outputs_shape[:-1] == label_shape:
            net_outputs = net_outputs.argmax(dim=-1)
        else:
            raise f"shape is mismatch, net_outputs shape is {net_outputs_shape}, label shape is {label_shape}"

        net_outputs = reshape_tensor_or_ndarray(net_outputs, mask=mask)
        label = reshape_tensor_or_ndarray(label, mask=mask)
        return self.score_fn(label, net_outputs)


@register_score("core/score/accuracy")
class core_acc_score(core_base_score):
    def __init__(self, gate=0.5):
        super().__init__(accuracy_score, gate=gate)

    @classmethod
    @add_default_section_for_init("core/score/accuracy")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass


@register_score("core/score/recall")
class core_recall_score(core_base_score):
    def __init__(self, gate=0.5):
        super().__init__(recall_score, gate=gate)

    @classmethod
    @add_default_section_for_init("core/score/recall")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass


@register_score("core/score/precision")
class core_precision_score(core_base_score):
    def __init__(self, gate=0.5):
        super().__init__(precision_score, gate=gate)

    @classmethod
    @add_default_section_for_init("core/score/precision")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass


@register_score("core/score/f1")
class core_f1_score(core_base_score):
    def __init__(self, gate=0.5):
        super().__init__(f1_score, gate=gate)

    @classmethod
    @add_default_section_for_init("core/score/f1")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass


@register_score("core/score/matthews_corr")
class core_matthews_corr_score(core_base_score):
    def __init__(self, gate=0.5):
        super().__init__(matthews_corrcoef, gate=gate)

    @classmethod
    @add_default_section_for_init("core/score/f1")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass


@register_score("core/score/pearson_corr")
class core_pearson_corr_score(core_base_score):
    def __init__(self):
        super().__init__(lambda x, y: pearson_corr(x, y)[0])


@register_score("core/score/spearman_corr")
class core_spearman_corr_score(core_base_score):
    def __init__(self):
        super().__init__(lambda x, y: spearman_corr(x, y)[0])


@register_score("core/score/roc_auc")
class core_roc_auc_score(core_base_score):
    def __init__(self):
        super().__init__(roc_auc_score)

    def get_net_outputs(self, net_outputs):
        net_outputs = net_outputs.squeeze()
        net_outputs_shape = tuple(net_outputs.shape)
        if len(net_outputs_shape) == 1:
            return net_outputs
        if len(net_outputs_shape) == 2 and net_outputs_shape[-1] == 2:
            return net_outputs[:, 1]
        raise f"net_outputs shape is {net_outputs_shape}, is suitable for auc score"

    def get_net_target(self, net_targets):
        label = pop_first_non_none_value(
            *[net_targets.get(k) for k in self.keys_for_label]
        )

        assert all((label == 1) | (label == 0))
        return net_targets
