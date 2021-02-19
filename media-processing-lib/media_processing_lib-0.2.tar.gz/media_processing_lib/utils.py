import os
from tqdm import trange

def dprint(msg):
    assert "MPL_QUIET" in os.environ
    quiet = int(os.environ["MPL_QUIET"])
    assert quiet in (0, 1)
    if quiet == 0:
        print(msg)

def drange(*args, **kwargs):
    assert "MPL_QUIET" in os.environ
    quiet = int(os.environ["MPL_QUIET"])
    assert quiet in (0, 1)
    if quiet == 0:
        return trange(*args, **kwargs)
    else:
        return range(*args)
