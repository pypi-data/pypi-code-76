from context import compflow as cf
from context import TEST_DIR
import numpy as np

# Ratio of specific heats
ga = 1.4

# Quantity names
var_sub = ['Ma', 'To_T', 'Po_P', 'rhoo_rho', 'V_cpTo', 'mcpTo_APo',
           'mcpTo_AP', 'F_mcpTo', '4cfL_D', 'rhoVsq_2Po']
var_sup = var_sub + ['Mash', 'Posh_Po', 'Psh_P',
                     'Posh_P', 'Tsh_T', 'nu', 'Ma2']

# Read verification data
csv_sub = TEST_DIR + '/cued_data_book_subsonic.csv'
dat_sub = {var_sub[i]: np.loadtxt(csv_sub).reshape((-1, 10))[:, i]
           for i in range(len(var_sub))}

csv_sup = TEST_DIR + '/cued_data_book_supersonic.csv'
dat_sup = {var_sup[i]: np.loadtxt(csv_sup).reshape((-1, 17))[3:, i]
           for i in range(len(var_sup))}

# Take reciprocals of verification data
for vi in ['To_T', 'Po_P', 'rhoo_rho']:
    dat_sub[vi] = 1. / dat_sub[vi]
    dat_sup[vi] = 1. / dat_sup[vi]

# List variables which the module implements
var_test_sub = ['To_T', 'Po_P', 'rhoo_rho', 'V_cpTo', 'mcpTo_APo', 'mcpTo_AP']
var_test_sup = ['To_T', 'Po_P', 'rhoo_rho', 'V_cpTo', 'mcpTo_APo',
                'mcpTo_AP', 'Mash', 'Posh_Po']

# Number of times to repeat the number crunching
Nrep = 100

#
# Begin test functions

def test_Ma_0():
    """Check expected values for Ma = 0."""
    val0 = np.array([1., 1., 1., 0., 0., 0., np.nan, np.nan])
    Y0 = {var_test_sup[i]: val0[i] for i in range(len(var_test_sup))}
    for v in var_test_sup:
        print(v, Y0[v], cf.from_Ma( v, np.atleast_1d(0.), ga))
        assert np.isclose( cf.from_Ma( v, np.atleast_1d(0.), ga), Y0[v],
                           atol=1e-7, equal_nan=True)
        if np.isfinite(Y0[v]):
            assert np.isclose( cf.to_Ma( v, np.atleast_1d(Y0[v]), ga), 0.0,
                                atol=1e-7, equal_nan=True)

def test_Ma_inf():
    """Check expected values for Ma = i."""
    val_inf = np.array([np.inf, np.inf, np.inf, np.sqrt(2.), 0.,
                        np.inf, np.sqrt((ga - 1.)/ 2. / ga), 0.])
    Y0 = {var_test_sup[i]: val_inf[i] for i in range(len(var_test_sup))}
    for v in var_test_sup:
        print(v)
        assert np.isclose( cf.from_Ma( v, np.atleast_1d(np.inf), ga), Y0[v], atol=1e-7)

def test_Ma_1():
    """Check inversion for values near Ma = 1."""
    dMa = 0.0001
    Ma_fw = np.array([-dMa, 0., dMa]) + 1.
    for v in var_test_sup:
        Y_fw = cf.from_Ma( v, Ma_fw, ga)
        Ma_bk = cf.to_Ma( v, Y_fw, ga)
        if v in ['mcpTo_APo','A_Acrit']:
            Ma_bk[-1] = cf.to_Ma( v, Y_fw[-1], ga, True)
        err = Ma_fw-Ma_bk
        print(v, err)
        assert np.all(np.abs(err[~np.isnan(Ma_bk)])<1e-5)

def test_explicit_sub():
    """Compare quantity values to CUED Data Book, subsonic."""
    for v in var_test_sub:
        for _ in range(Nrep):
            Ysub = cf.from_Ma(v, dat_sub['Ma'], ga)
        err_sub = np.abs(Ysub / dat_sub[v] - 1.)
        imax = np.argmax(err_sub)
        assert err_sub[imax] < 0.005, \
            "Ma={0} => {1}={2} with error={3}".format(
                dat_sub['Ma'][imax], v, Ysub[imax], err_sub[imax])


def test_explicit_sup():
    """Compare quantity values to CUED Data Book, supersonic."""
    for v in var_test_sup:
        for _ in range(Nrep):
            Ysup = cf.from_Ma(v, dat_sup['Ma'], ga)
        err_sup = np.abs(Ysup / dat_sup[v] - 1.)
        imax = np.argmax(err_sup)
        assert err_sup[imax] < 0.005, \
            "Ma={0} => {1}={2} with error={3}".format(
                dat_sup['Ma'][imax], v, Ysup[imax], err_sup[imax])


def test_inverse_sub():
    """Compare Ma lookup values to CUED Data Book, subsonic."""
    for v in var_test_sub:
        for _ in range(Nrep):
            X = cf.to_Ma(v, dat_sub[v], ga)
        err_sub = np.abs(X - dat_sub['Ma'])
        imax = np.argmax(err_sub)
        assert err_sub[imax] <= 0.01, \
            "{0}={1} =>  Ma={2} with error={3}".format(
                v, dat_sub[v][imax], X[imax], err_sub[imax])


def test_inverse_sup():
    """Compare Ma lookup values to CUED Data Book, supersonic."""
    for v in var_test_sup:
        for _ in range(Nrep):
            X = cf.to_Ma(v, dat_sup[v], ga, supersonic=True)
        err_sup = np.abs(X - dat_sup['Ma'])
        imax = np.argmax(err_sup)
        assert err_sup[imax] <= 0.01, \
            "{0}={1} =>  Ma={2} with error={3}".format(
                v, dat_sup[v][imax], X[imax], err_sup[imax])


def test_derivative():
    """Check explicit derivative against a numerical approximation."""
    for v in var_test_sup:
        Ma = np.linspace(0., 3.)

        # Explicit
        dYdMa = cf.derivative_from_Ma(v, Ma, ga)

        # Numerical approximation
        Y = cf.from_Ma(v, Ma, ga)
        dYdMa_numerical = np.gradient(Y, Ma)

        # Check discrepancy
        err = dYdMa / dYdMa_numerical - 1.
        print(v)
        assert np.max(err[np.isfinite(err)]) < 0.05
