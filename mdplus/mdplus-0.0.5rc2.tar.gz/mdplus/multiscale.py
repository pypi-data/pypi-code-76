import mdtraj as mdt
from mdtraj.geometry import alignment
import numpy as np
import pickle
from mdplus.pca import PCA
from mdplus.refinement import REFINE
from sklearn.linear_model import LinearRegression
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans

class GLIMPS(object):
    """
    A resolution transformer

    GLIMPS is a machine learning approach to resolution transformation
    targetted primarily at molecular structures (sets of 3D coordinates).

    Once trained on a matched set of higher and lower resolution models of
    a system, GLIMPS can transform further samples between the two resolutions
    in either direction.

    The API is modelled on that used by ML methods in scipy and sklearn:

    Instantiate a transformer:
    
        transformer = GLIMPS()

    Train a transformer:

        transformer.fit(Xtrain, Ytrain)

        where Xtrain[n_samples, n_xparticles, 3] and 
        Ytrain[n_samples, n_yparticles, 3] are matched pairs of structures 
        at the two resolutions.

    Apply a transformer X->Y:

        Ypred = transformer.transform(Xtest)

    Apply the inverse transform:

       Xpred = transformer.inverse_transform(Ytest)

    Save the trained transformer (pickle format):

        transformer.save("XYtransformer.pkl")
        
    """
    
    def __init__(self, refine=True, x_valence=4, y_valence=4):
        """
        Initiate a GLIMPS resolution transformer

        Args:

            refine: Bool, if True, perform SHAKE-style refinement on
                    crude resolution transformed coordinates.

            x_valence: int, "valency" of models in X. Controls the
                       automatic identification of "bonds" in the
                       structures in X for SHAKE refinement. Typically
                       a value of 4 works for all-atom coordinate sets,
                       but 3 or 2 may be better for CG coordinates. Has
                       no effect if refine=False.

            y_valence: int, as above for the Y samples.
        """

        self.refine = refine
        self.x_valence = x_valence
        self.y_valence = y_valence
        self.pca_x = None
        self.pca_y = None
        self.x_refiner = None
        self.y_refiner = None
        self.xy_regressor = None
        self.yx_regressor = None
        self.n_components = None
        self.xy_score = None  # not currently used
        self.yx_score = None  # not currently used
        
    def _get_tr(self, traj, ref):
        """
        Return a list of translation vectors and rotation matrices to map x onto ref
        """
    
        n = len(traj)
        trans = np.zeros((n, 3))
        rot = np.zeros((n, 3, 3))
        for i, x in enumerate(traj):
            trans[i], rot[i] = alignment.compute_translation_and_rotation(x, ref)
        return trans, rot

    def _apply_tr(self, traj, t, r, inverse=False):
        """
        Apply translations and rotations to snapshots in traj.
        """
        result = np.zeros_like(traj)
        for i, x in enumerate(traj):
            if inverse:
                result[i] = (x - t[i]).dot(r[i].T)
            else:
                result[i] = x.dot(r[i]) + t[i]
        return result

    def fit(self, X, Y):
        """
        Train a resolution transformer that maps from X to Y, and the reverse.

        Args:

            X: [n_samples, n_xparticles, 3] array of coordinates
            Y: [n_samples, n_yparticles, 3] array of coordinates
            
        """
        X = np.array(X)
        Y = np.array(Y)
        shape_x = X.shape
        shape_y  = Y.shape
        if not len(shape_x) == 3:
            raise ValueError('Error: X must be shape [n_samples, n_xatoms, 3]')
        if not len(shape_y) == 3:
            raise ValueError('Error: Y must be shape [n_samples, n_yatoms, 3]') 
        if not shape_x[0] == shape_y[0]:
            raise ValueError('Error: X and Y must be matched samples')
        if not shape_x[2] == 3:
            raise ValueError('Error: X must be shape [n_samples, n_xatoms, 3]')
        if not shape_y[2] == 3:
            raise ValueError('Error: Y must be shape [n_samples, n_yatoms, 3]')
        
        self.n_components = min(len(X), shape_x[1] * 3, shape_y[1] * 3)
        if self.n_components < 2:
            raise ValueError('Error: insufficient samples for fitting')

        self.pca_x = PCA(n_components=self.n_components)
        self.pca_y = PCA(n_components=self.n_components)
        self.pca_x.fit(X)
        self.pca_y.fit(Y)
        
        if self.refine:
            self.x_refiner = REFINE(valence=self.x_valence)
            self.x_refiner.fit(X, pca=self.pca_x)
            self.y_refiner = REFINE(valence=self.y_valence)
            self.y_refiner.fit(Y, pca=self.pca_y)
        
        x_scores = self.pca_x.transform(X)
        y_scores = self.pca_y.transform(Y)
        self.xy_regressor = LinearRegression().fit(x_scores, y_scores)
        #self.xy_score = self.xy_regressor.score(x_scores, y_scores)
        self.yx_regressor = LinearRegression().fit(y_scores, x_scores)
        #self.yx_score = self.yx_regressor.score(y_scores, x_scores)
        
    def transform(self, X):
        """
        Transform X to the resolution of Y

        Args:

            X: [n_samples, n_xparticles, 3] array of coordinates.

        Returns:

            Y: [n_samples, n_yparticles, 3] array of coordinates.
        """
        if self.xy_regressor is None:
            raise RuntimeError('Error: model has not been trained yet')
            
        X = np.array(X)
        n_dims = len(X.shape)
        if n_dims < 2 or n_dims > 3:
            raise ValueError('Error: X must be an [n_atoms, 3] or [n_samples, n_atoms, 3] array')
        one_frame = n_dims == 2
        if one_frame:
            X = np.array([X])
        if X.shape[2] != 3:
            raise ValueError('Error: X must be an [n_atoms, 3] or [n_samples, n_atoms, 3] array')
        if X.shape[1] != self.pca_x.n_atoms:
            raise ValueError('Error: X contains {} atoms, was expecting {}'.format(X.shape[1], self.pca_x.n_atoms))
        t, r = self._get_tr(X, self.pca_x.mean)
        x_scores = self.pca_x.transform(X)
        y_scores = self.xy_regressor.predict(x_scores)
        Y = self.pca_y.inverse_transform(y_scores)
        if self.refine:
            Y = self.y_refiner.transform(Y)
        Y = self._apply_tr(Y, t, r, inverse=True)
        if one_frame:
            Y = Y[0]
        return Y
    
    def inverse_transform(self, Y):
        """
        Transform Y to the resolution of X

        Args:

            Y: [n_samples, n_yparticles, 3] array of coordinates.

        Returns:

            X: [n_samples, n_xparticles, 3] array of coordinates.
        """
        if self.yx_regressor is None:
            raise RuntimeError('Error: model has not been trained yet')
            
        Y = np.array(Y)
        n_dims = len(Y.shape)
        if n_dims < 2 or n_dims > 3:
            raise ValueError('Error: Y must be an [n_atoms, 3] or [n_samples, n_atoms, 3] array')
        one_frame = n_dims == 2
        if one_frame:
            Y = np.array([Y])
        if Y.shape[2] != 3:
            raise ValueError('Error: Y must be an [n_atoms, 3] or [n_samples, n_atoms, 3] array')
        if Y.shape[1] != self.pca_y.n_atoms:
            raise ValueError('Error: Y contains {} atoms, was expecting {}'.format(Y.shape[1], self.pca_y.n_atoms))
        t, r = self._get_tr(Y, self.pca_y.mean)
        y_scores = self.pca_y.transform(Y)
        x_scores = self.yx_regressor.predict(y_scores)
        X = self.pca_x.inverse_transform(x_scores)
        if self.refine:
            X = self.x_refiner.transform(X)
        X = self._apply_tr(X, t, r, inverse=True)
        if one_frame:
            X = X[0]
        return X

    def save(self, filename):
        """
        Save a transformer to a file

        Args:

            filename: str, name of the file (python pickle format)
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

class TrajGLIMPS(object):
    """
    GLIMPS for MDTraj trajectories.

    Should really be a subclass of GLIMPS.
    """
    def __init__(self, chunksize=100, refine=True, x_valence=4, y_valence=4):
        self.chunksize = chunksize
        self.refine = refine
        self.x_valence = x_valence
        self.y_valence = y_valence
        self.glimpss = []

    def _split(self, traj):
        """
        Split up a trajectory
        """
        nr = traj.topology.n_residues
        rinds = [r.index for r in traj.topology.residues]
        nchunks = int(np.ceil(nr / self.chunksize))
        cs = int(np.ceil( nr / nchunks))
        trajs = []
        for i in range(0, nr, cs):
            r1 = rinds[i]
            r2 = rinds[i + cs - 1]
            sel = 'resid {} to {}'.format(r1, r2)
            ats = traj.topology.select(sel)
            trajs.append(traj.atom_slice(ats))
        return trajs

    def fit(self, X, Y):
        """
        Train a resolution transformer that maps from X to Y, and the reverse.
        """
        self.x_topology = X.topology
        self.y_topology = Y.topology
        xs = self._split(X)
        ys = self._split(Y)
        for x, y in zip(xs, ys):
            glimps = GLIMPS(refine=self.refine, x_valence=self.x_valence, 
                      y_valence=self.y_valence)
            glimps.fit(x.xyz, y.xyz)
            self.glimpss.append(glimps)
            
    def transform(self, X):
        """
        Transform X to the resolution of Y
        """
        xs = self._split(X)
        Y = None
        for i, x in enumerate(xs):
            y = self.glimpss[i].transform(x.xyz)
            if Y is None:
                Y = y
            else:
                Y = np.hstack([Y, y])
        return mdt.Trajectory(Y, self.y_topology)
        
    def inverse_transform(self, Y):
        """
        Transform Y to the resolution of X
        """
        ys = self._split(Y)
        X = None
        for i, y in enumerate(ys):
            x = self.glimpss[i].inverse_transform(y.xyz)
            if X in None:
                X = x
            else:
                X = np.hstack([X, x])
        return mdt.Trajectory(X, self.x_topology)
        
    def save(self, filename):
        """
        Save a transformer to a file
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

class SolMapper(object):
    """
    A solvent mapper.

    This does not use the GLIMPS method at all, but is included here
    as it adopts the same API.
    """
    def __init__(self):
        self.cg_res = None
        self.fg_cluster = None
        
    def fit(self, cg_traj, fg_traj):
        """
        Train the mapper
        """
        self.n_merge = fg_traj.topology.n_residues // cg_traj.topology.n_residues
        self.cg_res = cg_traj.topology.residue(0)
        
        r_atoms = fg_traj.topology.residue(0).n_atoms
        cluster_size = self.n_merge 
        done = False
        while not done:
            rand_res = np.random.randint(fg_traj.topology.n_residues)
            rand_at = rand_res * r_atoms
            d = cdist(fg_traj.xyz[0,rand_at:rand_at+1], fg_traj.xyz[0,::r_atoms])[0]
            
            n_clusters = 10
            n_map = r_atoms * n_clusters
            r_neighs = np.argsort(d)[:n_map] * r_atoms
            kmeans = KMeans(n_clusters=n_clusters).fit(fg_traj.xyz[0, r_neighs])
            clusters = []
            for i in range(n_clusters):
                clusters.append(np.where(kmeans.labels_ == i)[0])
                
            minvar = None
            cv = None
            for cluster in clusters:
                if len(cluster) == cluster_size:
                    v = pdist(fg_traj.xyz[0, r_neighs[cluster]]).var()
                    if minvar is None:
                        minvar = v
                        cv = cluster
                    elif v < minvar:
                        minvar = v
                        cv = cluster
            done = cv is not None
            
        a_neighs = []
        for r in r_neighs[cv]:
            a_neighs += list(range(r, r + r_atoms))
        self.fg_cluster = fg_traj[0].atom_slice(a_neighs)
        self.fg_cluster.xyz -= self.fg_cluster.xyz[0].mean(axis=0)
        
    def transform(self, cg_traj):
        """
        Convert a cg trajectory to a fg trajectory
        """
        n_frames = cg_traj.n_frames
        n_cg_residues = cg_traj.topology.n_residues
        n_cg_atoms = cg_traj.topology.residue(0).n_atoms
        n_fg = self.fg_cluster.n_atoms
        n_fg_atoms = n_cg_residues * n_fg
        xyz_fg = np.zeros((n_frames, n_fg_atoms, 3))
        ref_crds = self.fg_cluster.xyz[0]
        
        for iframe, xyz in enumerate(cg_traj.xyz[:, ::n_cg_atoms]):
            for iat, x in enumerate(xyz):
                xyz_fg[iframe, iat * n_fg:(iat+1) * n_fg] = ref_crds + x
        
        fg_top = mdt.Topology()
        for iat in range(n_cg_residues):
            for r in self.fg_cluster.topology.residues:
                chain = fg_top.add_chain()
                res = fg_top.add_residue(r.name, chain)
                for a in r.atoms:
                    fg_top.add_atom(a.name, a.element, res)
        return mdt.Trajectory(xyz_fg, fg_top)
    
    def inverse_transform(self, fg_traj):
        """
        Convert a fg trajectory to a cg trajectory
        """
        return _sol_cg(fg_traj, self.cg_res, self.n_merge)

    def save(self, filename):
        """
        Save a transformer to a file
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

def _sol_cg(t_fg, cg_res, n_merge):
    """
    Produce a CG representation of the solvent in t_fg
    
    Args:
        t_fg: MDTraj trajectory of fine-grained solvent
        cg_res: MDTraj residue object for a cg solvent molecule
        n_merge: int, number of fg solvent molecules that map onto a 
                 single cg solvent molecule
    Returns:
        MDTraj trajectory of CG solvent

    The method is approximate, but as follows:
    
    1. CG particles will be placed at the position of the first atom
       in 1/n_merge-th of the fine-grained solvent molecules.
    2. The subsample is chosen as follows:
       2a. Take every (n_merge-1)th molecule (i.e., too many)
       2b. Calculate the distances between all molecules (1st atoms of each)
       2c. Calculate the minimium distance between each molecule and any other
       2d. Cull the list, removing one of each pair that is most close, until
           just 1/n_merge-th of the initial number of molecules remains.
    3. Create a new trajectory from these selected atoms.
    """
    r_atoms = t_at.topology.residue(0).n_atoms # number of atoms per residue
    t = t_at.atom_slice(range(0, t_at.n_atoms, r_atoms))
    sample_xyz = t.xyz[:,::(n_merge - 1)] # coordinates of every (n_merge -1)th 1st atoms
    n_samples = len(sample_xyz[0])
    cg_xyz = np.zeros((t.n_frames, t.topology.n_atoms // n_merge, 3))
    for iframe in range(len(sample_xyz)):
        d = squareform(pdist(sample_xyz[iframe]))
        dmax = d.max()
        for i in range(len(d)):
            d[i,i] = dmax
        dmin = d.min(axis=0)

        n_cg = t.n_atoms // n_merge
        n_cull = n_samples - n_cg

        tmp_indx = np.argsort(dmin)
        tmp_indx[:2 * n_cull:2] = -1 # remove one atom from each too-close pair
        cg_indx = np.where(tmp_indx > -1)[0]
        cg_xyz[iframe] = sample_xyz[iframe, cg_indx]

    cg_top = mdt.Topology()
    for i in range(n_cg):
        c = cg_top.add_chain()
        r = cg_top.add_residue(cg_res.name, c)
        for a in cg_res.atoms:
            cg_top.add_atom(a.name, a.element, r)
    t_cg = mdt.Trajectory(cg_xyz, cg_top)
    return t_cg

def load_transformer(filename):
    """
    Load a GLIMPS (or solvent) transformer from a file
    """
    with open(filename, 'rb') as f:
        glimps = pickle.load(f)
    return glimps

def compile_topologies(trajdict, sequence):
    """
    Compile a sequence of topologies into a single topology

    Args:
        trajdict: dictionary of MDTraj trajectories
        sequence: list of molecule names - keys in trajdict.

    Returns:
        MDTraj topology

    """
    
    result = mdt.Topology()
    topdict = {}
    for key in trajdict:
        topdict[key] = trajdict[key].topology

    for mol in sequence:
        for c in topdict[mol].chains:
            nc = result.add_chain()
            for r in c.residues:
                nr = result.add_residue(r.name, nc)
                for a in r.atoms:
                    result.add_atom(a.name, a.element, nr)

    for r in result.residues:
        r.resSeq = r.index + 1

    return result 


def traj_split(traj, molfile):
    """
    Split a trajectory into separate molecule trajectories.

    Each molecule specified in the molfile generates a separate
    dictionary in the returned list.

    Args:
        traj: MDTraj trajectory
        molfile: str, filename of a "molspec" file.

    Returns:
        list of dictionaries, each of which has the keys:
            'name' : molecule name, as in molfile
            'type' : molecule type, as in molfile
            'indices': residue indices (zero based) for the subset
            'trajectory' : MDTraj trajectory for the subset

    A "molspec" file defines how a whole trajectory should be split
    up into sections for resolution transformation. Each section has
    its own transformer object. An example  molspec file is as follows:

        # Any number of comment lines
        [polymers] 
        AQP 1 321
        [monomers]
        POPC POPC
        NA NA
        CL CL
        [solvents]
        SOL HOH
        SOL W

    Comment lines can occur anywhere in the file. the [polymers] section
    defines molecules by a range or residue indices (one based). So here
    for example, a molecule called "AQP" is defined by residues 1 to 321.
    If your system contains multiple protein (or nucleic acid) molecules,
    each will have its own entry. 
    The [monomers] section defines molecules
    by their residue name. So here, molecule "POPC" refers to all POPC 
    residues in the system, NA to all residues named NA, etc. There is no
    requirement that molecule name and residue name match, but it may be
    convenient if they do. 
    The [solvents] section defines those parts of
    the system that should be treated as solvent, for which the resolution
    transformatuon method is different (and more approximate). Note here
    that the same molecule name "SOL" maps to two different residue names.
    This is because very commonly solvent residues have different residue
    names at different resolutions.
    """
    trajs = []
    molecule_types = {'polymers': False, 'monomers': False, 'solvents': False}
    current_type = None
    with open(molfile) as f:
        for line in f.readlines():
            if line[0] == '#':
                pass
            elif line[0] == '[':
                for key in molecule_types:
                    molecule_types[key] = False
                    if key in line:
                        molecule_types[key] = True
                        current_type = key
            else:
                if current_type is None:
                    raise ValueError('Error parsing molspec file')
                w = line.split()
                if len(w) == 2:
                    molname = w[0]
                    resname = w[1]
                    selection = 'resname {}'.format(resname)
                    atom_indices = traj.topology.select(selection)
                    res_indices = [r.index for r in traj.topology.subset(atom_indices).residues]
                    if len(atom_indices) > 0:
                        td = {}
                        td['name'] = molname
                        td['type'] = current_type
                        td['indices'] = res_indices
                        td['trajectory'] = traj.atom_slice(atom_indices)
                        trajs.append(td)
                elif len(w) == 3:
                    molname = w[0]
                    rfirst = int(w[1]) - 1
                    rlast = int(w[2]) - 1
                    selection = 'resid {} to {}'.format(rfirst, rlast)
                    atom_indices = traj.topology.select(selection)
                    res_indices = [r.index for r in traj.topology.subset(atom_indices).residues]
                    if len(atom_indices) > 0:
                        td = {}
                        td['name'] = molname
                        td['type'] = current_type
                        td['indices'] = res_indices
                        td['trajectory'] = traj.atom_slice(atom_indices)
                        trajs.append(td)
    return trajs

def traj_flatten(traj):
    """
    Flatten a trajectory that contains multiple copies of the same residue

    Args:
        traj: MDTraj trajectory with n_residues copies of the same residue
              in its n_frames snapshots.

    Returns:
        MDTraj trajectory with 1 residue per n_frames * n_residues snapshots.
    """
    rlist = [r.name for r in traj.topology.residues]
    if len(rlist) == 1:
        return traj

    homogeneous = True
    rref = rlist[0]
    for r in rlist[1:]:
        if r != rref:
            homogeneous = False
    if not homogeneous:
        raise TypeError('Error - not all residues are the same')

    n_atoms = traj.n_atoms // len(rlist)
    top = traj.topology.subset(range(n_atoms))
    xyz = traj.xyz.reshape((-1, n_atoms, 3))
    return mdt.Trajectory(xyz, top)

def traj_ravel(traj, n_residues):
    """
    Reverse of traj_flatten

    Args:
        traj: MDTraj trajectory of n_frames, with 1 residue per snapshot.
        n_residues: int, number of residues per snaphot in the output.

    Returns:
        MDTraj trajectory of length n_frames / n_residues, with n_residues
        per snapshot.
    """
    if traj.n_frames % n_residues != 0:
        raise ValueError('Error - cannot reshape the trajectory')

    n_frames = traj.n_frames // n_residues
    res = traj.topology.residue(0)
    top = mdt.Topology()
    nc = top.add_chain()
    for i in range(n_residues):
        nr = top.add_residue(res.name, nc)
        for a in res.atoms:
            top.add_atom(a.name, a.element, nr)

    return mdt.Trajectory(traj.xyz.reshape((n_frames, -1, 3)), top)

def traj_merge(trajfiles, indices):
    """
    Merge the contents of multiple trajectories

    Args:
        trajfiles: list of MDTraj trajectories
        indices: list of residue indices for each trajectory

    Returns:
        MDTraj trajectory

    The indices arrays index the complete, final trajectory. It would be
    nice to assume that each set of indices would be a contiguous list,
    i.e. that all the residues in trajfiles[0] will be contiguous in the
    final trajectory, but we do not assume this. Hence the rather more
    complex code below, which looks for "subtrajectories" within each.
    This is belt and braces stuff, probebly very rarely will this actually
    happen, but just in case...
    """
    subtrajs = []
    subinds = []
    for i in range(len(trajfiles)):
        for j, r in enumerate(trajfiles[i].topology.residues):
            r.index = j
        jstart = 0
        jlast = 0
        for j in range(1, len(indices[i])):
            if j != jlast + 1:
                subinds.append(indices[i][jstart:j])
                sel = trajfiles[i].topology.select('resid {} to {}'.format(jstart, jlast))
                subtrajs.append(trajfiles[i].atom_slice(sel))
                jstart = j
            jlast = j
        subinds.append(indices[i][jstart:jlast+1])
        sel = trajfiles[i].topology.select('resid {} to {}'.format(jstart, jlast))
        subtrajs.append(trajfiles[i].atom_slice(sel))
              
    top = mdt.Topology()
    nc = top.add_chain()
    for i in np.argsort([ind[0] for ind in subinds]):
        tp = subtrajs[i].topology
        for r in tp.residues:
            nr = top.add_residue(r.name, nc)
            for a in r.atoms:
                top.add_atom(a.name, a.element, nr)
    n_tot = top.n_atoms
    for r in top.residues:
        r.resSeq = r.index + 1
    n_frames = len(trajfiles[0])
    for i in range(len(subinds)):
        ir1 = subinds[i][0]
        ir2 = subinds[i][-1]
        subinds[i] = top.select('resid {} to {}'.format(ir1, ir2))
    xyz = np.zeros((n_frames, n_tot, 3))
    for i in range(len(subtrajs)):
        xyz[:, subinds[i]] = subtrajs[i].xyz
    t = mdt.Trajectory(xyz, top)
    return t
