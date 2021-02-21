import torch
import torch.nn as nn
from unitorch import register_loss
from unitorch.core import core_class
from unitorch.functions import pop_first_non_none_value
from unitorch.utils.decorators import add_default_section_for_init


def add_sample_weight_for_loss(loss, sample_weight):
    if loss.dim() == 2:
        loss = loss.squeeze()

    if sample_weight is not None:
        loss = torch.sum(loss * sample_weight) / torch.sum(sample_weight)
    else:
        loss = torch.mean(loss)

    return loss


@register_loss("core/loss/ce")
class core_ce_loss(core_class):
    def __init__(self, smoothing_alpha=0.0):
        self.smoothing_alpha = smoothing_alpha

    @classmethod
    @add_default_section_for_init("core/loss/ce")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def __call__(self, net_outputs, net_targets):
        assert net_outputs.dim() == 2
        label = net_targets.get("label")
        sample_weight = net_targets.get("sample_weight")

        assert label.dim() == 1
        label = label.long()
        if self.smoothing_alpha == 0:
            loss = nn.CrossEntropyLoss(reduction="none")(net_outputs, label).squeeze()
        else:
            batch_size, num_class = net_outputs.size()
            smooth_label = torch.full(
                size=(batch_size, num_class),
                fill_value=self.smoothing_alpha / (num_class - 1),
            ).to(loss)
            smooth_label.scatter_(
                dim=1,
                index=torch.unsqueeze(label, dim=1),
                value=(1 - self.smoothing_alpha),
            )
            log_logits = torch.nn.functional.log_softmax(net_outputs, dim=1)
            loss = log_logits * smooth_label

        return add_sample_weight_for_loss(loss, sample_weight)


@register_loss("core/loss/bce")
class core_bce_loss(core_class):
    def __init__(self):
        pass

    @classmethod
    @add_default_section_for_init("core/loss/bce")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def __call__(self, net_outputs, net_targets):
        assert net_outputs.dim() == 2
        label = net_targets.get("label")
        sample_weight = net_targets.get("sample_weight")
        if label.dim() == 1:
            label = label.unsqueeze(-1)

        assert label.dim() == 2
        label = label.float()
        loss = nn.BCEWithLogitsLoss(reduction="none")(net_outputs, label).squeeze()

        return add_sample_weight_for_loss(loss, sample_weight)


@register_loss("core/loss/lm")
class core_lm_loss(core_class):
    def __init__(self, smoothing_alpha=0.0):
        self.smoothing_alpha = smoothing_alpha
        self.keys_for_label = ["label", "next_tokens_ids"]
        self.keys_for_label_mask = ["label_mask", "next_tokens_mask"]

    @classmethod
    @add_default_section_for_init("core/loss/lm")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def __call__(self, net_outputs, net_targets):
        assert net_outputs.dim() == 3
        label = pop_first_non_none_value(
            *[net_targets.get(k) for k in self.keys_for_label]
        )
        label_mask = pop_first_non_none_value(
            *[net_targets.get(k) for k in self.keys_for_label_mask]
        )
        sample_weight = net_targets.get("sample_weight")

        batch_size, seq_len, num_class = net_outputs.size()
        logits = net_outputs.contiguous().view(batch_size * seq_len, num_class)
        label = label.contiguous().view(-1)
        label_mask = label_mask.contiguous().view(-1)
        loss = nn.CrossEntropyLoss(reduction="none")(logits, label)
        loss = loss * label_mask.float()
        loss = loss.contiguous().view(batch_size, seq_len).sum(1) / torch.max(
            label_mask.contiguous().view(batch_size, seq_len).float().sum(1),
            torch.ones(batch_size).to(label_mask.device),
        )
        return add_sample_weight_for_loss(loss, sample_weight)


@register_loss("core/loss/qa")
class core_qa_loss(core_class):
    def __init__(self):
        pass
