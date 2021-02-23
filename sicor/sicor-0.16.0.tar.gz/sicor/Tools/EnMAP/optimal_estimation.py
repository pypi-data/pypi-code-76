#!/usr/bin/env python
# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file provides the basic core functionality for optimal estimation. Practically everything is based on:
# Rodgers C. D., Inverse methods for atmospheric sounding, volume 2 of
# Series on Atmospheric Oceanic and Planetary Physics. World Scientific, 2000.

# Copyright (C) 2018  René Preusker (FU Berlin, <rene.preusker@gmail.com>),
# Freie Universität Berlin, Institute for Space Sciences (FU Berlin, <https://www.geo.fu-berlin.de/wew/index.html>)

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


from collections import namedtuple as NT
import json
import numpy as np
import typing


# not yet supported, thus typing testing with mypy is currently useless
NpArrayT = typing.Type[np.array]

JacobianParamT = typing.Union[None, typing.Any]
GaussNewtonT = typing.Tuple[NpArrayT, NpArrayT, NpArrayT, NpArrayT]
Diagnostic1T = typing.Tuple[NpArrayT, NpArrayT, NpArrayT]
Diagnostic2T = typing.Tuple[NpArrayT, NpArrayT, NpArrayT, NpArrayT]
CallableT = typing.Callable
NpOrAnyT = typing.Union[None, NpArrayT]
FltOrNoneT = typing.Union[None, float]
InternalOptimizerT = typing.Tuple[NpArrayT, NpArrayT, bool, int, NpArrayT, NpOrAnyT, NpOrAnyT, FltOrNoneT, FltOrNoneT,
                                  FltOrNoneT, NpOrAnyT, NpOrAnyT]

EPSIX = np.finfo(float).resolution
# to be larger than ULP
HH = EPSIX ** (1. / 3.)

RESULT = NT('result',
            'state '
            'jacobian '
            'convergence '
            'number_of_iterations '
            'retrieval_error_covariance '
            'gain '
            'averaging_kernel '
            'cost '
            'dof '
            'information_content '
            'retrieval_noise '
            'smoothing_error')

DEFAULTS = {'se': None, 'sa': None, 'xa': None, 'fg': None, 'eps': 0.01, 'jaco': None, 'll': None, 'ul': None, 'mi': 10,
            'fparam': None, 'jparam': None, 'clip': True, 'full': True, 'dx': None, 'gnform': 'n'}


class OeCoreError(Exception):
    pass


class LinAlgError(OeCoreError):
    pass


class NonSquareMatrixError(OeCoreError):
    pass


class MissingInputError(OeCoreError):
    pass


class WrongInputError(OeCoreError):
    pass


def inverse(inn: NpArrayT) -> NpArrayT:
    return invert_np(inn)


def right_inverse(inn: NpArrayT) -> NpArrayT:
    return np.dot(inn.T, inverse(np.dot(inn, inn.T)))


def left_inverse(inn: NpArrayT) -> NpArrayT:
    return np.dot(inverse(np.dot(inn.T, inn)), inn.T)


def invert_np(inn: NpArrayT) -> NpArrayT:
    try:
        out = np.linalg.inv(inn)
    except np.linalg.LinAlgError:
        # TODO
        # Is this always smart?
        # it breaks functional programming, testing .....
        # or better to flag ..
        out = np.random.rand(*inn.shape) / np.nanmean(inn)
    return out


def invert_pupy(inn: NpArrayT) -> NpArrayT:
    """Pure python inversion of a square matrix."""
    try:
        l, u, p = lu_decomposition(inn)
        il = invert_lower(l)
        iu = invert_upper(u)
        out = iu.dot(il).dot(p)
    except LinAlgError:
        # TODO
        # Is this always smart?
        # or better to flag ..
        out = np.random.rand(*inn.shape) / np.nanmean(inn)
    return out


def pivot(a: NpArrayT) -> NpArrayT:
    """Return p, so that p*a is sorted."""
    nr, nc = a.shape
    if nr != nc:
        raise NonSquareMatrixError
    # start with unit matrix
    e = np.eye(nr)
    # sorting is with respect to abs value
    a_abs = np.abs(a)
    for j in range(nc):
        maxidx = a_abs[j:nr, j].argmax() + j
        # exchange rows
        e[[j, maxidx]] = e[[maxidx, j]]
    return e


def lu_decomposition(ua: NpArrayT) -> typing.Tuple[NpArrayT, NpArrayT, NpArrayT]:
    """Decomposes A into P*A=L*U, L is lower, U is upper, P pivot sorting."""
    nr, nc = ua.shape
    p = pivot(ua)
    a = p.dot(ua)
    ll = np.eye(nr)
    u = np.zeros_like(a)
    for j in range(nc):
        for i in range(j + 1):
            sm = (u[0:i, j] * ll[i, 0:i]).sum()
            u[i, j] = a[i, j] - sm
        if np.isclose(u[j, j], 0.):
            raise LinAlgError
        for i in range(j, nr):
            sm = (u[0:j, j] * ll[i, 0:j]).sum()
            ll[i, j] = (a[i, j] - sm) / u[j, j]
    return ll, u, p


def invert_lower(lo: NpArrayT) -> NpArrayT:
    """Calculate the inverse of a lower left triangular square matrix by forward substitution."""
    nr, nc = lo.shape
    ilo = np.zeros_like(lo)
    for j in range(nc):
        ilo[j, j] = 1. / lo[j, j]
        if np.isclose(lo[j, j], 0.):
            raise LinAlgError
        for i in range(j + 1, nr):
            sm = -(lo[i, :] * ilo[:, j]).sum()
            ilo[i, j] = sm / lo[i, i]
    return ilo


def invert_upper(up: NpArrayT) -> NpArrayT:
    return invert_lower(up.T).T


def approximate_jacobian_function(func: typing.Callable) -> typing.Callable:
    """Return numerical jacobian function for a given function ff.

    If func: R^N --> R^M
    then jac:  R^N --> R^(MxN)

    IMPORTANT:
        It is assumed, that *func* takes two
        arguments:
          x:      1d np-array (the state)
          p:      any kind of parameter object...
        Similar to func, *jac_func* takes two arguments
        the state and params, where params is  a 2-tupel:
           params[0] the same as  p for func
           params[1] is delta_x, a 1d np-array
                     of the same size as x,
                     used for the numerical
                     differentiation
    """

    def jac_func(x: NpArrayT, params: JacobianParamT = None, dx: NpArrayT = None) -> NpArrayT:
        """Jacobian function of %s."""
        nx = x.size
        if dx is None:
            sign = np.sign(x)
            dx = np.where((sign * x) < HH, sign * HH, x * HH)
        for ix in range(nx):
            dxm = x * 1.
            dxp = x * 1.
            dxm[ix] = dxm[ix] - dx[ix]
            dxp[ix] = dxp[ix] + dx[ix]
            dyy = func(dxp, params) - func(dxm, params)
            # first run: now I know size of y
            if ix == 0:
                ny = dyy.size
                j = np.zeros((ny, nx), dtype=x.dtype)  # rows first, columns later
            j[:, ix] = dyy[:] / dx[ix] / 2.
        return j

    jac_func.__doc__ = jac_func.__doc__ % func.__name__
    return jac_func


def gauss_newton_increment_nform(x: NpArrayT, y: NpArrayT, k: NpArrayT, xa: NpArrayT, sei: NpArrayT, sai: NpArrayT,
                                 sa: NpArrayT) -> GaussNewtonT:
    """
    input:
        x: state vector
        y: forward(x) - measurement
        k: jacobian(x)
        xa: prior state
        sei: inverse of measurement error co-variance
        sai: inverse of prior error co-variance
        se: measurement error co-variance
        sa: prior error co-variance
    return:
        nx: optimal state respecting measurement and prior
                and coresponding uncertainties
                all for for the linear case
        inc_r: increment of x,
        ret_err_cov_i: inverse of retrieval error covariance
        ret_err_cov:  retrieval error covariance

    Equation: 5.8 (with negative sign put into brackets)
    This variant is a 'n-form' (n = dimension of state).
    """
    kt_sei = np.dot(k.T, sei)
    kt_sei_k = (np.dot(kt_sei, k))
    ret_err_cov_i = sai + kt_sei_k
    ret_err_cov = inverse(ret_err_cov_i)
    kt_sei_y = np.dot(kt_sei, y)
    sai_dx = np.dot(sai, xa - x)
    incr_x = np.dot(ret_err_cov, kt_sei_y - sai_dx)
    nx = x - incr_x
    return nx, incr_x, ret_err_cov_i, ret_err_cov


def gauss_newton_increment_mform(x: NpArrayT, y: NpArrayT, k: NpArrayT, xa: NpArrayT, sei: NpArrayT, sai: NpArrayT,
                                 sa: NpArrayT) -> GaussNewtonT:
    """
    input:
        x: state vector
        y: forward(x) - measurement
        k: jacobian(x)
        xa: prior state
        sei: inverse of measurement error co-variance
        sai: inverse of prior error co-variance
        se: measurement error co-variance
        sa: prior error co-variance
    return:
        nx: optimal state respecting measurement and prior
                and coresponding uncertainties
                all for for the linear case
        inc_r: increment of x,
        ret_err_cov_i: inverse of retrieval error covariance
        ret_err_cov:  retrieval error covariance

    Equation: 5.10 (with negative sign put into brackets)
    This variant is a 'm-form' (m is Dimension of measurement).
    """
    kt_sei = np.dot(k.T, sei)
    kt_sei_k = (np.dot(kt_sei, k))
    sa_kt = np.dot(sa, k.T)
    sa_kt_sei = np.dot(sa_kt, sei)
    sa_kt_sei_k_one = np.dot(sa_kt_sei, k) + np.identity(x.size)
    sa_kt_sei_k_one_i = inverse(sa_kt_sei_k_one)
    sa_kt_sei_y_dx = np.dot(sa_kt_sei, y) - (xa - x)

    incr_x = np.dot(sa_kt_sei_k_one_i, sa_kt_sei_y_dx)
    nx = x - incr_x
    ret_err_cov_i = sai + kt_sei_k
    ret_err_cov = inverse(ret_err_cov_i)
    return nx, incr_x, ret_err_cov_i, ret_err_cov


def check_increment(ix: NpArrayT, sri: NpArrayT, eps: float) -> bool:
    """See Rodgers for details...

    input:
      ix : increment of x_i+1 = x_i -ix
      sri: inverse of retrieval error co-variance
    """
    return np.dot(ix.T, np.dot(sri, ix)) < (eps * ix.size)


def gain_aver_cost(x: NpArrayT, y: NpArrayT, k: NpArrayT, xa: NpArrayT, sei: NpArrayT, sai: NpArrayT,
                   rec: NpArrayT) -> Diagnostic1T:
    """
    input:
        x: state vector
        y: forward(x) - measurement
        k: jacobian(x)
        xa: prior state
        sei: inverse of measurement error co-variance
        sai: inverse of prior error co-variance
        rec: retrieval error covarince
    return:
        gain: gain matrix
        aver: averaging kernel
        cost: cost function
    """
    gain = np.dot(rec, np.dot(k.T, sei))
    aver = np.dot(gain, k)
    cost = np.dot((xa - x).T, np.dot(sai, xa - x)) + np.dot(y.T, np.dot(sei, y))
    return gain, aver, cost


def dof_infocont_retrnoise_smootherrr(sa: NpArrayT, se: NpArrayT, gg: NpArrayT, av: NpArrayT) -> Diagnostic2T:
    dof = np.trace(av)
    # information content h
    w, v = np.linalg.eigh(av)
    h = 0.5 * np.log(1 + w ** 2).sum()
    sn = np.dot(gg, np.dot(se, gg.T))
    ia = np.identity(av.shape[0]) - av
    sme = np.dot(ia, np.dot(sa, ia.T))

    return dof, h, sn, sme


def internal_optimizer(y: NpArrayT, func: CallableT, fparam: NpOrAnyT, jaco: CallableT, jparam: NpOrAnyT, xa: NpArrayT,
                       fg: NpArrayT, sei: NpArrayT, sai: NpArrayT, se: NpArrayT, sa: NpArrayT, dx: NpOrAnyT, eps: float,
                       maxiter: int, full: bool, gnform: str) -> InternalOptimizerT:
    """
    y:       measurement
    func:    function to be inverted
    fparam:  parameter for func
    jaco:    function that returns the jacobian of func
    jparam:  parameter for jaco
    xa:      prior state
    fg:      first guess state
    sei:     inverse of measurement error covariance matrix
    sai:     inverse of prior error covariance matrix
    se :     measurement error covariance matrix
    sa :     prior error covariance matrix
    eps:     if (x_i-x_i+1)^T # S_x # (x_i-x_i+1)   < eps * N_x, optimization
             is stopped. This is the *original* as, e.g. proposed by Rodgers
    maxiter: maximum number of number_of_iterations
    """
    if gnform == 'm':
        increment = gauss_newton_increment_mform
    elif gnform == 'n':
        increment = gauss_newton_increment_nform
    else:
        raise WrongInputError('Unknown key for internal optimizer: %s' % gnform)

    # 1. prior as first guess ...
    if fg is None:
        xn = xa
    else:
        xn = fg

    # 2. optimization
    ii, conv = 0, False
    while not conv and ii <= maxiter:
        ii += 1
        yn = func(xn, fparam) - y
        kk = jaco(xn, jparam, dx)
        xn, ix, sri, sr = increment(xn, yn, kk, xa, sei, sai, sa)
        conv = check_increment(ix, sri, eps)

    # 3. exit
    if full is False:
        return xn, kk, conv, ii, sr, None, None, None, None, None, None, None
    # else:
    gg, av, co = gain_aver_cost(xn, yn, kk, xa, sei, sai, sr)
    dof, ico, sn, sme = dof_infocont_retrnoise_smootherrr(sa, se, gg, av)
    return xn, kk, conv, ii, sr, gg, av, co, dof, ico, sn, sme


def invert_function(func, **args):
    """This solves the following equation:
       y=func(x,params)
       and returns a function which is effectively the inverse of func
       x=func⁻¹(y,fparam=params).

    mandatory INPUT:
       func  = function to be inverted
               y=func(x)
     optional INPUT:
     jaco   = function that returns jacobian of func,
              if not given, numerical differentiation is used
     fparam = default additional parameter for func
     jparam = default additional parameter for corresponding jacobian
              (if no jacobian function is given, and numerical differentiation must
              performed internaly, then jparam shall be either a 2-tupel, where the
              first element is the same parameter object as for *func* and the second
              element is te delta_x. )
      eps   = default convergence criteria when iteration is stopped (Rodgers),xtol=0.001
       xa   = default prior x
       fg   = default first guess x
       sa   = default prior error co-variance
       se   = default measurement error co-variance
       mi   = default maximum number of iterations
     clip   = default lower and upper limit
   gnform   = default Gauss Newton form ('n' or 'm')
    OUTPUT:
       func_inverse    inverse of func
    every optional input can be overwritten in the function
    """
    for kk in DEFAULTS:
        if kk not in args:
            args[kk] = DEFAULTS[kk]
    if args['jaco'] is None:
        args['jaco'] = approximate_jacobian_function(func)

    def func_inverse(yy, fparam=args['fparam'], jparam=args['jparam'], ll=args['ll'], ul=args['ul'], se=args['se'],
                     sa=args['sa'], xa=args['xa'], dx=args['dx'], eps=args['eps'], fg=args['fg'], jaco=args['jaco'],
                     maxiter=args['mi'], full=args['full'], clip=args['clip'], gnform=args['gnform']):
        """Inverse function of *%(name)s*. Estimates the optimal *state*, that explains the measurement *yy*.

        Input:
            yy   = measurement

        optional Input:
          fparam = additional parameter for func
          jparam = additional parameter for corresponding jacobian
            ll   = lower limit (same size and type as state)
            ul   = upper limit (same size and type as state)
            se   = measurement error co-variance matrix
            sa   = prior error co-variance matrix
            xa   = prior
            dx   = for numerical jacobian
            fg   = first guess
           eps   = Rodgers convergence criteria eps
          jaco   = function that returns jacobian of func
        gnform   = Gauss Newton increment ('n' form or 'm' form)

        Output:
            named tuple, containing:
                state
                jacobian
                convergence
                number_of_iterations
                gain
                averaging_kernel
                retrieval_error_covariance
                cost
                dof
                information_content
                retrieval_noise
                smoothing_error
        """
        if sa is None:
            raise MissingInputError('sa is missing')
        if se is None:
            raise MissingInputError('se is missing')
        if xa is None:
            raise MissingInputError('xa (prior) is missing')
        if jparam is None:
            jparam = fparam

        sai = inverse(sa)
        sei = inverse(se)
        if isinstance(yy, list):
            yyy = np.array(yy)
        elif isinstance(yy, float):
            yyy = np.array([yy])
        else:
            yyy = yy

        if jparam is None:
            jparam = fparam

        if clip is True:
            if ll is None:
                raise MissingInputError('ll (lower limit of state) is missing')
            if ul is None:
                raise MissingInputError('ul (upper limit of state) is missing')

            def cfunc(*pargs, **kwargs):
                return func(np.clip(pargs[0], ll, ul), *pargs[1:], **kwargs)

            def cjaco(*pargs, **kwargs):
                return jaco(np.clip(pargs[0], ll, ul), *pargs[1:], **kwargs)
        else:
            cfunc, cjaco = func, jaco

        result = internal_optimizer(y=yyy, xa=xa, fg=fg, sei=sei, sai=sai, se=se, sa=sa, dx=dx, eps=eps,
                                    maxiter=maxiter, func=cfunc, fparam=fparam, jaco=cjaco, jparam=jparam, full=full,
                                    gnform=gnform)

        return RESULT(*result)

    func_inverse.__doc__ = func_inverse.__doc__ % {'name': func.__name__}
    func_inverse.__doc__ += "\n      Defaults are:\n"
    func_inverse.__doc__ += json.dumps(args, default=str, sort_keys=True, indent=12)
    return func_inverse
