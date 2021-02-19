#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Mon 21 Jan 2019 03:00:26 PM CST

# File Name: loss.py
# Description:

"""

import torch
from torch.nn import functional as F
from torch.distributions import Normal, kl_divergence
import math

def kl_div(mu, var):
    return kl_divergence(Normal(mu, var.sqrt()),
                         Normal(torch.zeros_like(mu),torch.ones_like(var))).sum(dim=1).mean()
 
def binary_cross_entropy(recon_x, x):
    return -torch.sum(x * torch.log(recon_x + 1e-8) + (1 - x) * torch.log(1 - recon_x + 1e-8), dim=-1)

