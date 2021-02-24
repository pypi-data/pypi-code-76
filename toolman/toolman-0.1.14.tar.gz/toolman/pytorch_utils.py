"""

"""


# Built-in
import os
import timeit

# Libs
import torch
import torchvision
import numpy as np
from torch import nn
from torchsummary import summary

# Own modules


def set_gpu(gpu, enable_benchmark=True):
    """
    Set which gpu to use, also return True as indicator for parallel model if multi-gpu selected
    :param gpu: which gpu(s) to use, could allow a string with device ids separated by ','
    :param enable_benchmark: if True, will let CUDNN find optimal set of algorithms for input configuration
    :return: device instance
    """
    if not torch.cuda.is_available():
        return torch.device('cpu'), False
    if not isinstance(gpu, str):
        gpu = str(int(gpu))
    if len(str(gpu)) > 1:
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu
        parallel = True
        device = torch.device("cuda:{}".format(','.join([str(a) for a in range(len(gpu.split(',')))])))
        print("Devices being used: cuda:", gpu)
    else:
        parallel = False
        device = torch.device("cuda:{}".format(gpu))
        print("Device being used:", device)
    torch.backends.cudnn.benchmark = enable_benchmark
    return device, parallel


def set_random_seed(seed_):
    """
    Set random seed for torch, cudnn and numpy
    :param seed_: random seed to use, could be your lucky number :)
    :return:
    """
    torch.manual_seed(seed_)
    torch.backends.cudnn.deterministic = True
    np.random.seed(seed_)


def get_model_summary(model, shape, device=None):
    """
    Get model summary with torchsummary
    :param model: the model to visualize summary
    :param shape: shape of the input data
    :return:
    """
    if not device:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    summary(model.to(device), shape)


def get_model_size(model):
    """
    Get the size of the models
    :param model:
    :return:
    """
    return sum(p.numel() for p in model.parameters()) / 1000000.0


class LossMeter(nn.Module):
    """
    A meter for calculated loss
    """
    def __init__(self, name, func=None):
        super(LossMeter, self).__init__()
        self.loss = 0
        self.cnt = 0
        self.name = f'meter_{name}'
        self.func = func

    def forward(self, pred, lbl):
        loss = self.func(pred, lbl)
        self.loss += loss.item() * pred.size(0)
        self.cnt += 1
        return loss

    def reset(self):
        """
        Reset the loss tracker
        :return:
        """
        self.loss = 0
        self.cnt = 0

    def get_loss(self):
        """
        Get mean loss within this epoch
        :return:
        """
        return self.loss / self.cnt


def infi_loop_loader(dl):
    """
    An iterator that reloads after reaching to the end
    :param dl: data loader
    :return: an endless iterator
    """
    while True:
        for x in dl: yield x


if __name__ == '__main__':
    pass
