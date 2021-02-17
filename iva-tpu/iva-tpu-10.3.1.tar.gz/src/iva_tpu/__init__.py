# -*- coding: utf-8 -*-
"""IVA TPU Platform classes."""

from .tpu_device import TPUDevice, TPUInferenceQueue
from .tpu_program import TPUProgram


def open_device() -> TPUDevice:
    """Build platform tpu device."""
    return TPUDevice()


__all__ = ['TPUDevice', 'TPUProgram', 'open_device', 'TPUInferenceQueue']
