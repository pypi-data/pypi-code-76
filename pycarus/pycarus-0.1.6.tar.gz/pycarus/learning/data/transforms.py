from typing import Callable, List

import torch


class Compose:
    """Composes several transforms together.

    Each transform should be  an instance of a class with a __call__ method.

    Args:
        transforms: the transform to apply.
    """

    def __init__(self, transforms: List[Callable]) -> None:
        self.transforms = transforms

    def __call__(self, data: torch.Tensor) -> torch.Tensor:
        for t in self.transforms:
            data = t(data)
        return data

    def __repr__(self) -> str:
        format_string = self.__class__.__name__ + "("
        for t in self.transforms:
            format_string += "\n"
            format_string += "    {0}".format(t)
            format_string += "\n)"
        return format_string
