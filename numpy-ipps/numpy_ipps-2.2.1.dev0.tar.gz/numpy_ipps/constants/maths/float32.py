"""Maths numerical constants as float32."""
import numpy as _numpy

import numpy_ipps.policies
import numpy_ipps.tools
import numpy_ipps.utils

from ._detail import generators as _generators


pi = numpy_ipps.tools.bbp(
    numpy_ipps.tools.sumN(
        numpy_ipps.utils.ndarray(
            _numpy.array([[4, 0], [1, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-2, 0], [4, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-1, 0], [5, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-1, 0], [6, 8]], dtype=_numpy.float64)
        ),
    ),
    16,
    _numpy.float32,
)
#: ``pi`` as float32,
#: use ``pi`` if you need a ``ndarray``
pi_C = pi[0]


twoPi = numpy_ipps.tools.bbp(
    numpy_ipps.tools.sumN(
        numpy_ipps.utils.ndarray(
            _numpy.array([[8, 0], [1, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-4, 0], [4, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-2, 0], [5, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-2, 0], [6, 8]], dtype=_numpy.float64)
        ),
    ),
    16,
    _numpy.float32,
)
#: ``2 pi`` as float32,
#: use ``twoPi`` if you need a ``ndarray``
twoPi_C = twoPi[0]


fourPi = numpy_ipps.tools.bbp(
    numpy_ipps.tools.sumN(
        numpy_ipps.utils.ndarray(
            _numpy.array([[16, 0], [1, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-8, 0], [4, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-4, 0], [5, 8]], dtype=_numpy.float64)
        ),
        numpy_ipps.utils.ndarray(
            _numpy.array([[-4, 0], [6, 8]], dtype=_numpy.float64)
        ),
    ),
    16,
    _numpy.float32,
)
#: ``4 pi`` as float32,
#: use ``fourPi`` if you need a ``ndarray``
fourPi_C = fourPi[0]


ln2 = numpy_ipps.tools.bbp(
    numpy_ipps.utils.ndarray(
        _numpy.array([[1, 0], [2, 2]], dtype=_numpy.float64)
    ),
    2,
    _numpy.float32,
)
#: Natural logarithm ``ln(2)`` as float32,
#: use ``ln2`` if you need a ``ndarray``
ln2_C = ln2[0]


ln3 = numpy_ipps.tools.bbp(
    numpy_ipps.utils.ndarray(
        _numpy.array([[1, 0], [1, 2]], dtype=_numpy.float64)
    ),
    4,
    _numpy.float32,
)
#: Natural logarithm ``ln(3)`` as float32,
#: use ``ln3`` if you need a ``ndarray``
ln3_C = ln3[0]


e = numpy_ipps.tools.series(_generators.e(_numpy.float32), _numpy.float32)
#: Euler's number as float32,
#: use ``e`` if you need a ``ndarray``
e_C = e[0]


I1 = numpy_ipps.tools.series(_generators.I1(_numpy.float32), _numpy.float32)
#: Sophomore's dream 1 as float32,
#: use ``I1`` if you need a ``ndarray``
I1_C = I1[0]


I2 = numpy_ipps.tools.series(_generators.I2(_numpy.float32), _numpy.float32)
#: Sophomore's dream 2 as float32,
#: use ``I2`` if you need a ``ndarray``
I2_C = I2[0]


EB = numpy_ipps.tools.series(_generators.EB(_numpy.float32), _numpy.float32)
#: Erdos-Borwein constant as float32,
#: use ``EB`` if you need a ``ndarray``
EB_C = EB[0]


# G = numpy_ipps.tools.series(_generators.G(_numpy.float32), _numpy.float32)
G = numpy_ipps.utils.ndarray(
    _numpy.array([0.915965594177219], dtype=_numpy.float32)
)
#: Catalan's constant as float32,
#: use ``G`` if you need a ``ndarray``
G_C = G[0]


# zeta3 = numpy_ipps.tools.series(
#     _generators.zeta3(_numpy.float32), _numpy.float32
# )
zeta3 = numpy_ipps.utils.ndarray(
    _numpy.array([1.2020569031595942], dtype=_numpy.float32)
)
#: Apery's constant as float32,
#: use ``zeta3`` if you need a ``ndarray``
zeta3_C = zeta3[0]


ePi = numpy_ipps.tools.series(
    _generators.ePi(pi, _numpy.float32), _numpy.float32
)
#: Gelfond's constant as float32,
#: use ``ePi`` if you need a ``ndarray``
ePi_C = ePi[0]


df = numpy_ipps.utils.ndarray(_numpy.empty(1, dtype=_numpy.float32))
numpy_ipps.Div(size=1, dtype=_numpy.float32)(ln2, ln3, df)
#: Fractal dimension of the Cantor set as float32,
#: use ``df`` if you need a ``ndarray``
df_C = df[0]


phi = numpy_ipps.utils.ndarray(
    _numpy.array([1.61803398874989], dtype=_numpy.float32)
)
#: Golden ration as float32,
#: use ``phi`` if you need a ``ndarray``
phi_C = phi[0]


gamma = numpy_ipps.utils.ndarray(
    _numpy.array([0.577215664901532], dtype=_numpy.float32)
)
#: Euler–Mascheroni constant as float32,
#: use ``gamma`` if you need a ``ndarray``
gamma_C = gamma[0]


d = numpy_ipps.utils.ndarray(
    _numpy.array([0.739085133215160], dtype=_numpy.float32)
)
#: Dottie number as float32,
#: use ``d`` if you need a ``ndarray``
d_C = d[0]


_sqrt = numpy_ipps.Sqrt(
    size=1,
    dtype=_numpy.float32,
    accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
)


sqrt2 = numpy_ipps.utils.ndarray(_numpy.array([2], dtype=_numpy.float32))
_sqrt(sqrt2, sqrt2)
#: Square root of 2 as float32,
#: use ``sqrt2`` if you need a ``ndarray``
sqrt2_C = sqrt2[0]


sqrt3 = numpy_ipps.utils.ndarray(_numpy.array([3], dtype=_numpy.float32))
_sqrt(sqrt3, sqrt3)
#: Square root of 3 as float32,
#: use ``sqrt3`` if you need a ``ndarray``
sqrt3_C = sqrt3[0]


del _sqrt
