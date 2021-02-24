"""Cyclotron Simulation

References:
    [1] Goldstein
"""
import collections
import functools
import types

import numpy
from scipy import integrate

SPEED_OF_LIGHT = 1
MUCH_LESS_THAN = 1 / 10

Result = collections.namedtuple('Result', 'data t x y x_dot y_dot radius mag mag_dot flux speed elec j')


def magnetic_field_strength(t: float, alpha: float, mag_init: float):
    """One possible form of a magnetic field dependence on time, related to PHYS 557 HW 4 Prob 3
    which is given by:
    
        B(t) = \frac{B_0}{2} (1 + e^{-\alpha t})
    
    Args:
        t: 
            float, the time
        alpha: 
            float, the characteristic frequency of the B field change
        mag_init:
            float, B_0

    Returns:
        float, B(t)
    """
    return (1 / 2.0) * mag_init * (1 + numpy.exp(- alpha * t))


def magnetic_field_strength_deriv(t: float, alpha: float, mag_init: float):
    """One possible form of a derivative of magnetic field dependence on time, related to PHYS 557 HW 4 Prob 3
    which is given by:

        B'(t) = \frac{-\alpha B_0}{2} e^{-\alpha t}

    Args:
        t:
            float, the time
        alpha:
            float, the characteristic frequency of the B field change
        mag_init:
            float, B_0

    Returns:
        float, B(t)
    """
    return (-1 / 2.0) * alpha * mag_init * numpy.exp(- alpha * t)


def time_deriv(state: numpy.ndarray, t: float, charge_mass_ratio: float, mag_func: types.FunctionType, mag_deriv_func: types.FunctionType):
    """Compute the time derivative of the state vector (x, y, \dot{x}, \dot{y}) that represents the 
    position and velocity of a particle moving in two dimensions under the Lorentz-force influence of 
    a time-dependent magnetic field perpendicular to the plane of the particle motion
    
    Args:
        state: 
            Array[x, y, x_dot, y_dot]
        t: 
            float, the time step
        charge_mass_ratio:
            float, ratio of charge to mass
        mag_func:
            Function, a function that takes an argument "t" and returns the magnetic field strength
        mag_deriv_func:
            Function, a function that takes an argument "t" and returns time-derivative of magnetic field strength

    Returns:
        Array[dx/dt, dy/dt, dx_dot/dt, dy_dot/dt]
    """
    x, y, x_dot, y_dot = state
    B = mag_func(t)
    B_dot = mag_deriv_func(t)
    dxdt = x_dot
    dydt = y_dot
    dx_dotdt = (1 / 2.0) * charge_mass_ratio * B_dot * y + charge_mass_ratio * y_dot * B
    dy_dotdt = - (1 / 2.0) * charge_mass_ratio * B_dot * x - charge_mass_ratio * x_dot * B
    return numpy.array([dxdt, dydt, dx_dotdt, dy_dotdt])


def solve(t_final: float, t_interval: float = 0.1, t_init: float = 0.0, r_init: float = 1, state_init: numpy.ndarray = None, much_less_than: float = MUCH_LESS_THAN,
          mag_func: types.FunctionType = None, mag_deriv_func: types.FunctionType = None, mag_init: float = 1, charge: float = 1, mass: float = 1):
    """Wrapper around scipy integrator for cyclotron state vector

    Args:
        t_final:
        t_interval:
        t_init:
        r_init:
        mag_func:
        state_init:
        mag_init:
        mag_deriv_func:
        charge:
        mass:

    Returns:

    """
    charge_mass_ratio = charge / mass
    cyclotron_freq = charge_mass_ratio * mag_init / SPEED_OF_LIGHT
    alpha = much_less_than * cyclotron_freq

    if mag_func is None:
        mag_func = functools.partial(magnetic_field_strength, alpha=alpha, mag_init=mag_init)

    if mag_deriv_func is None:
        mag_deriv_func = functools.partial(magnetic_field_strength_deriv, alpha=alpha, mag_init=mag_init)

    # Verbosely set initial conditions if not given:
    if state_init is None:
        B_0 = mag_func(0.0)
        x_0 = r_init
        y_0 = 0.0
        x_dot_0 = 0.0
        y_dot_0 = - charge_mass_ratio * r_init * B_0
        state_init = numpy.array([x_0, y_0, x_dot_0, y_dot_0])

    # Integrate!
    integrand = functools.partial(time_deriv, charge_mass_ratio=charge_mass_ratio, mag_func=mag_func, mag_deriv_func=mag_deriv_func)
    t = numpy.arange(t_init, t_final, t_interval)
    data = integrate.odeint(integrand, state_init, t)

    # Package results
    result = Result(data=data,
                    t=t,
                    x=data[:, 0],
                    y=data[:, 1],
                    x_dot=data[:, 2],
                    y_dot=data[:, 3],
                    radius=numpy.sqrt(data[:, 0] ** 2 + data[:, 1] ** 2),
                    mag=mag_func(t),
                    mag_dot=mag_deriv_func(t),
                    flux=numpy.pi * (data[:, 0] ** 2 + data[:, 1] ** 2) * mag_deriv_func(t),
                    elec=numpy.sqrt(data[:, 0] ** 2 + data[:, 1] ** 2) * mag_deriv_func(t),
                    speed=numpy.sqrt(data[:, 2] ** 2 + data[:, 3] ** 2),
                    j=mag_func(t) * (data[:, 0] ** 2 + data[:, 1] ** 2))
    return result
