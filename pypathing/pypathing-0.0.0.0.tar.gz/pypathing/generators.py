"generators of mazes"


from .scr import cy_generators

import numpy as np

def prim(x_size: int, y_size: int, seed:int=0, reprProb:float=.1) -> np.ndarray:
    """prim maze generation

        prim maze generation of a maze of size x_size, y_size

        @param reprProb: the probability of continuening computations after first connection
        @param seed: the seed of the mazes generation random function
        """
    if x_size%2==0: raise ValueError(f"x_size must be odd not {x_size}")
    if y_size%2==0: raise ValueError(f"y_size must be odd not {y_size}")
    v = cy_generators.prim(x_size, y_size, seed%2_147_483_647, int(reprProb*100))
    return np.array(v).reshape(x_size, y_size)

def rand_terain(x_size: int, y_size: int, prob: float=.5):
    """generate random terain of size x_size X y_size with unwakable probability prob
        """
    arr = np.random.rand(x_size, y_size)
    out = np.zeros((x_size, y_size), dtype=np.int8)
    out[arr>prob] = 1
    return out