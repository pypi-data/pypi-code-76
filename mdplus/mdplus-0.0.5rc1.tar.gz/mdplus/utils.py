# utils.py 
from mdplus.fast import rmsd_traj, fitted_traj, fitted_mean
import numpy as np

def rmsd(traj, xref):
    """
    Calculate rmsd between coordinates in traj and xref)

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array

    Returns:
        float or vector or array depending on dhapes of traj and xref
    """
    traj = check_dimensions(traj)
    xref = check_dimensions(xref)
    rmsd = np.zeros((len(traj), len(xref)))
    for i, r in enumerate(xref):
        rmsd[:, i] = rmsd_traj(traj, r)
    if rmsd.shape[1] == 1:
        rmsd = rmsd.flatten()
    if len(rmsd) == 1:
        rmsd = rmsd[0]
    return rmsd

def fit(traj, xref):
    """
    Least squares fit a trajectory to a reference structure

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array. if the latter,
              the first coordinate set is used for the fit.

    Returns:
        [n_frames, n_atoms, 3] array of fitted coordinates.f
    """
    traj = check_dimensions(traj)
    xref = check_dimensions(xref)
    
    fitted = fitted_traj(traj, xref[0])

    return fitted
    
def check_dimensions(traj):
    """
    Check and regularize a trajectory array
    """
    if not isinstance(traj, np.ndarray):
        traj = np.array(traj)
    if len(traj.shape) < 2 or len(traj.shape) > 3 or traj.shape[-1] != 3:
        raise ValueError('Error: traj must be an [n_atoms, 3] or [n_frames, n_atoms, 3] array')
    if len(traj.shape) == 2:
        traj = traj.reshape((1, -1, 3))
    return traj

class Procrustes(object):

    def __init__(self, max_its=10, drmsd=0.01):
        """
        Initialise a procrustes least-squares fitter.

        Args:
            max_its: int, maximum number of iterations
            drmsd: float, target rmsd between successive means for convergence
        """
        self.max_its = max_its
        self.drmsd = drmsd

    def fit(self, X):
        """
        Train the fitter.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        """
        X = check_dimensions(X)
        old_mean = X[0].copy()
        err = self.drmsd + 1.0
        it = 0
        while err > self.drmsd and it < self.max_its:
            it += 1
            new_mean = fitted_mean(X, old_mean)
            err = rmsd(old_mean, new_mean)
            old_mean = new_mean

        self.converged = err <= self.drmsd
        self.mean = old_mean
            
    def transform(self, X):
        """
        Least-squares fit the coordinates in X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        X = check_dimensions(X)
        return fit(X, self.mean)
    
    def fit_transform(self, X):
        """
        Train the fitter, and apply to X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        self.fit(X)
        return self.transform(X)
