import torch.optim as optim
from unitorch import register_optim
from unitorch.core import core_class
from unitorch.utils.decorators import add_default_section_for_init


@register_optim("core/optim/adam")
class core_adam_optim(core_class):
    def __init__(self, learning_rate=0.0001):
        self.learning_rate = learning_rate

    @classmethod
    @add_default_section_for_init("core/optim/adam")
    def init_from_core_configure(cls, cfg, **kwargs):
        pass

    def __call__(self, params):
        return optim.Adam(params, lr=self.learning_rate)
