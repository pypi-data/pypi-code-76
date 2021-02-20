"""Physics numerical constants as float64."""
import numpy_ipps.constants.maths.float64
import numpy_ipps.single.float64
import numpy_ipps.tools


c = numpy_ipps.single.float64.new(299792458)
#: Speed of light in vacuum in SI as float64,
#: use ``c`` if you need a ``ndarray``
c_C = c[0]


h = numpy_ipps.single.float64.new(6.62607015e-34)
#: Planck constant in SI as float64,
#: use ``h`` if you need a ``ndarray``
h_C = h[0]


e = numpy_ipps.single.float64.new(1.602176634e-19)
#: Elementary charge in SI as float64,
#: use ``h`` if you need a ``ndarray``
e_C = e[0]


kB = numpy_ipps.single.float64.new(1.380649e-23)
#: Boltzmann constant in SI as float64,
#: use ``kB`` if you need a ``ndarray``
kB_C = kB[0]


NA = numpy_ipps.single.float64.new(6.02214076e23)
#: Avogadro constant in SI as float64,
#: use ``NA`` if you need a ``ndarray``
NA_C = NA[0]


_alphaInv = numpy_ipps.single.float64.new(137.0359992)

G = numpy_ipps.single.float64.new(6.674e-11)
#: Newtonian constant of gravitation in SI as float64,
#: use ``G`` if you need a ``ndarray``
G_C = G[0]


g0 = numpy_ipps.single.float64.new(9.80665)
#: Newtonian constant of gravitation in SI as float64,
#: use ``g0`` if you need a ``ndarray``
g0_C = g0[0]


md = numpy_ipps.single.float64.new(3.34358377e-27)
#: Deuteron mass in SI as float64,
#: use ``md`` if you need a ``ndarray``
md_C = md[0]


me = numpy_ipps.single.float64.new(9.1093837e-31)
#: Electron mass in SI as float64,
#: use ``me`` if you need a ``ndarray``
me_C = me[0]


mh = numpy_ipps.single.float64.new(5.00641277e-27)
#: Helion mass in SI as float64,
#: use ``mh`` if you need a ``ndarray``
mh_C = mh[0]


mmu = numpy_ipps.single.float64.new(1.8835316e-28)
#: Muon mass in SI as float64,
#: use ``mmu`` if you need a ``ndarray``
mmu_C = mmu[0]


mn = numpy_ipps.single.float64.new(1.674927498e-27)
#: Neutron mass in SI as float64,
#: use ``mn`` if you need a ``ndarray``
mn_C = mn[0]


mp = numpy_ipps.single.float64.new(1.672621923e-27)
#: Proton mass in SI as float64,
#: use ``mp`` if you need a ``ndarray``
mp_C = mp[0]


mt = numpy_ipps.single.float64.new(5.00735674e-27)
#: Triton mass in SI as float64,
#: use ``mt`` if you need a ``ndarray``
mt_C = mt[0]


gd = numpy_ipps.single.float64.new(0.85743823)
#: Deuteron g-factor as float64,
#: use ``gd`` if you need a ``ndarray``
gd_C = gd[0]


ge = numpy_ipps.single.float64.new(-2.002319304362)
#: Electron g-factor as float64,
#: use ``ge`` if you need a ``ndarray``
ge_C = ge[0]


gh = numpy_ipps.single.float64.new(-4.2552506)
#: Helion g-factor as float64,
#: use ``gh`` if you need a ``ndarray``
gh_C = gh[0]


gmu = numpy_ipps.single.float64.new(-2.00233184)
#: Muon g-factor as float64,
#: use ``gmu`` if you need a ``ndarray``
gmu_C = gmu[0]


gn = numpy_ipps.single.float64.new(-3.826085)
#: Neutron g-factor as float64,
#: use ``gn`` if you need a ``ndarray``
gn_C = gn[0]


gp = numpy_ipps.single.float64.new(-5.58569468)
#: Proton g-factor as float64,
#: use ``gp`` if you need a ``ndarray``
gp_C = gp[0]


gt = numpy_ipps.single.float64.new(5.9579249)
#: Triton g-factor as float64,
#: use ``gt`` if you need a ``ndarray``
gt_C = gt[0]


alpha = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.inv(_alphaInv, alpha)
#: Fine-structure constant as float64,
#: use ``alpha`` if you need a ``ndarray``
alpha_c = alpha[0]


R = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.mul(kB, NA, R)
#: Molar gas constant in SI as float64,
#: use ``R`` if you need a ``ndarray``
R_C = R[0]


F = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.mul(e, NA, F)
#: Faraday constant in SI as float64,
#: use ``F`` if you need a ``ndarray``
F_C = F[0]


hBar = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(
    h, numpy_ipps.constants.maths.float64.twoPi, hBar
)
#: Reduced Planck constant in SI as float64,
#: use ``hBar`` if you need a ``ndarray``
hBar_C = hBar[0]


_two = numpy_ipps.single.float64.new(2)

Q2e = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.mul(_two, e, Q2e)
#: Cooper pair charge in SI as float64,
#: use ``Q2e`` if you need a ``ndarray``
Q2e_C = Q2e[0]


KJ = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(Q2e, h, KJ)
#: Josephson constant in SI as float64,
#: use ``KJ`` if you need a ``ndarray``
KJ_C = KJ[0]


Phi0 = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(h, Q2e, Phi0)
#: Magnetic flux quantum in SI as float64,
#: use ``Phi0`` if you need a ``ndarray``
Phi0_C = Phi0[0]


Phi0Bar = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(hBar, Q2e, Phi0Bar)
#: Reduced magnetic flux quantum in SI as float64,
#: use ``Phi0Bar`` if you need a ``ndarray``
Phi0Bar_C = Phi0Bar[0]


G0 = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.mul(KJ, e, G0)
#: Conductance quantum in SI as float64,
#: use ``G0`` if you need a ``ndarray``
G0_C = G0[0]


RK = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(_two, G0, RK)
#: Von Klitzing constant in SI as float64,
#: use ``RK`` if you need a ``ndarray``
RK_C = RK[0]


_twoAlpha = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(_two, _alphaInv, _twoAlpha)

Z0 = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.mul(_twoAlpha, RK, Z0)
#: Characteristic impedance of vacuum in SI as float64,
#: use ``Z0`` if you need a ``ndarray``
Z0_C = Z0[0]


mu0 = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(Z0, c, mu0)
#: Vacuum magnetic permeability in SI as float64,
#: use ``mu0`` if you need a ``ndarray``
mu0_C = mu0[0]


RK2e = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(RK, numpy_ipps.single.float64.new(4), RK2e)
#: Superconducting quantum of resistance in SI as float64,
#: use ``RK2e`` if you need a ``ndarray``
RK2e_C = RK2e[0]


_cInv = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.inv(c, _cInv)

eps0 = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(_cInv, Z0, eps0)
#: Vacuum electric permitivity in SI as float64,
#: use ``eps0`` if you need a ``ndarray``
eps0_C = eps0[0]


_eps0Inv = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(Z0, _cInv, _eps0Inv)

kC = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(
    _eps0Inv, numpy_ipps.constants.maths.float64.fourPi, kC
)
#: Coulomb constant in SI as float64,
#: use ``kC`` if you need a ``ndarray``
kC_C = kC[0]


alphaPauw = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.div(
    numpy_ipps.constants.maths.float64.pi,
    numpy_ipps.constants.maths.float64.ln2,
    alphaPauw,
)
#: Van der Pauw constant in SI as float64,
#: use ``alphaPauw`` if you need a ``ndarray``
alphaPauw_C = alphaPauw[0]


thetam = numpy_ipps.single.float64.new()
numpy_ipps.single.float64.sqrt(_two, thetam)
numpy_ipps.single.float64.atan(thetam, thetam)
#: Magic angle in radian as float64,
#: use ``thetam`` if you need a ``ndarray``
thetam_C = thetam[0]


Laplace = numpy_ipps.single.float64.new(0.662743419349181)
#: Laplace limit as float64,
#: use ``Laplace`` if you need a ``ndarray``
Laplace_C = Laplace[0]


del _alphaInv
del _cInv
del _eps0Inv
del _two
del _twoAlpha
