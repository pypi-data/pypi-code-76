import mdtraj as mdt
import os
import numpy as np
import pytest
from mdplus import multiscale
from mdplus.utils import rmsd

rootdir = os.path.dirname(os.path.abspath('__file__'))
ncfile = os.path.join(rootdir, 'examples/test.nc')
pdbfile = os.path.join(rootdir, 'examples/test.pdb')
pczfile = os.path.join(rootdir, 'examples/test.pcz')
pczfile_dm = os.path.join(rootdir, 'examples/test_dm.pcz')

@pytest.fixture(scope="module")
def cg_traj():
    t =  mdt.load(ncfile, top=pdbfile)
    return t.atom_slice(t.topology.select('name CA')).xyz

@pytest.fixture(scope="module")
def fg_traj():
    t = mdt.load(ncfile, top=pdbfile)
    return t.xyz

def test_fit(cg_traj, fg_traj):
    g = multiscale.GLIMPS(x_valence=2)
    g.fit(cg_traj, fg_traj)

def test_fit_transform(cg_traj, fg_traj):
    g = multiscale.GLIMPS(x_valence=2)
    g.fit(cg_traj, fg_traj)
    ref = fg_traj[0]
    cg = cg_traj[0]
    fg = g.transform(cg)
    assert rmsd(ref, fg) < 0.2
