# pca.py - PCA routines for MD trajectory data.

from mdplus import fast
from mdplus.utils import Procrustes, check_dimensions, fit
from sklearn.decomposition import PCA as skPCA
import zlib
import xdrlib
import numpy as np

def zagzig_encode(iarr):
    iarr = np.array(iarr, dtype=np.int32)
    sign = np.abs((np.sign(iarr)-1)//2)
    iarr = (np.abs(iarr)*2 + sign).astype(np.uint32)
    return iarr

def zagzig_decode(iarr):
    iarr = np.array(iarr, dtype=np.uint32)
    neg = iarr % 2 == 1
    iarr = (iarr // 2).astype(np.int32)
    iarr = np.where(neg, -iarr, iarr)
    return iarr

def squeeze(ilist):
    iarr = np.array(ilist).flatten()
    signed = iarr.min() < 0
    if signed:
        iarr = zagzig_encode(iarr)
    else:
        iarr = iarr.astype(np.uint32)
    buff, bl = fast.pack(iarr)
    buff = buff.tobytes()
    bl = bl.astype(np.uint8)
    blz = zlib.compress(bl)
    lb = len(buff)
    if signed:
        lb = -lb
    off = np.array([lb], dtype=np.int32).tobytes()
    return off + buff + blz

def stretch(sq):
    off = np.frombuffer(sq[:4], dtype=np.int32)[0]
    signed = off < 0
    if signed:
        off = -off
    buff = np.frombuffer(sq[4:4+off], dtype=np.uint32).copy()
    blz = sq[4+off:]
    bl = np.frombuffer(zlib.decompress(blz), dtype=np.uint8).astype(np.uint32)
    iout = fast.unpack(buff, bl)
    if signed:
        iout = zagzig_decode(iout)
    return iout.astype(np.int32)

def pcazipsave(xyz, filename, explained_variance=0.75, residual_scale=200,
               eigenvector_scale=100):
    p = PCA(n_components=explained_variance)
    scores = p.fit_transform(xyz)
    evecs = p._pca.components_
    mean = p.mean
    n_frames, n_atoms, _ = xyz.shape
    n_vecs = p.n_components
    if residual_scale > 0:
        xfitted = fit(xyz, mean.reshape((n_atoms, 3)))
        residuals = xfitted - p.inverse_transform(scores)
        iresiduals = (residuals * residual_scale).astype(np.int32) 
    iscores = (scores * 1000).astype(np.int32)
    ievecs = (evecs * eigenvector_scale * np.sqrt(n_atoms)).astype(np.int32).flatten()
    imean = (mean * 1000).astype(np.int32).flatten()
    magic = np.frombuffer(bytearray('PCZX', 'utf-8'), dtype=np.int32)[0]
    metadata = np.array([magic, n_frames, n_atoms, n_vecs, residual_scale, eigenvector_scale], dtype=np.int32)
    header = np.concatenate([metadata, imean, ievecs])
    pa = xdrlib.Packer()
    with open(filename, 'wb') as f:
        pa.pack_bytes(squeeze(header))
        if residual_scale > 0:
            for i, r in zip(iscores, iresiduals):
                pa.pack_bytes(squeeze(np.concatenate((i, r.flatten()))))
                f.write(pa.get_buffer())
                pa.reset()
        else:
            for i in iscores:
                pa.pack_bytes(squeeze(i))
                f.write(pa.get_buffer())
                pa.reset()


def pcazipload(filename):
    with open(filename, 'rb') as f:
        u = xdrlib.Unpacker(f.read())
        header = stretch(u.unpack_bytes())
        magic = header[0].tobytes()
        if magic != b'PCZX':
            raise TypeError('Error, unrecognised file type (magic={})'.format(magic))
        n_frames, n_atoms, n_vecs, residual_scale, eigenvector_scale = header[1:6]
        meanoff = 6
        evecoff = meanoff + 3 * n_atoms
        mean = header[meanoff:evecoff].astype(np.float32) / 1000
        evecs = header[evecoff:].astype(np.float32).reshape((n_vecs, 3*n_atoms)) / (eigenvector_scale * np.sqrt(n_atoms))
        xyz = np.zeros((n_frames, n_atoms, 3), dtype=np.float32)
        for i in range(n_frames):
            data = stretch(u.unpack_bytes())
            scores = data[:n_vecs].astype(np.float32) / 1000
            if residual_scale > 0:
                residuals = data[n_vecs:].astype(np.float32) / residual_scale
                x = mean + np.dot(scores, evecs) + residuals
            else:
                x = mean + np.dot(scores, evecs)

            xyz[i] = x.reshape((n_atoms, 3))
    return xyz
 
class PCA(object):
    """
    PCA for MD trajectory data, with an API like scikit-learn PCA

    With a [n_frames, n_atoms, 3] array of coordinates:

        pca = PCA()
        pca.fit(X)
        scores = pca.transform(X)

    Attributes:
        n_atoms: int, number of atoms
        n_components: int, number of PCA components
        mean: [n_atoms, 3] array, mean structure
        eigenvalues: [n_components] array
        
    """
    def __init__(self, n_components=None):
        self.n_components = n_components
        self._pca = skPCA(n_components=self.n_components)

    def fit(self, traj):
        """
        Build the PCA model.

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.
        """
        traj = check_dimensions(traj)
        n_frames = traj.shape[0]
        self.n_atoms = traj.shape[1]

        if self.n_components is not None:
            if self.n_components > 1 and self.n_components > min(n_frames, 3 * self.n_atoms):
                raise ValueError('Error: cannot find {} principal components from a trajectory of {} frames of {} atoms'.format(self.n_components, n_frames, self.n_atoms))
          
        self._fitter = Procrustes()
        fitted_traj = self._fitter.fit_transform(traj)
        self._pca.fit(fitted_traj.reshape((n_frames, -1)))
        self.n_components = self._pca.n_components_
        self.eigenvalues = self._pca.explained_variance_
        self.mean = self._pca.mean_.reshape((self.n_atoms, 3))

    def transform(self, traj):
        """
        Transform the trajectory frames into the PCA space.

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.

        Returns:
            An [n_frames, n_components)
        """
        traj = check_dimensions(traj)
        n_atoms = traj.shape[1]
        if n_atoms != self.n_atoms:
            raise ValueError('Error: trajectory has {} atoms but the model requires {}'.format(n_atoms, self.n_atoms))
        traj = self._fitter.transform(traj)
        n_frames = traj.shape[0]
        return self._pca.transform(traj.reshape((n_frames, -1)))

    def inverse_transform(self, traj):
        """
        Transform frames back from PCA space to Cartesian space

        Args:
            traj: an [n_components] or [n_frames, n_components] array

        Returns:
            an [n_frames, n_atoms, 3] array
        """
        traj = np.array(traj)
        if len(traj.shape) > 2 or traj.shape[-1] != self.n_components:
            raise ValueError('Error: traj must be a vector of length {} or an array of shape [any,{}]'.format(self.n_components, self.n_components))
        if len(traj.shape) == 1:
            traj = traj.reshape((1, -1) )
        n_frames = len(traj)
        crds = self._pca.inverse_transform(traj)
        return crds.reshape((n_frames, self.n_atoms, 3))
        
    def fit_transform(self, traj):
        """
        Fit the PCA model and return the transformed data

        Args:
            traj: [n_frames, n_atoms, 3] numpy array of coordinates.

        Returns:
            An [n_frames, n_components] array
        """
        traj = check_dimensions(traj)
        self.fit(traj)
        return self.transform(traj)
        
