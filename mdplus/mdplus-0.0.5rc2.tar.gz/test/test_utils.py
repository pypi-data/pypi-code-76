import mdtraj as mdt
import os
import numpy as np
import pytest
from mdplus import utils, pca

rootdir = os.path.dirname(os.path.abspath('__file__'))
ncfile = os.path.join(rootdir, 'examples/test.nc')
pdbfile = os.path.join(rootdir, 'examples/test.pdb')

@pytest.fixture(scope="module")
def traj():
    t =  mdt.load(ncfile, top=pdbfile)
    return t.atom_slice(t.topology.select('name CA')).xyz

def test_check_dimensions():
    arr = np.zeros((5,4,3))
    arr2 = utils.check_dimensions(arr)
    assert arr.shape == arr2.shape
    arr3 = np.zeros((4, 3))
    arr4 = utils.check_dimensions(arr3)
    assert arr4.shape == (1, 4, 3)
    with pytest.raises(ValueError):
        arr = np.zeros((3,4,6))
        arr2 = utils.check_dimensions(arr)

def test_rmsd(traj):
    assert utils.rmsd(traj[0], traj[0]) < 0.001
    assert abs(utils.rmsd(traj[0], traj[1]) -  0.04557) < 0.01
    r = utils.rmsd(traj, traj[0])
    assert r.shape == (10,)
    r2 = utils.rmsd(traj, traj)
    assert r2.shape == (10, 10)
    assert abs(r2[5, 3] -  r2[3, 5]) < 0.0001

def test_fit(traj):
    ref = traj[0]
    x = traj[1] + 3.0
    y = traj[1] - 3.0
    x2 = utils.fit(x, ref)
    y2 = utils.fit(y, ref)
    assert np.abs(x2 - y2).max() < 0.01

def test_procrustes(traj):
    fitter = utils.Procrustes()
    fitter.fit(traj)
    t_fitted = fitter.transform(traj)

def test_zagzig_encode():
    i = np.array([1, -2, 3, -4])
    j = np.array([2, 5, 6, 9])
    e = pca.zagzig_encode(i)
    assert np.all(e == j)

def test_zagzig_decode():
    i = np.array([1, -2, 3, -4])
    j = np.array([2, 5, 6, 9])
    e = pca.zagzig_decode(j)
    assert np.all(e == i)

def test_stretch_squeeze_unsigned():
    i = np.array([1, 2, 3, 4])
    isq = pca.squeeze(i)
    i2 = pca.stretch(isq)
    assert np.all(i == i2)

def test_stretch_squeeze_signed():
    i = np.array([1, -2, 3, -4])
    isq = pca.squeeze(i)
    i2 = pca.stretch(isq)
    assert np.all(i == i2)
