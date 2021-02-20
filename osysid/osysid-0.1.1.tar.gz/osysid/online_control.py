import logging

import numpy as np
from control import lqr, StateSpace

from .online_linear_model import OnlineLinearModel

logger = logging.getLogger(__name__)

class OnlineLinearControl(OnlineLinearModel):
    def __init__(self, n: int, k: int, m: int = None, alpha: float = 1.0):
        super().__init__(n, k, m, alpha)
        
    def lqr(self, x):
        # given the current state x, what's the best way to control
        sys = StateSpace(self.A, self.B, self.C, )