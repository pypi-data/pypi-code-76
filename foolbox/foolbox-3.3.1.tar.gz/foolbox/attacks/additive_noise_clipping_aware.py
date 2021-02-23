from typing import Union, Any
from abc import ABC
from abc import abstractmethod
import eagerpy as ep

from ..devutils import atleast_kd

from .base import FixedEpsilonAttack
from .base import Criterion
from .base import Model
from .base import T
from .base import get_criterion
from .base import get_is_adversarial
from .base import raise_if_kwargs

from ..external.clipping_aware_rescaling import l2_clipping_aware_rescaling

from .additive_noise import L2Mixin, GaussianMixin, UniformMixin


class BaseL2ClippingAwareAdditiveNoiseAttack(L2Mixin, FixedEpsilonAttack, ABC):
    def __init__(self, *, clipping_aware: bool = True):
        self.clipping_aware = clipping_aware

    def run(
        self,
        model: Model,
        inputs: T,
        criterion: Union[Criterion, Any] = None,
        *,
        epsilon: float,
        **kwargs: Any,
    ) -> T:
        raise_if_kwargs(kwargs)
        x, restore_type = ep.astensor_(inputs)
        del inputs, criterion, kwargs

        min_, max_ = model.bounds
        p = self.sample_noise(x)
        if self.clipping_aware:
            epsilons = l2_clipping_aware_rescaling(x, p, epsilon, a=min_, b=max_)
        else:
            norms = self.get_norms(p)
            epsilons = epsilon / atleast_kd(norms, p.ndim)
        x = x + epsilons * p
        x = x.clip(min_, max_)

        return restore_type(x)

    @abstractmethod
    def sample_noise(self, x: ep.Tensor) -> ep.Tensor:
        raise NotImplementedError


class L2ClippingAwareAdditiveGaussianNoiseAttack(
    GaussianMixin, BaseL2ClippingAwareAdditiveNoiseAttack
):
    """Samples Gaussian noise with a fixed L2 norm after clipping

    Args:
        clipping_aware : Whether to use the clipping-aware rescaling.
    """

    pass


class L2ClippingAwareAdditiveUniformNoiseAttack(
    UniformMixin, BaseL2ClippingAwareAdditiveNoiseAttack
):
    """Samples uniform noise with a fixed L2 norm after clipping

    Args:
        clipping_aware : Whether to use the clipping-aware rescaling.
    """

    pass


class BaseL2RepeatedClippingAwareAdditiveNoiseAttack(L2Mixin, FixedEpsilonAttack, ABC):
    def __init__(
        self,
        *,
        repeats: int = 100,
        check_trivial: bool = True,
        clipping_aware: bool = True,
    ):
        self.repeats = repeats
        self.check_trivial = check_trivial
        self.clipping_aware = clipping_aware

    def run(
        self,
        model: Model,
        inputs: T,
        criterion: Union[Criterion, Any] = None,
        *,
        epsilon: float,
        **kwargs: Any,
    ) -> T:
        raise_if_kwargs(kwargs)
        x0, restore_type = ep.astensor_(inputs)
        criterion_ = get_criterion(criterion)
        del inputs, criterion, kwargs

        is_adversarial = get_is_adversarial(criterion_, model)

        min_, max_ = model.bounds

        result = x0
        if self.check_trivial:
            found = is_adversarial(result)
        else:
            found = ep.zeros(x0, len(result)).bool()

        for _ in range(self.repeats):
            if found.all():
                break

            p = self.sample_noise(x0)
            if self.clipping_aware:
                epsilons = l2_clipping_aware_rescaling(x0, p, epsilon, a=min_, b=max_)
            else:
                norms = self.get_norms(p)
                epsilons = epsilon / atleast_kd(norms, p.ndim)
            x = x0 + epsilons * p
            x = x.clip(min_, max_)
            is_adv = is_adversarial(x)
            is_new_adv = ep.logical_and(is_adv, ep.logical_not(found))
            result = ep.where(atleast_kd(is_new_adv, x.ndim), x, result)
            found = ep.logical_or(found, is_adv)

        return restore_type(result)

    @abstractmethod
    def sample_noise(self, x: ep.Tensor) -> ep.Tensor:
        raise NotImplementedError


class L2RepeatedClippingAwareAdditiveGaussianNoiseAttack(
    GaussianMixin, BaseL2RepeatedClippingAwareAdditiveNoiseAttack
):
    """Repeatedly samples uniform noise with a fixed L2 size

    Args:
        repeats : How often to sample random noise.
        check_trivial : Check whether original sample is already adversarial.
        clipping_aware : Whether to use the clipping-aware rescaling.
    """

    pass


class L2RepeatedClippingAwareAdditiveUniformNoiseAttack(
    UniformMixin, BaseL2RepeatedClippingAwareAdditiveNoiseAttack
):
    """Repeatedly samples uniform noise with a fixed L2 size

    Args:
        repeats : How often to sample random noise.
        check_trivial : Check whether original sample is already adversarial.
        clipping_aware : Whether to use the clipping-aware rescaling.
    """

    pass
