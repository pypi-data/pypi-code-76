from math import atan, pi, sqrt


class EleComplex:
    """Improvement of the builtin complex type.

    Additional attributes:
        phase: Returns the complex number's phase in degrees.
        module: Returns the complex number's unitless amplitude.
    """

    def __init__(self, val_0, val_1=0):
        from energy_tools.phasor import Phasor

        if val_0.__class__ in (complex, EleComplex, Phasor):
            self.real = val_0.real
            self.imag = val_0.imag

        elif val_0.__class__ in (int, float):
            self.real = val_0
            if val_1.__class__ in (int, float):
                self.imag = val_1
            else:
                return NotImplemented

        else:
            return NotImplemented

    @property
    def phase(self):
        """Returns the complex number's phase in degrees.
        """
        if self.real > 0:
            if self.imag >= 0:
                return abs(180 * atan(self.imag / self.real) / pi)
            else:
                return 360 - abs(180 * atan(self.imag / self.real) / pi)

        elif self.real < 0:
            if self.imag >= 0:
                return 180 - abs(180 * atan(self.imag / self.real) / pi)
            else:
                return 180 + abs(180 * atan(self.imag / self.real) / pi)

        else:
            if self.imag == 0:
                return 0.0
            elif self.imag > 0:
                return 90.0
            else:
                return 270.0

    @property
    def module(self):
        return self.__abs__()

    @property
    def pf(self):
        if self.real * self.imag >= 0:
            return abs(self.real) / self.module
        else:
            return -abs(self.real) / self.module

    def __add__(self, other):
        from energy_tools.phasor import Phasor

        if other.__class__ in (int, float, Phasor):
            return self.__add__(EleComplex(other))

        elif other.__class__ == EleComplex:
            real = self.real + other.real
            imag = self.imag + other.imag
            return EleComplex(real, imag)

        else:
            return NotImplemented

    def __round__(self, ndigits=None):
        return EleComplex(round(self.real, ndigits) + round(self.imag, ndigits) * 1j)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        from energy_tools.phasor import Phasor

        if other.__class__ in (int, float):
            return EleComplex(self.real * other, self.imag * other)

        elif other.__class__ in (complex, EleComplex):
            x = self.real
            y = self.imag
            u = other.real
            v = other.imag
            return EleComplex(x * u - y * v + (x * v + y * u) * 1j)

        else:
            return NotImplemented

    def __truediv__(self, other):
        from energy_tools.phasor import Phasor

        if other.__class__ in (int, float):
            return EleComplex(self.real / other, self.imag / other)

        elif other.__class__ in (complex, EleComplex):
            x = self.real
            y = self.imag
            u = other.real
            v = other.imag
            return EleComplex(
                (x * u + y * v + (-x * v + y * u) * 1j) / (u ** 2 + v ** 2)
            )

        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        from energy_tools.phasor import Phasor

        if other.__class__ in (int, float):
            x = self.real
            y = self.imag
            u = other.real
            v = other.imag
            return other * EleComplex(
                x / (x ** 2 + y ** 2) - y / ((x ** 2 + y ** 2) * 1j)
            )

        elif other.__class__ in (complex, EleComplex):
            x = other.real
            y = other.imag
            u = self.real
            v = self.imag
            return EleComplex(
                (x * u + y * v + (-x * v + y * u) * 1j) / (u ** 2 + v ** 2)
            )

        else:
            return NotImplemented

    def __pow__(self, other, modulo=None):
        return NotImplemented

    def __abs__(self):
        return sqrt(self.real ** 2 + self.imag ** 2)

    def __neg__(self):
        return EleComplex(-self.real, -self.imag)

    def __pos__(self):
        return self

    def __invert__(self):
        return self.__neg__()

    def __int__(self):
        return int(self.module)

    def __float__(self):
        return float(self.module)

    def __complex__(self):
        return self

    def __round__(self, n=0):
        return EleComplex(round(self.real, n), round(self.imag, n))

    def __repr__(self):
        s = "("
        s += str(round(self.real, 3))
        if self.imag >= 0:
            s += "+"
        s += str(round(self.imag, 3)) + "j)"
        return s

    def __eq__(self, other):
        if self.real == other.real and self.imag == other.imag:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def complex_impedance(z, xr):
    """Returns a complex impedance based on an impedance *z* and the X/R ratio.

    Args:
        z: Unitless impedance value.
        xr: X/R ratio.

    Returns:
        Complex impedance (EleComplex).
    """

    z = float(abs(z))
    xr = float(abs(xr))
    real = (z ** 2 / (1 + xr ** 2)) ** 0.5
    try:
        imag = (z ** 2 / (1 + 1 / xr ** 2)) ** 0.5
    except ZeroDivisionError:
        imag = 0.0
    return EleComplex(real, imag)
