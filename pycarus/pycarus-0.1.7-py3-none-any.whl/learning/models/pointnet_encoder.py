from typing import List

import torch
from torch import nn as nn


class PointNetEncoder(nn.Module):
    """Model class respresenting a point cloud encoder based on PointNet as proposed in:

    Groueix, Thibault, et al. "A papier-mâché approach to learning 3d surface generation."
    Proceedings of the IEEE conference on computer vision and pattern recognition. 2018.

    The model performs 1D convolution on the input point cloud followed by a max pooling operator,
    like in PointNet. Eventually, linear layers can be added to increase the depth of the network
    and change the size of the latent code. In this case the latent space will have the same number
    of output channels as in the last linear layer.
    """

    def __init__(
        self,
        input_channels: int = 3,
        size_latent: int = 1024,
        convolutions: List[int] = [64, 128],
        linears: List[int] = [1024, 1024],
    ) -> None:
        """Create an instance of PointNetEncoder.

        Args:
            input_channels: the number of point cloud coordinates. Defaults to 3.
            size_latent: the size for the latent space. Defaults to 1024.
            convolutions: the output channels for the 1D convolutions. Defaults to [64, 128, 1024].
            linears: the output channels for the fully connected. Defaults to [1024, 1024].
        """
        super(PointNetEncoder, self).__init__()  # type: ignore
        self.size_latent = size_latent
        self.dim_input = input_channels

        if len(linears):
            if self.size_latent != linears[0]:
                raise ValueError("The out channel of first linear layer must match size_latent.")

        list_convolutions = nn.ModuleList()
        for idx in range(len(convolutions)):
            in_ch_conv = self.dim_input if idx == 0 else convolutions[idx - 1]
            out_ch_conv = convolutions[idx]
            list_convolutions.append(nn.Conv1d(in_ch_conv, out_ch_conv, 1))
            list_convolutions.append(nn.BatchNorm1d(out_ch_conv))  # type: ignore
            list_convolutions.append(nn.ReLU())

        # Last convolution without ReLu
        list_convolutions.append(nn.Conv1d(convolutions[-1], self.size_latent, 1))
        list_convolutions.append(nn.BatchNorm1d(self.size_latent))  # type: ignore
        self.convolutions = nn.Sequential(*list_convolutions)

        list_linears = nn.ModuleList()
        for idx in range(len(linears)):
            in_ch_lin = self.size_latent if idx == 0 else linears[idx - 1]
            out_ch_lin = linears[idx]
            list_linears.append(nn.Linear(in_ch_lin, out_ch_lin))
            list_linears.append(nn.BatchNorm1d(out_ch_lin))  # type: ignore
            list_linears.append(nn.ReLU())

        self.linears = nn.Sequential(*list_linears)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Process input point cloud patches and produce a sequence of embeddings.

        Args:
            x: The input point cloud with shape (BATCH, NUM_POINTS, 3). The method internally
            transposes the data tensor to correctly operate with PyTorch convetion (B CH N).

        Returns:
            The embeddings with shape (BATCH, SIZE_LATENT).
        """
        size_batch = x.shape[0]
        x_channel_first = torch.transpose(x, 2, 1)
        x = self.convolutions(x_channel_first)
        x, _ = torch.max(x, 2)
        x = x.view(size_batch, self.size_latent)

        if len(self.linears):
            x = self.linears(x)

        return x

    def __repr__(self) -> str:
        layer_str = ""
        for name, param in self.named_parameters():
            if "kernel" in name:
                layer_str += "Name: {} - Shape {}".format(name, param.transpose(2, 1).shape) + "\n"

        return super(PointNetEncoder, self).__repr__() + layer_str  # type: ignore
