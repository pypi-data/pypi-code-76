import numpy as np
from scipy import interpolate
import pandas as pd

def read_rx_spectrum(file_name, interpolation="cubic", normalise=False):
    # Resolution of IMon 512 USB is 0.166015625 nm = 166.015 pm
    x = np.arange(1510,1595,0.166015625,dtype=float)
    dx = np.arange(1510,1595,0.001000000,dtype=float)

    df = pd.read_csv(file_name,sep="\t",error_bad_lines=False)
    df = df[[f"Pixel {i}" for i in range(1, 513)]]
    # calculate mean of all the entries and reverse it
    mean = df.mean().values[::-1]


    if interpolation == "cubic":
        # perform cublic spline interpolation
        cs = interpolate.CubicSpline(x, mean)
        dy = cs(dx)

    if normalise:
        dy = dy /max(dy)

    return dx, dy
