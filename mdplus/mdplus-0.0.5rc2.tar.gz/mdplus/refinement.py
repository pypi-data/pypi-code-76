# refinement.py - 'SHAKE"-like routines to improve geometry.
import mdplus
from mdplus import fast
import mdtraj as mdt
import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist, squareform
from mdplus.utils import check_dimensions

def _xfix(Xin, Dref, known, pca=None, gtol=0.001, dtol=0.001, max_its=1000):
    """
    SHAKE-style real-space refinement, with adaptive conjugate gradient minimization approach
    
    Args:
        Xin: The original coordinates
        Dref: Target distances, D[known] where D is a condensed distance matrix
        known: Boolean matrix, True where values from Dref are the targets
        pca: An sklearn PCA model (optional). If provided, refinement will
             not change the position of the structure in this subspace.
        dtol: stopping criterion for RMD distance violations
        gtol: stopping criterion for the force gradient
        tol: convergence tolerance
        max_its: maximum number of refinement cycles

    Returns:
        Xnew: Optimised coordinates
    """
    
    Dold = pdist(Xin)[known]
    Xold = Xin
    DX = np.zeros_like(Xold)
    C = np.zeros_like(Xold)
    n = len(Xin)
    
    ij = []
    k = -1
    for i in range(n - 1):
        for j in range(i+1, n):
            k += 1
            if known[k]:
                ij.append((i, j))
                C[i] += 1
                C[j] += 1
    C = 1.0 / np.where(C == 0, 1, C)
    grad = gtol + 0.1
    d = dtol + 0.1
    it = 0
    ij = np.array(ij, dtype=np.int)
    DXold = None
    alpha = 1.0
    while it < max_its and grad > gtol and d > dtol:
        it += 1
        dd = 0.5 * (Dref - Dold) / Dold
        DX = fast.make_dx(Xold.astype(np.float32), dd.astype(np.float32), ij)
        DX = DX * C
        if DXold is not None:
            v0 = DXold.flatten()
            v1 = DX.flatten()
            gamma = np.dot(v1, v1)/ np.dot(v0, v0)
            DX = DX + gamma * DXold
        
        if pca is not None:
            # remove components of DX in the pca subspace:
            DX_embedded = pca.inverse_transform(pca.transform([pca.mean + DX]))[0] - pca.mean
            DX = DX - DX_embedded
        Xnew = Xold + DX * alpha
        Dnew = pdist(Xnew)[known]
        newerr = np.linalg.norm(Dref - Dnew)
        
        if DXold is None:
            olderr = newerr + 1.0
        while newerr > olderr:
            alpha = alpha * 0.5
            Xnew = Xold + DX * alpha
            Dnew = pdist(Xnew)[known]
            newerr = np.linalg.norm(Dref - Dnew)
        
        alpha = alpha * 1.1
        DD = Dnew - Dold
        grad = np.linalg.norm(DD) / np.linalg.norm(Dold)
        Dold = Dnew
        Xold = Xnew
        DXold = DX
        olderr = newerr
        d = np.sqrt((DD * DD).mean())
   
    if grad > gtol and d > dtol:
        print('warning: tolerance limit {} not reached in {} iterations'.format(gtol, max_its))
    return Xnew

class REFINE(object):

    def __init__(self, valence=6.0, max_its=1000, dtol=0.0001, gtol=0.0001):
        """
        A SHAKE-type Refiner. 

        Adjusts the coordinates in each snapshot in a trajectory to
        satisfy a set of distance constraints. The constraints may be
        provided explicitly or identified automatically from analysis
        of conserved distances in the structures in a training trajectory. 

        Args:
            valence:    float, used in automatic constraint identification.
                        Sets the distance matrix variance cutoff to
                        give a total of bond_order * n_atoms constraints.
                        The default value of 6 comes from assuming each
                        atom has 4 bonded neighbours, and each of these
                        has 3 further neighbours, so (4*3/2)  unique bonds.
                        United atom or CG models may want a smaller number.
                        Has no effect if a set of bonds is provided to the
                        fit() method.
            max_its:    int, maximum number of refinement iterations.
            dtol:       float, stopping criterion for RMD distance violations
            gtol:       float, stopping criterion for the force gradient

        Attributes:
            n_atoms:    int, number of atoms
            constraints: [n_constraints, 2] array of indices of constrained
                         atom pairs.
            d_ref:      [n_constraints] array of constrained distances.

        """
        self.valence = valence
        self.max_its = max_its
        self.dtol = dtol
        self.gtol = gtol

        self.n_atoms = None
        self.constraints = None
        self.d_ref = None
        self.pca = None

    def fit(self, X, constraints=None, pca=None):
        """
        Train the refiner.

        If bonds is None, bonds are guessed from analysis of X.

        Args:
            X: [N_frames, N_atoms, 3] numpy array of coordinates.
            constraints: [N_bonds, 2] array of "bonded" atoms.
            pca: A PCA model (optional). If provided, refinement will
                 not change the position of the structure in this subspace.
                
        """
        X = check_dimensions(X)
        self.n_atoms = X.shape[1]
        d = np.array([pdist(x) for x in X])
        d_mean = d.mean(axis=0)
        d_var = d.var(axis=0)
        if constraints is not None:
            self.constraints = constraints
            constrained = np.zeros((self.n_atoms, self.n_atoms), dtype=np.bool)
            constrained[:, :] = False
            for b in constraints:
                constrained[b[0], b[1]] = True
                constrained[b[1], b[0]] = True
            self._constrained = squareform(constrained)
        else:
            d_thresh = sorted(d_var)[int(self.n_atoms * self.valence)]
            self._constrained = d_var <= d_thresh
            constrained = squareform(self._constrained)
            self.constraints = []
            for i in range(self.n_atoms - 1):
                for j in range(i + 1, self.n_atoms):
                    if constrained[i, j]:
                        self.constraints.append([i, j])

        self.d_ref = d_mean[self._constrained]
        self.pca = pca

    def transform(self, X):
        """
        Refine sets of coordinates.

        Args:
            X: [n_frames, n_atoms_3] or [n_atoms, 3] numpy array of coordinates

        Returns:
           [n_frames, n_atoms, 3] numpy array of refioned coordinates.
        """
        X = check_dimensions(X)
        if X.shape[1] != self.n_atoms:
            raise ValueError('Error: number of atoms in array to refine ({}) does not match number used to train refiner ({})'.format(X.shape[1], self.n_atoms))
        Xout = []
        for Xc in X:
            Xout.append(_xfix(Xc, self.d_ref, self._constrained, self.pca, 
                        self.gtol, self.dtol, self.max_its))
        return np.array(Xout)
