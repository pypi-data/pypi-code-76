import mdtraj as mdt
import os
import numpy as np
import pytest
from mdplus import refinement
from mdplus.utils import rmsd

rootdir = os.path.dirname(os.path.abspath('__file__'))
ncfile = os.path.join(rootdir, 'examples/test.nc')
pdbfile = os.path.join(rootdir, 'examples/test.pdb')
pczfile = os.path.join(rootdir, 'examples/test.pcz')
pczfile_dm = os.path.join(rootdir, 'examples/test_dm.pcz')

@pytest.fixture(scope="module")
def traj():
    t =  mdt.load(ncfile, top=pdbfile)
    return t.atom_slice(t.topology.select('name CA')).xyz

def test_fit(traj):
    r = refinement.REFINE(valence=3)
    r.fit(traj)
    assert r.n_atoms == 58
    assert len(r.constraints) == 175

def test_transform(traj):
    r = refinement.REFINE()
    r.fit(traj)
    ref = traj[0]
    crude = ref + (np.random.random(ref.shape) * 0.02) - 0.01 
    refined = r.transform(crude)
