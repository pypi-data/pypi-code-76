"""
gpu.py
======
Module with helper functions for selecting and managing GPUs.
"""
import subprocess

import torch.cuda

class GPUAvailabilityException(Exception):
    """Raised when a GPU is not available."""

def get_unused_gpu_id():
    """Returns the ID of the GPU with most free memory. Note that the GPU may
    not actually be unused, just _least_ used.

    This function requires `nvidia-smi` to be installed on the system.
    """
    # based on the solution to
    # https://discuss.pytorch.org/t/it-there-anyway-to-let-program-select-free-gpu-automatically/17560/2
    try:
        gpu_entries = subprocess.check_output(
        ['nvidia-smi', '--format=csv', '--query-gpu=memory.free']
    ).decode('utf-8').splitlines()[1:]
    except FileNotFoundError:
        raise GPUAvailabilityException("nvidia-smi is unavailable")
    mib_entries = [int(entry.rstrip(' MiB')) for entry in gpu_entries]
    max_idx = 0
    max_entry = mib_entries[0]
    for idx, entry in enumerate(mib_entries):
        if entry > max_entry:
            max_entry = entry
            max_idx = idx
    return max_idx

def get_unused_gpu_string():
    """Returns a device string "cuda:<id>" for the GPU with most free
    memory.
    """
    idx = get_unused_gpu_id()
    return "cuda:{}".format(idx)

def clear_device_cache(device):
    if 'cuda' in device:
        with torch.cuda.device(device):
            torch.cuda.ipc_collect()
            torch.cuda.empty_cache()
