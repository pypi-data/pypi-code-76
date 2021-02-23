import numpy as np
from geepy import simbinCLF
mu = np.array([0.4, 0.3, 0.2])
stdev = np.array([[1, 0.03, 0.03], [0.03, 1, 0.03], [0.03, 0.03, 1]])
A = simbinCLF(mu, stdev)
A.simulate()