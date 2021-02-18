from __future__ import print_function
import numpy as np
from math import sqrt
from scipy import linalg as la


def tri2full(H_nn, UL='L'):
    """Fill in values of hermitian matrix.

    Fill values in lower or upper triangle of H_nn based on the opposite
    triangle, such that the resulting matrix is symmetric/hermitian.

    UL='U' will copy (conjugated) values from upper triangle into the
    lower triangle.

    UL='L' will copy (conjugated) values from lower triangle into the
    upper triangle.
    """
    N, tmp = H_nn.shape
    assert N == tmp, 'Matrix must be square'
    # assert np.isreal(H_nn.diagonal()).all(), 'Diagonal should be real'
    if UL != 'L':
        H_nn = H_nn.T

    for n in range(N - 1):
        H_nn[n, n + 1:] = H_nn[n + 1:, n].conj()


def dagger(matrix):
    return np.conj(matrix.T)


def rotate_matrix(h, u):
    return np.dot(u.T.conj(), np.dot(h, u))


def get_subspace(matrix, index):
    """Get the subspace spanned by the basis function listed in index"""
    assert matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]
    return matrix.take(index, 0).take(index, 1)

permute_matrix = get_subspace


def normalize(matrix, S=None):
    """Normalize column vectors.

    ::

      <matrix[:,i]| S |matrix[:,i]> = 1

    """
    for col in matrix.T:
        if S is None:
            col /= np.linalg.norm(col)
        else:
            col /= np.sqrt(np.dot(col.conj(), np.dot(S, col)))


def get_orthonormal_subspace(h_ii, s_ii, index_j):
    h_sub_jj  = get_subspace(h_ii, index_j)
    s_sub_jj  = get_subspace(s_ii, index_j)
    e_j, v_jj = np.linalg.eig(np.linalg.solve(s_sub_jj, h_sub_jj))
    normalize(v_jj, s_sub_jj)  # normalize: <v_j|s|v_j> = 1
    permute_list = np.argsort(e_j.real)
    e_j = np.take(e_j, permute_list)
    v_jj = np.take(v_jj, permute_list, axis=1)
    return v_jj, e_j

def subdiagonalize(h_ii, s_ii, index_j):
    nb = h_ii.shape[0]
    nb_sub = len(index_j)
    v_jj, e_j = get_orthonormal_subspace(h_ii, s_ii, index_j)
    # Setup transformation matrix
    c_ii = np.identity(nb, h_ii.dtype)
    for i in range(nb_sub):
        for j in range(nb_sub):
            c_ii[index_j[i], index_j[j]] = v_jj[i, j]

    h1_ii = rotate_matrix(h_ii, c_ii)
    s1_ii = rotate_matrix(s_ii, c_ii)

    return h1_ii, s1_ii, c_ii, e_j

def cutcoupling(h, s, index_n):
    for i in index_n:
        s[:, i] = 0.0
        s[i, :] = 0.0
        s[i, i] = 1.0
        Ei = h[i, i]
        h[:, i] = 0.0
        h[i, :] = 0.0
        h[i, i] = Ei


def fermidistribution(energy, kt):
   # fermi level is fixed to zero
   # energy can be a single number or a list
   assert kt >= 0., 'Negative temperature encountered!'

   if kt==0:
       if isinstance(energy, float):
           return int(energy / 2. <= 0)
       else:
           return (energy / 2. <= 0).astype(int)
   else:
       return 1. / (1. + np.exp(energy / kt))


def fliplr(a):
    length = len(a)
    b = [0] * length
    for i in range(length):
        b[i] = a[length - i - 1]
    return b


def plot_path(energy):
    import pylab
    pylab.plot(np.real(energy), np.imag(energy), 'b--o')
    pylab.show()


def function_integral(function, calcutype):
    # return the integral of the 'function' on 'intrange'
    # the function can be a value or a matrix, arg1,arg2 are the possible
    # parameters of the function

    intctrl = function.intctrl
    if calcutype == 'eqInt':
        intrange = intctrl.eqintpath
        tol = intctrl.eqinttol
        if hasattr(function.intctrl, 'eqpath_radius'):
            radius = function.intctrl.eqpath_radius
        else:
            radius = -1
        if hasattr(function.intctrl, 'eqpath_origin'):
            origin = function.intctrl.eqpath_origin
        else:
            origin = 1000
    elif calcutype == 'neInt':
        intrange = intctrl.neintpath
        tol = intctrl.neinttol
        radius = -1
        origin = 1000
    elif calcutype == 'locInt':
        intrange = intctrl.locintpath
        tol = intctrl.locinttol
        if hasattr(function.intctrl, 'locpath_radius'):
            radius = function.intctrl.locpath_radius
        else:
            radius = -1
        if hasattr(function.intctrl, 'locpath_origin'):
            origin = function.intctrl.locpath_origin
        else:
            origin = 1000
    trace = 0
    a = 0.
    b = 1.

    # Initialize with 13 function evaluations.
    c = (a + b) / 2
    h = (b - a) / 2
    realmin = 2e-17

    s = [.942882415695480, sqrt(2.0 / 3),
         .641853342345781, 1 / sqrt(5.0), .236383199662150]
    s1 = [0] * len(s)
    s2 = [0] * len(s)
    for i in range(len(s)):
        s1[i] = c - s[i] * h
        s2[i] = c + fliplr(s)[i] * h
    x0 = [a] + s1 + [c] + s2 + [b]

    s0 = [.0158271919734802, .094273840218850, .155071987336585,
          .188821573960182, .199773405226859, .224926465333340]
    w0 = s0 + [.242611071901408] + fliplr(s0)
    w1 = [1, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 1]
    w2 = [77, 0, 432, 0, 625, 0, 672, 0, 625, 0, 432, 0, 77]
    for i in range(len(w1)):
        w1[i] = w1[i] / 6.0
        w2[i] = w2[i] / 1470.0

    dZ = [intrange[:len(intrange) - 1], intrange[1:]]
    hmin = [0] * len(dZ[1])

    path_type = []
    for i in range(len(intrange) - 1):
        rs = np.abs(dZ[0][i] - origin)
        re = np.abs(dZ[1][i] - origin)
        if abs(rs - radius) < 1.0e-8 and abs(re - radius) < 1.0e-8:
            path_type.append('half_circle')
        else:
            path_type.append('line')

    for i in range(len(dZ[1])):
        if path_type[i] == 'half_circle':
            dZ[0][i] = 0
            dZ[1][i] = np.pi
    for i in range(len(dZ[1])):
        dZ[1][i] = dZ[1][i] - dZ[0][i]
        hmin[i] = realmin / 1024 * abs(dZ[1][i])

    temp = np.array([[1] * 13, x0]).transpose()

    Zx = np.dot(temp, np.array(dZ))

    Zxx = []
    for i in range(len(intrange) - 1):
        for j in range(13):
            Zxx.append(Zx[j][i])

    ns = 0
    ne = 12
    if path_type[0] == 'line':
        yns = function.calgfunc(Zxx[ns], calcutype)
    elif path_type[0] == 'half_circle':
        energy = origin + radius * np.exp((np.pi - Zxx[ns + i]) * 1.j)
        yns = (-1.j * radius * np.exp(-1.j * Zxx[ns + i]) *
               function.calgfunc(energy, calcutype))
    fcnt = 0

    for n in range(len(intrange) - 1):
        # below evaluate the integral and adjust the tolerance
        Q1pQ0 = yns * (w1[0] - w0[0])
        Q2pQ0 = yns * (w2[0] - w0[0])
        fcnt = fcnt + 12
        for i in range(1, 12):
            if path_type[n] == 'line':
                yne = function.calgfunc(Zxx[ns + i], calcutype)
            elif path_type[n] == 'half_circle':
                energy = origin + radius * np.exp((np.pi - Zxx[ns + i]) * 1.j)
                yne = (-1.j * radius * np.exp(-1.j * Zxx[ns + i]) *
                       function.calgfunc(energy, calcutype))
            Q1pQ0 += yne * (w1[i] - w0[i])
            Q2pQ0 += yne * (w2[i] - w0[i])

        # Increase the tolerance if refinement appears to be effective
        r = np.abs(Q2pQ0) / (np.abs(Q1pQ0) + np.abs(realmin))
        dim = np.product(r.shape)
        r = np.sum(r) / dim
        if r > 0 and r < 1:
            thistol = tol / r
        else:
            thistol = tol
        if path_type[n] == 'line':
            yne = function.calgfunc(Zxx[ne], calcutype)
        elif path_type[n] == 'half_circle':
            energy = origin + radius * np.exp((np.pi - Zxx[ne]) * 1.j)
            yne = (-1.j * radius * np.exp(-1.j * Zxx[ne]) *
                   function.calgfunc(energy, calcutype))
        # Call the recursive core integrator

        Qk, xpk, wpk, fcnt, warn = quadlstep(function, Zxx[ns],
                                             Zxx[ne], yns, yne,
                                             thistol, trace, fcnt,
                                             hmin[n], calcutype, path_type[n],
                                             origin, radius)
        if n == 0:
            Q = np.copy(Qk)
            Xp = xpk[:]
            Wp = wpk[:]
        else:
            Q += Qk
            Xp = Xp[:-1] + xpk
            Wp = Wp[:-1] + [Wp[-1] + wpk[0]] + wpk[1:]
        if warn == 1:
            print('warning: Minimum step size reached,singularity possible')
        elif warn == 2:
            print('warning: Maximum function count excced; singularity likely')
        elif warn == 3:
            print('warning: Infinite or Not-a-Number function value '
                  'encountered')
        else:
            pass

        ns += 13
        ne += 13
        yns = np.copy(yne)

    return Q, Xp, Wp, fcnt


def quadlstep(f, Za, Zb, fa, fb, tol, trace, fcnt, hmin, calcutype,
              path_type, origin, radius):
    # Gaussian-Lobatto and Kronrod method
    # QUADLSTEP Recursive core routine for integral
    # input parameters:
    #      f      ----------   function, here we just use the module calgfunc
    #                          to return the value, if wanna use it for
    #                          another one, change it
    #     Za, Zb  ----------   the start and end point of the integral
    #     fa, fb  ----------   the function value on Za and Zb
    #     fcnt    ----------   the number of the function recalled till now
    # output parameters:
    #      Q      ----------   integral
    #     Xp      ----------   selected points
    #     Wp      ----------   weight
    #    fcnt     ----------   the number of the function recalled till now

    maxfcnt = 10000

    # Evaluate integrand five times in interior of subintrval [a,b]
    Zh = (Zb - Za) / 2.0
    if abs(Zh) < hmin:
        # Minimun step size reached; singularity possible
        Q = Zh * (fa + fb)
        if path_type == 'line':
            Xp = [Za, Zb]
        elif path_type == 'half_circle':
            Xp = [origin + radius * np.exp((np.pi - Za) * 1.j),
                  origin + radius * np.exp((np.pi - Zb) * 1.j)]
        Wp = [Zh, Zh]
        warn = 1
        return Q, Xp, Wp, fcnt, warn
    fcnt += 5
    if fcnt > maxfcnt:
        # Maximum function count exceed; singularity likely
        Q = Zh * (fa + fb)
        if path_type == 'line':
            Xp = [Za, Zb]
        elif path_type == 'half_circle':
            Xp = [origin + radius * np.exp((np.pi - Za) * 1.j),
                  origin + radius * np.exp((np.pi - Zb) * 1.j)]
        Wp = [Zh, Zh]
        warn = 2
        return Q, Xp, Wp, fcnt, warn
    x = [0.18350341907227, 0.55278640450004, 1.0,
         1.44721359549996, 1.81649658092773]
    Zx = [0] * len(x)
    y = [0] * len(x)
    for i in range(len(x)):
        x[i] *= 0.5
        Zx[i] = Za + (Zb - Za) * x[i]
        if path_type == 'line':
            y[i] = f.calgfunc(Zx[i], calcutype)
        elif path_type == 'half_circle':
            energy = origin + radius * np.exp((np.pi - Zx[i]) * 1.j)
            y[i] = f.calgfunc(energy, calcutype)
    # Four point Lobatto quadrature
    s1 = [1.0, 0.0, 5.0, 0.0, 5.0, 0.0, 1.0]
    s2 = [77.0, 432.0, 625.0, 672.0, 625.0, 432.0, 77.0]
    Wk = [0] * 7
    Wp = [0] * 7
    for i in range(7):
        Wk[i] = (Zh / 6.0) * s1[i]
        Wp[i] = (Zh / 1470.0) * s2[i]
    if path_type == 'line':
        Xp = [Za] + Zx + [Zb]
    elif path_type == 'half_circle':
        Xp = [Za] + Zx + [Zb]
        for i in range(7):
            factor = -1.j * radius * np.exp(1.j * (np.pi - Xp[i]))
            Wk[i] *= factor
            Wp[i] *= factor
            Xp[i] = origin + radius * np.exp((np.pi - Xp[i]) * 1.j)
    Qk = fa * Wk[0] + fb * Wk[6]
    Q = fa * Wp[0] + fb * Wp[6]
    for i in range(1, 6):
        Qk += y[i - 1] * Wk[i]
        Q += y[i - 1] * Wp[i]
    if np.isinf(np.max(np.abs(Q))):
        Q = Zh * (fa + fb)
        if path_type == 'line':
            Xp = [Za, Zb]
        elif path_type == 'half_circle':
            Xp = [origin + radius * np.exp((np.pi - Za) * 1.j),
                  origin + radius * np.exp((np.pi - Zb) * 1.j)]
        Wp = [Zh, Zh]
        warn = 3
        return Qk, Xp, Wp, fcnt, warn
    else:
        pass
    if trace:
        print(fcnt, np.real(Za), np.imag(Za), np.abs(Zh))
    # Check accurancy of integral over this subinterval
    XXk = [Xp[0], Xp[2], Xp[4], Xp[6]]
    WWk = [Wk[0], Wk[2], Wk[4], Wk[6]]
    YYk = [fa, y[1], y[3], fb]
    if np.max(np.abs(Qk - Q)) <= tol:
        warn = 0
        return Q, XXk, WWk, fcnt, warn
    # Subdivide into six subintevals
    else:
        Q, Xk, Wk, fcnt, warn = quadlstep(f, Za, Zx[1], fa, YYk[1],
                                          tol, trace, fcnt, hmin,
                                          calcutype, path_type,
                                          origin, radius)

        Qk, xkk, wkk, fcnt, warnk = quadlstep(
            f, Zx[1],
            Zx[3], YYk[1], YYk[2], tol, trace, fcnt, hmin,
            calcutype, path_type,
            origin, radius)
        Q += Qk
        Xk = Xk[:-1] + xkk
        Wk = Wk[:-1] + [Wk[-1] + wkk[0]] + wkk[1:]
        warn = max(warn, warnk)

        Qk, xkk, wkk, fcnt, warnk = quadlstep(f, Zx[3], Zb, YYk[2], fb,
                                              tol, trace, fcnt, hmin,
                                              calcutype, path_type,
                                              origin, radius)
        Q += Qk
        Xk = Xk[:-1] + xkk
        Wk = Wk[:-1] + [Wk[-1] + wkk[0]] + wkk[1:]
        warn = max(warn, warnk)
    return Q, Xk, Wk, fcnt, warn


def mytextread0(filename):
    num = 0
    df = open(filename)
    df.seek(0)
    for line in df:
        if num == 0:
            dim = line.strip().split(' ')
            row = int(dim[0])
            col = int(dim[1])
            mat = np.empty([row, col])
        else:
            data = line.strip().split(' ')
            if len(data) == 0 or len(data) == 1:
                break
            else:
                for i in range(len(data)):
                    mat[num - 1, i] = float(data[i])
        num += 1
    return mat


def mytextread1(filename):
    num = 0
    df = open(filename)
    df.seek(0)
    data = []
    for line in df:
        tmp = line.strip()
        if len(tmp) != 0:
            data.append(float(tmp))
        else:
            break
    dim = int(sqrt(len(data)))
    mat = np.empty([dim, dim])
    for i in range(dim):
        for j in range(dim):
            mat[i, j] = data[num]
            num += 1
    return mat


def mytextwrite1(filename, mat):
    df = open(filename, 'w')
    df.seek(0)
    dim = mat.shape[0]
    if dim != mat.shape[1]:
        print('matwirte, matrix is not square')
    for i in range(dim):
        for j in range(dim):
            df.write('%20.20e\n' % mat[i, j])
    df.close()

########## ADDED ##########

def order_diagonal(h_mm, s_mm):
    permute_list = np.argsort(h_mm.diagonal())
    h_mm = get_subspace(h_mm, permute_list)
    s_mm = get_subspace(s_mm, permute_list)
    U_mm = np.eye(len(h_mm)).take(permute_list, axis=1)
    return h_mm, s_mm, U_mm

def get_coupling_bfs(h_mm, index, natoms, cutoff=1e-2):
    '''This function returns the indices of the orbitas overlapping
    with the i-th orbital specified by index. The matrix h_mm has to
    be subdiagonalized and ordered.'''
    index_ao_coupling = [] # list of overlapping orbitals
    nbf = h_mm.shape[0] // natoms # ao per atom
    xrange = list(range(index*natoms, index*natoms+natoms))
    for ibf in range(nbf):
        yrange = range(ibf*natoms,ibf*natoms+natoms)
        coupling_mat = h_mm.take(xrange, 0).take(yrange, 1).flat
        if np.max(np.abs(coupling_mat))>cutoff: index_ao_coupling.append(ibf)
    return index_ao_coupling

def plot_ao_coupling(h_mm, natm, precision):
    '''Plot helper for subdiagonalized and ordered matrices.'''
    from matplotlib import pyplot as plt
    nbf = h_mm.shape[0] // natm
    plt.figure(figsize=(13,13))
    plt.spy(h_mm,precision=precision)
    plt.hlines(np.arange(0,natm*nbf,natm)-0.5,-0.5,natm*nbf-0.5,colors='r')
    plt.vlines(np.arange(0,natm*nbf,natm)-0.5,-0.5,natm*nbf-0.5,colors='r')
    plt.yticks(ticks=np.arange(0,natm*nbf,natm)-0.5,labels=[(i,e) for i,e in enumerate(np.round(h_mm.diagonal().real[::5],1))])
    plt.xticks(ticks=np.arange(0,natm*nbf,natm)-0.5,labels=np.arange(0,nbf))

def reshaffle_matrix(matrix, perm_list, start=False):
    """Put permute_list at end of the matrix"""
    nbf = len(matrix)
    if start:
        perm_list =  list(perm_list) + list(np.setdiff1d(range(nbf),perm_list))
    else:
        perm_list =  list(np.setdiff1d(range(nbf),perm_list)) + list(perm_list)
    return get_subspace(matrix, perm_list)

def zero_fermi(nzp):
    '''Compute poles (zp) and residues (Rp) of fermi function.'''
    N = nzp
    M = 2*N

    A = np.zeros((2*M,2*M))
    B = np.zeros((2*M,2*M))

    zp = np.zeros(2+M)
    Rp = np.zeros(2+M)

    for i in range(1,M+1):
        B[i,i] = (2*i-1)

    for i in range(1,M):
        A[i,i+1] = -0.5;
        A[i+1,i] = -0.5;

    a = np.zeros(M*M)
    b = np.zeros(M*M)

    for i in range(M):
        for j in range(M):
            a[j*M+i] = A[i+1,j+1]
            b[j*M+i] = B[i+1,j+1]

    a.shape = (M,M)
    b.shape = (M,M)

    eigvas, eigvecs = la.eigh(a,b)

    zp[:M] = eigvas

    for i in range(M,0,-1):
        zp[i] = zp[i-1]

    for i in range(1,M+1):
        zp[i] = 1.0/zp[i];

    a = eigvecs.T.flatten()

    for i in range(0,M):
        Rp[i+1] = -a[i*M]*a[i*M]*zp[i+1]*zp[i+1]*0.250;

    zp = -zp[1:N+1]
    Rp = Rp[1:N+1]

    return zp, Rp

def integrate_dos(G, mu=0, T=300, nzp=100, R=1e10):

    from scipy.constants import e, k

    zp, Rp = zero_fermi(nzp)
    N = nzp

    k_B = k / e # Boltzmann constant [eV/K] 8.6173303e-05
    beta = 1/(k_B*T)
    a_p = mu + 1j*zp/beta

    eta = G.eta
    G.eta = complex(0.)

    R = 1e10
    mu_0 = 1j*R*G.apply_retarded(1j*R, G.S).trace()

    mu_1 = complex(0)
    for i in range(N):
        mu_1 += G.apply_retarded(a_p[i], G.S).trace() * Rp[i]
    mu_1 *= -1j*4/beta

    rho = np.real(mu_0) + np.imag(mu_1)

    G.eta = eta

    return rho


def integrate_pdos(G, mu=0, T=300, nzp=100, R=1e10):

    from scipy.constants import e, k

    zp, Rp = zero_fermi(nzp)
    N = nzp

    k_B = k / e # Boltzmann constant [eV/K] 8.6173303e-05
    beta = 1/(k_B*T)
    a_p = mu + 1j*zp/beta

    eta = G.eta
    G.eta = complex(0.)

    R = 1e10
    mu_0 = 1j*R*G.apply_retarded(1j*R, G.S).diagonal()

    mu_1 = np.zeros(len(G.H), complex)
    for i in range(N):
        mu_1 += G.apply_retarded(a_p[i], G.S).diagonal() * Rp[i]
    mu_1 *= -1j*4/beta

    rho = np.real(mu_0) + np.imag(mu_1)

    G.eta = eta

    return rho
