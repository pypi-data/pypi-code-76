from torch import nn


class Reshape(nn.Module):
    """
    Reshape Module

    Just a helper since PyTorch does not have one.
    """

    def __init__(self, *args):
        super(Reshape, self).__init__()
        self.shape = args

    def forward(self, x):
        return x.view(self.shape)
