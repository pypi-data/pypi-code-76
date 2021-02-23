from matplotlib.pyplot import *
import numpy as np
from numpy import dot
from numpy.linalg import inv, solve
from copy import copy
import tables
import importlib
from numba import jit
from time import time, sleep
from multiprocessing import Pool
from multiprocessing import cpu_count
from itertools import product
import pyprind
from tqdm import tqdm

# custom imports
from ..Tools import initializer, SharedNdarray
from ..Tools import SolarIrradiance
from ..Tools import box_rspf, gauss_rspf

__author = "Niklas Bohn, Andre Hollstein"


@jit(nopython=False)
def nrm(aa, bb):
    cc = 0.0
    nn = aa.shape[0]
    for ii in range(nn):
        cc += np.abs(aa[ii] - bb[ii])
    return cc / nn


@jit(nopython=True)
def int_rho(n_inp, xx_inp, yy_inp, n_int, xx_int, yy_out, jac_out):
    """
    :param n_inp:
    :param xx_inp:
    :param yy_inp:
    :param n_int:
    :param xx_int:
    :param yy_out:
    :param jac_out:
    :return:
    """
    for i_int in range(n_int):
        for i_inp in range(n_inp):
            jac_out[i_inp, i_int] = 0.0
    for i_int in range(n_int):
        for i_inp in range(n_inp):
            if xx_int[i_int] < xx_inp[i_inp]:
                break

        dx = xx_inp[i_inp] - xx_inp[i_inp - 1]
        jac_out[i_inp - 1, i_int] = (xx_inp[i_inp] - xx_int[i_int]) / dx
        jac_out[i_inp, i_int] = (xx_int[i_int] - xx_inp[i_inp - 1]) / dx
        yy_out[i_int] = yy_inp[i_inp - 1] * jac_out[i_inp - 1, i_int] + yy_inp[i_inp] * jac_out[i_inp, i_int]


# noinspection PyShadowingNames
@jit(nopython=True)
def apply_bounds(xii, xi, bounds_up, bounds_dn):
    nn = xii.shape[0]
    step = 0.5
    for ii in range(nn):
        if xii[ii] >= bounds_up[ii]:
            xii[ii] = xi[ii] + step * (bounds_up[ii] - xi[ii])
        if xii[ii] < bounds_dn[ii]:
            xii[ii] = xi[ii] + step * (bounds_dn[ii] - xi[ii])


# noinspection PyShadowingNames
def sat(wvl_inst, wvl_rsp, solar, rspf_type="gaussian", sigma=None, width=None):
    """
    Calculate normalized sensor specific response function with respect to given instrument wavelengths.
    :param wvl_inst: instrument wavelengths
    :param wvl_rsp: response wavelengths
    :param solar: solar irradiances
    :param rspf_type: type of response function, either "gaussian" or "box"
    :param sigma: fwhm of instrument bands (only for type "gaussian")
    :param width: fwhm of instrument bands (only for type "box")
    :return: dictionary containing instrument wavelengths, response wavelengths, sensor specific response function and
    solar irradiances
    """
    rsp = np.zeros((len(wvl_inst), len(wvl_rsp)))
    sol = np.zeros(len(wvl_inst))

    if sigma is not None:
        try:
            _ = sigma[0]  # sigma is array
            assert len(sigma) == len(wvl_inst)
            sigmas = sigma
        except TypeError:
            sigmas = sigma * np.ones(len(wvl_inst))
    else:
        sigmas = None

    if width is not None:
        try:
            _ = width[0]  # sigma is array
            assert len(width) == len(wvl_inst)
            widths = width
        except TypeError:
            widths = width * np.ones(len(wvl_inst))
    else:
        widths = None

    # calculate response function
    if rspf_type == "gaussian":
        for ii_chl, (wvl_center, sigma) in enumerate(zip(wvl_inst, sigmas)):
            rsp[ii_chl, :] = gauss_rspf(wvl_center=wvl_center, wvl_sol_irr=wvl_rsp, sigma=sigma)
            sol[ii_chl] = np.trapz(x=solar.wvl,
                                   y=gauss_rspf(wvl_center=wvl_center, sigma=sigma, wvl_sol_irr=solar.wvl) * solar())
    elif rspf_type == "box":
        for ii_chl, (wvl_center, width) in enumerate(zip(wvl_inst, widths)):
            rsp[ii_chl, :] = box_rspf(wvl_center=wvl_center, wvl_sol_irr=wvl_rsp, width=width)
            sol[ii_chl] = np.trapz(x=solar.wvl,
                                   y=box_rspf(wvl_center=wvl_center, width=width, wvl_sol_irr=solar.wvl) * solar())
    else:
        raise ValueError("Type is wrong.")

    return {"wvl_inst": wvl_inst, "wvl_rsp": wvl_rsp, "rspf": rsp, "sol_irr": sol}


# noinspection PyShadowingNames
def __ff_jj_sc__(self, xi, sc_jj):
    ff, jj = self.reflectance_toa_j(pt=xi)
    jj_t_sc = sc_jj * jj.transpose()  # for numpy broadcasting of sc_jj
    jj_sc = jj_t_sc.transpose()
    return ff, jj_sc, jj_t_sc


# noinspection PyUnresolvedReferences
@jit(nopython=False)
def __se_jj_sa_jit__(ssei, ssai, jj, g):
    ni = ssai.shape[0]
    nk = ssei.shape[0]
    bb = np.zeros((ni, ni))

    for ii in range(ni):
        for jj in range(ni):
            bb[ii, jj] = 0.0
        bb[ii, ii] = bb[ii, ii] + (1.0 + g) * ssai[ii]

    for ii in range(ni):
        for kk in range(nk):
            jj_ii_kk = jj[ii, kk] * ssei[kk]
            if jj_ii_kk != 0.0:
                for jj in range(ni):
                    bb[ii, jj] += jj_ii_kk * jj[jj, kk]

    return bb


def __se_jj_sa_np__(ssei, ssai, jj, g):
    jj_sc = jj
    jj_t_sc = jj.transpose()
    return dot(ssei * jj_sc, jj_t_sc) + (1.0 + g) * np.diag(ssai)


# noinspection PyShadowingNames,PyShadowingNames
def opt(self, y_rfl, pt0, rho_0=[{"method": "const", "value": 0.1},
                                 {"method": "guess", "sigma": None, "fill": 0.1},
                                 {'method': 'prescribed'}][0],
        ftol=None, ftol_rel=None, ee=1.05, n_iter=55, n_bad=5, debug=False, g=0.0,
        ssei=None, ssai=None, instrument_error_model=None, compute_errors=True, sc_oe_thres=0.01,
        optimization=True, se_jj_sa=__se_jj_sa_jit__, rho_fg=None
        ):
    from scipy.ndimage.filters import gaussian_filter1d  # import here to avoid static TLS ImportError

    t0 = time()

    if ssei is None:
        assert hasattr(instrument_error_model,
                       '__call__'), "instrument_error_model should be callable which converts refl. to error."
        # noinspection PyTypeChecker
        ssei = np.nan_to_num(1.0 / (instrument_error_model(y_rfl) ** 2.0))
    else:
        # noinspection PyTypeChecker
        ssei = np.nan_to_num(1.0 / (ssei ** 2.0))
        ssei[ssei > 1e10] = 1e10

    if len(ssai) != len(self.scale_dn):  # not all errors given, assume that first ones are given
        bf = np.ones(len(self.scale_dn), dtype=float)
        bf[:len(ssai)] = ssai[:]
        ssai = bf

    apriori_errors_sc = self.x_phys_to_scaled(ssai, offset_scaling=0.0)[:self.n_jac_at]
    # noinspection PyTypeChecker
    ssai = np.nan_to_num(1.0 / self.x_phys_to_scaled(ssai, offset_scaling=0.0) ** 2.0)  # only error, no offset needed
    ssai[ssai > 1e10] = 1e10

    sai = np.diag(ssai)

    # each method should produce rho_rfl
    if rho_0["method"] == "const":
        rho_rfl = rho_0["value"] * np.ones(self.n_wvl)
    elif rho_0["method"] == "prescribed":
        rho_rfl = np.array(rho_fg, dtype=self.dtype)
        rho_rfl[rho_rfl < 0.0] = 0.0
        rho_rfl[rho_rfl > 1.0] = 0.0
    elif rho_0["method"] == "guess":
        rho_rfl = self.reflectance_boa(pt=pt0, toa_reflectance=y_rfl)
        rho_rfl[rho_rfl < 0.0] = 0.0
        rho_rfl[rho_rfl > 1.0] = 0.0
        if rho_0["sigma"] is not None:
            rho_rfl = gaussian_filter1d(rho_rfl, sigma=rho_0["sigma"])
    else:
        raise ValueError("rho_0 should be dictionary with parameters:%s" % str(rho_0))
    rj = self.rho_to_rj(rho_rfl)
    rj0 = copy(rj)
    pt = copy(pt0)

    xi_ph, yi_ph = self.ptrh2x(pt, rj)
    xa_ph, ya_ph = self.ptrh2x(pt0, rj0)

    xa_sc = self.x_phys_to_scaled(xa_ph)
    xi_sc = self.x_phys_to_scaled(xi_ph)

    if ftol_rel is not None:
        assert ftol is None
        ftol = np.mean(y_rfl) / ftol_rel

    sc_jj = (self.bounds_up - self.bounds_dn) / (self.scale_up - self.scale_dn)

    xi_ph_best = copy(xi_ph)
    yi_ph_best = copy(yi_ph)
    pt_best = copy(pt0)
    rj_best = copy(rj)
    pt_s = np.zeros(len(pt))
    rj_s = np.zeros(len(rj))

    nrms = []
    result = {}
    improved_result = False  # we haven't improved jet
    result["ff"] = y_rfl

    jj_sc_best = np.zeros((len(xi_ph), self.n_wvl))
    jj_t_sc_best = np.zeros((self.n_wvl, len(xi_ph)))

    if np.max(apriori_errors_sc) >= sc_oe_thres and optimization is True:
        ff_best = np.zeros(self.n_wvl)
        nrm_min = 1e10  # nrm(y_rfl,self.reflectance_toa(pt=pt0,rho=rho_rfl))
        i_bad = 0
        for ii in range(n_iter):
            # evaluate actual step, compute Jacobian

            ff, jj_sc, jj_t_sc = __ff_jj_sc__(self, xi=yi_ph, sc_jj=sc_jj)
            nrm_akt = nrm(y_rfl, ff)

            if debug and np.isnan(nrm_akt):
                # import pudb; pu.db
                ff, jj_sc, jj_t_sc = __ff_jj_sc__(self, xi=yi_ph, sc_jj=sc_jj)
                nrm_akt = nrm(y_rfl, ff)

            if debug:  # print debug
                print(("step %2i,akt:%7.4f,min:%7.4f,ftol:%6.4f,ib:%2i->" % (ii, nrm_akt, nrm_min, ftol, i_bad)) +
                      (8 * "%.2f," % tuple(yi_ph[:8]))
                      )

            if ee * nrm_akt < nrm_min:  # if actual step is better than min

                nrm_min = copy(nrm_akt)
                nrms.append(copy(nrm_min))
                i_bad = 0  # reset i_bad counter

                xi_ph_best[:] = xi_ph[:]
                ff_best[:] = ff[:]
                pt_best[:] = pt[:]
                rj_best[:] = rj[:]
                jj_sc_best[:] = jj_sc[:]
                jj_t_sc_best[:] = jj_t_sc[:]
                improved_result = True
            else:
                i_bad += 1
                if i_bad > n_bad:
                    break
            if nrm_min < ftol:
                break

            # make step, compute xi_ph, pt, and rj
            """
            xii_sc = xi_sc + dot(inv(dot(ssei*jj_sc,jj_t_sc)+(1.0+g)*sai),
                                 (dot(jj_sc,ssei*(y_rfl-ff))-ssai*(xi_sc-xa_sc))) # readable but slow
            """
            try:
                xii_sc = xi_sc + np.nan_to_num(
                    solve(se_jj_sa(ssei, ssai, jj_sc, g), (dot(jj_sc, ssei * (y_rfl - ff)) - ssai * (xi_sc - xa_sc))))
                result["ssei"] = ssei
                result["ssai"] = ssai
            except np.linalg.linalg.LinAlgError as err:
                print("LinalgError")
                raise err

            if np.isnan(np.sum(xii_sc)):
                raise ValueError()

            apply_bounds(xii_sc, xi_sc, self.scale_up, self.scale_dn)
            xi_ph = self.x_scaled_to_phys(xii_sc)
            rj[:] = xi_ph[-self.n_rho_lin:]
            pt[:self.n_jac_at] = xi_ph[:self.n_jac_at]
            xi_ph, yi_ph = self.ptrh2x(pt, rj)
            xi_sc = self.x_phys_to_scaled(xi_ph)

        result["ff"] = ff_best

    result["apriori_errors_sc"] = apriori_errors_sc
    result["pt"] = pt_best
    result["rj"] = rj_best

    if compute_errors:
        while True:
            try:
                ss = np.sqrt((np.diagonal(inv(dot(jj_sc_best * ssei, jj_t_sc_best) + sai))))
            except UnboundLocalError:
                ff_best, jj_sc_best, jj_t_sc_best = __ff_jj_sc__(self, xi=yi_ph_best, sc_jj=sc_jj)
            else:
                break

        rj_s[:] = ss[-self.n_rho_lin:]
        pt_s[:self.n_jac_at] = self.x_scaled_to_phys(ss, offset_scaling=0.0)[:self.n_jac_at]
        result["pt_s"] = pt_s
        result["rj_s"] = rj_s

    if improved_result:
        result["rho_ac"] = self.reflectance_boa(pt=pt_best, toa_reflectance=y_rfl)
        result["rho_ac"][result["rho_ac"] > 1.0] = 0.0
        result["rho_ac"][result["rho_ac"] < 0.0] = 0.0

        result["rho_rj"] = copy(self.rj_to_rho_J(rj_best)[0])

        result["rho_rjp"] = copy(self.rj_to_rho_J(rj_best + rj_s)[0])
        result["rho_rjm"] = copy(self.rj_to_rho_J(rj_best - rj_s)[0])

    else:
        result["rho_ac"] = rho_rfl
        result["rho_rj"] = rho_rfl

    if debug:
        print("EEooFF, runtime:%.3fs" % (time() - t0,))
        print(len(pt0) * "%.3f," % tuple(pt0))
        print(len(pt) * "%.3f," % tuple(pt_best))
        print(nrms)

    return result


class Rho2Rj(object):
    def __init__(self, rho_wvl):
        self.rho_wvl = rho_wvl
        self.n_rho_lin = len(rho_wvl)

    def __call__(self, rho):
        return rho


class Rj2RhoJ(object):
    def __init__(self, rho_wvl):
        self.rho_wvl = rho_wvl
        self.n_rho_lin = len(rho_wvl)

    def __call__(self, rj):
        return rj, np.diag(rj)


def rho_wvl_lin_int(wvl, rho_wvl=None, n_rho_max=None, extra_points=None, linear_segments=None, min_wvl_difference=1.0):
    if rho_wvl is not None and n_rho_max is None:  # only rho_wvl given
        pass
    elif n_rho_max is not None and rho_wvl is None:  # only n_rho_max given
        rho_wvl = np.linspace(np.floor(wvl[0]), np.ceil(wvl[-1]), n_rho_max)
    else:
        ValueError("Give either rho_wvl or n_rho_max.s")

    if linear_segments is not None:
        rho_wvl = np.unique(np.hstack((rho_wvl, np.hstack(linear_segments))))
        for ex in linear_segments:
            rho_wvl = (lambda x: rho_wvl[np.invert(np.logical_and(x[0] < rho_wvl, rho_wvl < x[1]))])(ex)

    if extra_points is not None:
        rho_wvl = np.unique(np.hstack((rho_wvl, np.array(extra_points))))

    try:
        while np.min(np.abs(np.diff(rho_wvl[:-1]))) < min_wvl_difference:
            rho_wvl = np.delete(rho_wvl, 1 + np.argmin(np.abs(np.diff(rho_wvl[:-1]))))
    except ValueError:
        pass
    return rho_wvl


# noinspection PyPep8Naming
class Rho2Rj_LinInterp(object):
    def __init__(self, **kwargs):
        self.rho_wvl = rho_wvl_lin_int(**kwargs)
        self.n_rho_lin = len(self.rho_wvl)
        self.wvl = kwargs["wvl"]
        if 'linear_segments' in kwargs:
            self.linear_segments = kwargs["linear_segments"]

    def __call__(self, rho):
        return np.interp(x=self.rho_wvl, xp=self.wvl, fp=rho)


# noinspection PyPep8Naming
class Rj2RhoJ_LinInterp(object):
    def __init__(self, **kwargs):
        self.wvl = kwargs["wvl"]
        self.n_wvl = len(self.wvl)

        if 'linear_segments' in kwargs:
            self.linear_segments = kwargs["linear_segments"]

        self.rho_wvl = rho_wvl_lin_int(**kwargs)
        self.n_rho_lin = len(self.rho_wvl)

        self.rho = np.zeros(self.n_wvl, dtype=float)
        self.J_rho = np.zeros((self.n_rho_lin, self.n_wvl), dtype=float)

    def __call__(self, rj):
        int_rho(self.n_rho_lin, self.rho_wvl, rj, self.n_wvl, self.wvl, self.rho, self.J_rho)
        return self.rho, self.J_rho


# noinspection PyPep8Naming
class Rho2Rj_PCA(object):
    def __init__(self, components, mean, rho_wvl, bounds=None):
        assert len(rho_wvl) == len(mean)
        assert len(rho_wvl) == components.shape[1]

        self.rho_wvl = rho_wvl
        self.wvl = rho_wvl
        self.components = components
        self.mean = mean
        self.n_rho_lin = self.components.shape[0]

        if bounds is None:
            self.bounds_up = +1 * np.ones(self.n_rho_lin)
            self.bounds_dn = -1 * np.ones(self.n_rho_lin)
        else:
            self.bounds_up = +1 * np.abs(bounds)
            self.bounds_dn = -1 * np.abs(bounds)

    def __call__(self, rho):
        return np.dot(self.components, rho - self.mean)


# noinspection PyPep8Naming
class Rj2RhoJ_PCA(Rho2Rj_PCA):
    def __call__(self, rj):
        rho = np.dot(rj, self.components) + self.mean
        rho[rho < 0.0] = 0.0
        rho[rho > 1.0] = 1.0
        return rho, self.components


class Rho2Rj_const(object):
    def __init__(self, rho_wvl):
        self.wvl = rho_wvl
        self.n_rho_lin = len(rho_wvl)

    def __call__(self, rho):
        return rho * np.ones(self.n_rho_lin)


class Rj2RhoJ_const(object):
    def __init__(self, rho_wvl):
        self.wvl = rho_wvl
        self.n_rho_lin = len(rho_wvl)

    def __call__(self, rj):
        rho = rj * np.ones(self.n_rho_lin)
        return rho, np.diag(rho)


# noinspection PyProtectedMember,PyShadowingNames
class RtFo(object):
    def __init__(self, atm_tables_fn,
                 dim_scat,
                 dim_atm=("spr", "coz", "cwv", "tmp"),
                 dim_vza="vza",
                 dim_sza="sza",
                 dim_azi="azi",
                 dim_pca="pca",
                 dim_wvl="wvl",
                 dim_layer="layer",
                 table_path="",
                 buffer_tables=None,
                 only_toa=False,
                 n_pcs=99,
                 dtype=np.float32,
                 slices=None,
                 hash_formats=None,
                 hash_format_default="%.3f,",
                 interpol_dim_range=range(1, 12),
                 sensors=None,
                 response_function_threshold=1e-5,
                 sensor_interpolation_reference=["sensor", "pca"][0],
                 sol_irr_pca=None,
                 default_sensor=None, **_
                 ):
        """
        1. Build Forward Operator Object including relevant data from LUT
        2. Interpolation of atmospheric functions for a specific spectral subset,
        returns object which can be used to compute toa reflectance, radiance and surface reflectance
        :param atm_tables_fn: path to LUT
        :param dim_scat: key of relevant scattering parameter (tau)
        :param dim_atm: keys of relevant atmospheric parameters
        :param dim_vza: key of viewing zenith angle
        :param dim_sza: key of sun zenith angle
        :param dim_azi: key of sun azimuth angle
        :param dim_pca: key of principle components
        :param dim_wvl: key of wavelengths
        :param dim_layer: key of atmospheric layer
        :param table_path: path to aerosol table within LUT
        :param buffer_tables: AC table for specific sensors (smile)
        :param only_toa: use only TOA fluxes
        :param n_pcs: number of principle components
        :param dtype: data type of values stored in dimensions dictionary
        :param slices: part of LUT which should be considered
        :param hash_formats: fixed length of the parameter values
        :param hash_format_default: default length of the parameter values
        :param interpol_dim_range: maximum dimension of interpolation
        :param sensors: dict containing wavelength, response function and solar irradiances of input sensor
        :param response_function_threshold: threshold for sensor response function
        :param sensor_interpolation_reference: interpolation reference
        :param sol_irr_pca: principle components of solar irradiance
        :param default_sensor: default sensor
        :param _:
        """
        # check input parameters

        if slices is None:
            slices = {}
        if hash_formats is None:
            hash_formats = {}

        assert type(dim_scat) == list, "dim_scat is not list"
        assert all(isinstance(item, str) for item in dim_scat), "should be string with dim name for hdf5 file"
        assert type(n_pcs) == int
        assert type(table_path) == str, "table_path should be path string in hdf5 file"
        assert type(only_toa) == bool
        assert all(isinstance(item, int) for item in interpol_dim_range), "interpol_dim_range should only contain ints"
        assert type(slices) == dict, "Slices should be dictionary with dim_name:slice as key:value pairs"
        assert type(hash_formats) == dict, "hash_patterns should be dictionary"
        assert type(response_function_threshold) == float, "response_function_threshold should be small float number"

        # load interpolation classes
        self.interp = {ii: importlib.import_module("sicor.Tools.NM.interp_spectral_n_%i" % ii) for ii in
                       interpol_dim_range}
        # open LUT hdf5 file and group as defined in table_path
        with tables.open_file(atm_tables_fn, "r") as atm_tables_h5:
            self.atm_tables_h5 = atm_tables_h5
            self.atm_tables = atm_tables_h5.root
            self.grp = self.atm_tables.__getattr__(table_path)
            # copy dimension data names to self, collect in dim_names
            self.wvl_pca = self.atm_tables.__getattr__(dim_wvl).read()
            self.wvl = self.wvl_pca
            self.n_wvl = len(self.wvl_pca)
            self.dtype = dtype

            self.dim_scat = dim_scat
            self.dim_atm = dim_atm
            self.dim_vza = dim_vza
            self.dim_sza = dim_sza
            self.dim_azi = dim_azi
            self.dim_pca = dim_pca
            self.dim_layer = dim_layer
            self.dim_names = list(self.dim_atm) + list(self.dim_scat) + [
                self.dim_vza, self.dim_sza, self.dim_azi, self.dim_pca, self.dim_layer]

            self.sza_reduced = None
            self.vza_reduced = None

            # set given slices, default is all elements
            self.slices = {dim: slice(None) for dim in self.dim_names}
            for dim, slc in slices.items():
                self.slices[dim] = slc
            # same same for hash formats
            self.hash_formats = {dim: hash_format_default for dim in self.dim_names}
            for dim, slc in hash_formats.items():
                self.hash_formats[dim] = slc
            # set number of principal components, add slice for pca dimension
            self.n_pca_max = self.grp.E_DN.components.shape[0]
            self.n_pcs = np.min([self.n_pca_max, n_pcs])
            self.slices[self.dim_pca] = slice(0, self.n_pcs)
            # set dictionary for dimension_name:scale
            self.dims = {dim: np.array(self.atm_tables.__getattr__(dim)[self.slices[dim]], dtype=self.dtype) for dim in
                         self.dim_names}
            # convert arccos to degree
            self.dims[self.dim_vza] = np.rad2deg(np.arccos(self.dims[self.dim_vza]))
            self.dims[self.dim_sza] = np.rad2deg(np.arccos(self.dims[self.dim_sza]))

            # set sensor wavelengths, response function and solar irradiances
            self.sensors = sensors
            if self.sensors is not None:
                self.response_function_threshold = response_function_threshold
                self.sensor_interpolation_reference = sensor_interpolation_reference
                self.wvl_sensors = {sensor_name: sensor["wvl_inst"] for sensor_name, sensor in self.sensors.items()}
                self.sol_irr_sensors = {sensor_name: sensor["sol_irr"] / np.pi for sensor_name, sensor in
                                        self.sensors.items() if sensor["sol_irr"] is not None}
                for name, sensor in self.sensors.items():
                    self.__instrument_val__(sensor)
            self.components = "components"
            self.mean = "mean"
            if sol_irr_pca is not None:
                self.sol_irr_pca = sol_irr_pca / np.pi
            else:
                self.sol_irr_pca = None
            self.sol_irr = self.sol_irr_pca

            # each atmospheric function is defined as dictionary with common types as defined in __mk_table__
            # serves as preparation for the atmospheric dimension interpolation
            # __mk_table__ creates a spectral subset of the LUT to match the wavelengths (or subset) of the input sensor
            # process atmospheric path reflection and upward transmittance only at TOA
            if only_toa:

                if buffer_tables is not None and "L0" in buffer_tables:
                    self.L0 = buffer_tables["L0"]
                else:
                    self.L0 = self.__mk_tble__(
                        grp=self.grp.L0_TOA,
                        dims=(list(self.dim_atm) + list(self.dim_scat) +
                              [self.dim_vza, self.dim_sza, self.dim_azi, self.dim_pca])
                    )

                if buffer_tables is not None and "T_UP" in buffer_tables:
                    self.T_UP = buffer_tables["T_UP"]
                else:
                    self.T_UP = self.__mk_tble__(
                        grp=self.grp.T_UP_TOA,
                        dims=list(self.dim_atm) + list(self.dim_scat) + [self.dim_vza, self.dim_pca],
                        idx=self.L0["dims"]
                    )
            # process atmospheric path reflection and upward transmittance including the layer dimension
            else:
                self.L0 = self.__mk_tble__(
                    grp=self.grp.L0,
                    dims=(list(self.dim_atm) + list(self.dim_scat) +
                          [self.dim_layer, self.dim_vza, self.dim_sza, self.dim_azi, self.dim_pca])
                )
                self.T_UP = self.__mk_tble__(
                    grp=self.grp.T_UP,
                    dims=list(self.dim_atm) + list(self.dim_scat) + [self.dim_layer, self.dim_vza, self.dim_pca],
                    idx=self.L0["dims"]
                )

            self.pt_dims = copy(self.L0["dims"])
            self.pt_dims.remove(self.dim_pca)
            self.jacobean_switch = {dim_name: 1 for dim_name in self.pt_dims}

            if buffer_tables is not None and "E_DN" in buffer_tables:
                self.E_DN = buffer_tables["E_DN"]
            else:
                self.E_DN = self.__mk_tble__(grp=self.grp.E_DN,
                                             dims=list(self.dim_atm) + list(self.dim_scat) + [self.dim_sza,
                                                                                              self.dim_pca],
                                             idx=self.L0["dims"]
                                             )

            if buffer_tables is not None and "SS" in buffer_tables:
                self.SS = buffer_tables["SS"]
            else:
                self.SS = self.__mk_tble__(grp=self.grp.SS,
                                           dims=list(self.dim_atm) + list(self.dim_scat) + [self.dim_pca],
                                           idx=self.L0["dims"]
                                           )

        # settings for interpolation between atmospheric dimensions
        self.__jacobean__ = False
        self.__caching__ = False

        self.__jacobean_range__ = self.SS["idx"]
        self.n_jac_at = len(self.__jacobean_range__)
        self.n_jac_fl = len(self.L0["idx"])

        self.interpolation_settings(jacobean=self.__jacobean__,
                                    caching=self.__caching__)

        self.idx_dim_vza = self.L0["dims"].index(self.dim_vza)
        self.idx_dim_sza = self.L0["dims"].index(self.dim_sza)

        if default_sensor is not None:
            self.set_sensor(default_sensor)

        self.rho = None
        self.J_rho = None
        self.n_rho_lin = None

        self.bounds_atm = None

        self.bounds_up = None
        self.bounds_dn = None

        self.scale_up = None
        self.scale_dn = None

        self.rho_to_rj = None
        self.rj_to_rho_J = None

        self.LUTS = (self.L0, self.E_DN, self.T_UP, self.SS)
        self.LUT_suffixs = []

        self.current_sensor = ""

    # noinspection PyPep8Naming
    def set_rho_lin(self, Rho2Rj, Rj2RhoJ):
        """
        Assign the surface reflectance model to the forward operator.
        :param Rho2Rj: Model to obtain a first guess of surface reflectance values for selected absorption feature
        wavelengths.
        :param Rj2RhoJ: Surface reflectance model. Following models can be chosen: Rj2RhoJ_LinInterp, Rj2RhoJ_PCA or
        Rj2RhoJ_const for Sentinel-2; Rj2RhoJ_LinX1X2 for EnMAP single CH4/CWV Retrieval or Rj2RhoJ_Beer_Lambert for
        EnMAP simultaneous 3 phases of water retrieval.
        :return: None
        """
        # test api for surface reflectance model class
        assert hasattr(Rho2Rj, '__call__')
        assert hasattr(Rj2RhoJ, '__call__')
        assert Rho2Rj.n_rho_lin == Rj2RhoJ.n_rho_lin

        self.rho_to_rj = Rho2Rj
        self.rj_to_rho_J = Rj2RhoJ

        # number of surface reflectance values (i.e. number of the respective absorption feature wavelengths) used by
        # the chosen model
        self.n_rho_lin = Rho2Rj.n_rho_lin

        # Assign lower and upper bounds for the values of atmospheric state parameters
        self.bounds_atm = np.array(self.L0["range"])
        self.bounds_up = np.ones(self.n_jac_fl + self.n_rho_lin)
        self.bounds_up[:self.n_jac_fl] = self.bounds_atm[:self.n_jac_fl, 1]

        self.bounds_dn = np.zeros(self.n_jac_fl + self.n_rho_lin)
        self.bounds_dn[:self.n_jac_fl] = self.bounds_atm[:self.n_jac_fl, 0]

        try:
            self.bounds_up[self.n_jac_fl:] = Rho2Rj.bounds_up
            self.bounds_dn[self.n_jac_fl:] = Rho2Rj.bounds_dn
        except AttributeError:
            pass

        # assign lower and upper bounds for scaling of the values of atmospheric state parameters
        self.scale_up = 1.0 + np.zeros(self.bounds_up.shape[0])
        self.scale_dn = 0.0 + np.zeros(self.bounds_up.shape[0])

        # check if instrument wavelengths equal model walenghths
        if np.sum(np.abs(self.wvl - self.rho_to_rj.wvl)) > 0.0:
            print("Warning, do something!")

    def ptrh2x(self, pt, rj):
        return np.hstack((pt[self.__jacobean_range__], rj)), np.hstack((pt, rj))

    def x_phys_to_scaled(self, xx, offset_scaling=1.0):
        """
        Convert physical values of atmospheric state parameters to scaled values with respect to the upper bounds..
        :param xx: array containing physical values of atmospheric state parameters
        :param offset_scaling: offset scaling
        :return: array containing scaled values of atmospheric state parameters
        (ratio of the max. value as defined in LUT)
        """
        aa = (self.scale_up - self.scale_dn) / (self.bounds_up - self.bounds_dn)
        bb = self.scale_dn - aa * self.bounds_dn
        return aa * xx + bb * offset_scaling

    def x_scaled_to_phys(self, xx, offset_scaling=1.0):
        """
        Convert scaled values of atmospheric parameters to physical values.
        :param xx: array containing scaled values of atmospheric state parameters
        (ratio of the max. value as defined in LUT)
        :param offset_scaling: offset scaling
        :return: array containing physical values of atmospheric state parameters
        """
        aa = (self.bounds_up - self.bounds_dn) / (self.scale_up - self.scale_dn)
        bb = self.bounds_dn - aa * self.scale_dn
        return aa * xx + bb * offset_scaling

    def pt(self, **kwargs):
        pt = np.zeros(len(self.pt_dims))
        for ii, key in enumerate(self.pt_dims):
            pt[ii] = kwargs[key]
        return pt

    @staticmethod
    def __instrument_val__(instrument):
        for key in ["wvl_inst", "wvl_rsp", "rspf"]:
            assert type(instrument[key]) == np.ndarray, "%s should be numpy ndarray"
        assert instrument["rspf"].shape == (
            len(instrument["wvl_inst"]), len(instrument["wvl_rsp"])), "Shape of rspf is wrong."

    @staticmethod
    def __component_key__(sensor_name):
        return sensor_name + "_components"

    @staticmethod
    def __mean_key__(sensor_name):
        return sensor_name + "_mean"

    def set_sensor(self, sensor_name=None):

        self.rho_to_rj = None
        self.rj_to_rho_J = None

        if sensor_name is None:
            self.components = "components"
            self.mean = "mean"
            self.wvl = self.wvl_pca
            self.sol_irr = self.sol_irr_pca
            self.current_sensor = sensor_name
        else:
            assert self.sensors is not None, "Sensors were not defined on init."
            assert sensor_name in self.sensors, "Sensor %s were not defined. Defined are:%s" % (
                sensor_name, str(self.sensors.keys()))
            self.components = self.__component_key__(sensor_name)
            self.mean = self.__mean_key__(sensor_name)
            self.wvl = self.wvl_sensors[sensor_name]
            self.sol_irr = self.sol_irr_sensors[sensor_name] if sensor_name in self.sol_irr_sensors else None
            self.current_sensor = sensor_name
        self.n_wvl = len(self.wvl)

    def interpolation_settings(self, jacobean, caching):
        """
        Set Jacobean and/or caching to True or False.
        :param jacobean: True or False
        :param caching: True or False
        :return: None
        """
        assert type(jacobean) == bool
        assert type(caching) == bool
        for interp in [self.E_DN, self.SS, self.T_UP, self.L0]:
            interp["int"].settings(jacobean, caching)
        self.__jacobean__ = jacobean
        self.__caching__ = caching

    # noinspection PyProtectedMember,PyDictCreation
    def __mk_tble__(self, grp, dims, idx=None):
        """
        Build a subset of LUT for each atmospheric function to match the spectral subset of the input sensor.
        :param grp: atmospheric function
        :param dims: parameters of the atmospheric state the respective function depends on
        :param idx: indices dims as stored in LUT
        :return: spectral subset of LUT for the respective atmospheric function
        """
        assert type(grp) == tables.group.Group, "grp should be hdf5 group"
        assert all(isinstance(item, str) for item in dims), "dims should be list of strings with dim names"
        # set up table dict
        tble = {}
        # noinspection PyProtectedMember
        # fill dict with information from LUT and set interpolation parameters
        tble["pathname"] = grp._v_pathname
        tble["dims"] = dims
        tble["components"] = np.array(grp.components[0:self.n_pcs, :], dtype=self.dtype)
        tble["mean"] = np.array(grp.mean[:], dtype=self.dtype)
        tble["range"] = [(self.dims[dim][0], self.dims[dim][-1]) for dim in tble["dims"]]
        tble["n_dims"] = len(tble["dims"]) - 1  # only for interpolation, spectral dim doesn't count
        # set up the jacobian with the same dimension as the atmospheric state
        tble["jacobean_switch"] = np.ones((tble["n_dims"], self.n_pcs))
        # load table data to memory, according to given slice
        tble["dat"] = np.array(grp.pca[tuple([self.slices[dim] for dim in tble["dims"]])], dtype=self.dtype)
        if idx is None:
            tble["idx"] = np.arange(tble["n_dims"])
        else:
            tble["idx"] = np.array([idx.index(dim) for dim in tble["dims"][:-1]], dtype=int)

        # instance the n-dimensional interpolation function (n = number of dimensions of atmospheric state)
        tble["int"] = self.interp[tble["n_dims"]].intp(data=tble["dat"],
                                                       axes=[self.dims[dim] for dim in tble["dims"][:-1]],
                                                       hash_pattern="".join(
                                                           [self.hash_formats[dim] for dim in tble["dims"][:-1]]))

        if self.sensors is not None:
            # build LUT subset with respect to either the sensor response wavelengths (default) or the wavelengths
            # stored in the LUT.
            # for now this is super slow - but we do this only once and premature optimization might not be needed here
            for sensor_name, sensor in tqdm(self.sensors.items()):
                components = self.__component_key__(sensor_name)
                mean = self.__mean_key__(sensor_name)

                tble[components] = np.zeros((self.n_pcs, len(self.sensors[sensor_name]["wvl_inst"])))
                tble[mean] = np.zeros(len(self.sensors[sensor_name]["wvl_inst"]))

                if self.sensor_interpolation_reference == "sensor":
                    sels = [(lambda x: slice(x[0], x[1]))(
                        np.where(sensor["rspf"][jj_sensor, :] > self.response_function_threshold)[0][[0, -1]]) for
                        jj_sensor in range(len(sensor["wvl_inst"]))]

                    for jj_sensor, sel in zip(range(len(sensor["wvl_inst"])), sels):
                        smpl = np.interp(x=sensor["wvl_rsp"][sel], xp=self.wvl_pca, fp=tble["mean"], left=0.0,
                                         right=0.0)
                        buf = np.trapz(x=sensor["wvl_rsp"][sel], y=sensor["rspf"][jj_sensor, sel] * smpl)
                        tble[mean][jj_sensor] = buf
                    for jj_pc in range(self.n_pcs):
                        for jj_sensor, sel in zip(range(len(sensor["wvl_inst"])), sels):
                            smpl = np.interp(x=sensor["wvl_rsp"][sel], xp=self.wvl_pca, fp=tble["components"][jj_pc, :])
                            buf = np.trapz(x=sensor["wvl_rsp"][sel], y=sensor["rspf"][jj_sensor, sel] * smpl)
                            tble[components][jj_pc, jj_sensor] = buf

                elif self.sensor_interpolation_reference == "pca":
                    for jj_sensor in range(len(sensor["wvl_inst"])):
                        smpl = np.interp(x=self.wvl_pca, xp=sensor["wvl_rsp"], fp=sensor["rspf"][jj_sensor, :],
                                         left=0.0, right=0.0)
                        buf = np.trapz(x=self.wvl_pca, y=tble["mean"][:] * smpl)
                        tble[mean][jj_sensor] = buf
                    for jj_pc in range(self.n_pcs):
                        for jj_sensor in range(len(sensor["wvl_inst"])):
                            smpl = np.interp(x=self.wvl_pca, xp=sensor["wvl_rsp"], fp=sensor["rspf"][jj_sensor, :],
                                             left=0.0, right=0.0)
                            buf = np.trapz(x=self.wvl_pca, y=tble["components"][jj_pc, :] * smpl)
                            tble[components][jj_pc, jj_sensor] = buf
                else:
                    raise ValueError("self.sensor_interpolation_reference=\"%s\" is not implemented" %
                                     self.sensor_interpolation_reference)
        return tble

    def __interpolate__(self, func, pt):
        """
        Interpolate within atmospheric function for a given state.
        :param func: atmospheric function (E_DN, L0, SS, T_UP)
        :param pt: array containing atmospheric state parameters
        :return: interpolated spectrum and its jacobean of atmospheric function
        """
        try:
            if func["int"].__jacobean__:  # we have a Jacobean
                ii, jj = func["int"](pt[func["idx"]])  # e.g., sicor.Tools.NM.interp_spectral_n_3.intp(pt[0, 2, 6])
                # reconstruction of the spectrum from the principle components using matrix multiplication
                spectrum = np.dot(ii, func[self.components]) + func[self.mean]
                jacobean = np.dot(jj * func["jacobean_switch"], func[self.components])
                if self.__jacobean_range__ is None:
                    return spectrum, jacobean
                else:
                    return spectrum, jacobean[self.__jacobean_range__, :]

            else:  # spectral scalar return case
                return np.dot(func["int"](pt[func["idx"]]), func[self.components]) + func[self.mean]
        except ValueError as err:
            raise err

    def set_jacobean_switch(self, **kwargs):
        """ update self.jacobean_switch and update function jacobean switch matrices """
        for key, value in kwargs.items():
            self.jacobean_switch[key] = value
        for func in [self.T_UP, self.E_DN, self.SS, self.L0]:
            self.__set_jacobean_switch__(func)

    def __set_jacobean_switch__(self, func):
        """ edit jacobean switch matrix of function according to self.jacobean_switch """
        for ii, dim in enumerate(func["dims"][:-1]):
            func["jacobean_switch"][ii] = self.jacobean_switch[dim]

    def ee(self, pt):
        """
        Interpolate E_DN for a given atmospheric state pt.
        :param pt: atmospheric state
        :return: solar downward reflection at the surface
        """
        return self.__interpolate__(self.E_DN, pt)

    def tt(self, pt):
        """
        Interpolate T_UP for a given atmospheric state pt.
        :param pt: atmospheric state
        :return: upward transmittance
        """
        return self.__interpolate__(self.T_UP, pt)

    def ss(self, pt):
        """
        Interpolate SS for a given atmospheric state pt.
        :param pt: atmospheric state
        :return: spherical albedo
        """
        return self.__interpolate__(self.SS, pt)

    def l0(self, pt):
        """
        Interpolate L0 for a given atmospheric state pt.
        :param pt: atmospheric state
        :return: atmospheric path reflectance
        """
        return self.__interpolate__(self.L0, pt)

    def reflectance_to_radiance(self, reflectance, pt):
        """
        Convert TOA reflectance to radiance.
        :param reflectance: TOA reflectance
        :param pt: atmospheric state
        :return: TOA radiance
        """
        return reflectance * self.sol_irr * self.mu_sun(pt)

    def radiance_to_reflectance(self, radiance, pt, in_place=False):
        """
        Convert TOA radiance to reflectance.
        :param radiance: TOA radiance
        :param pt: atmospheric state
        :param in_place: if True, convert input radiance array without returning a new one
        :return: if in_place=False, TOA reflectance, else None
        """
        if in_place is True:
            radiance_bf = radiance.reshape((-1, radiance.shape[-1])).T
            radiance_bf /= self.mu_sun(pt).reshape(-1)
            radiance /= self.sol_irr
        else:
            return radiance / (self.sol_irr * self.mu_sun(pt))

    def reflectance_toa(self, pt, rho):
        """
        Calculate TOA reflectance for a given atmospheric state and for given surface reflectance
        by interpolating in the LUT and applying the simplified solution of the RTE.
        :param pt: atmospheric state
        :param rho: surface reflectance
        :return: TOA reflectance
        """
        if self.__jacobean__:
            self.interpolation_settings(jacobean=False, caching=self.__caching__)

        ee = self.ee(pt)
        tt = self.tt(pt)
        ss = self.ss(pt)
        l0 = self.l0(pt)

        # this is the simplified solution of the RTE
        return (ee * rho * tt / (-rho * ss + 1) + l0 * np.pi) / self.mu_sun(pt)

    def radiance_toa(self, pt, rho):
        """
        Convert TOA reflectance, calculated by the simplified solution of the RTE, to radiance.
        :param pt: atmospheric state
        :param rho: surface reflectance
        :return: TOA radiance
        """
        return self.reflectance_to_radiance(self.reflectance_toa(pt, rho), pt)

    def reflectance_toa_j(self, pt):
        """
        Calculate TOA reflectance for a given atmospheric state by interpolating in the LUT and applying
        the simplified solution of the RTE. The needed surface reflectance value is derived from
        the predefined surface reflectance model. Additionally, the Jacobian is calculated.
        :param pt: atmospheric state
        :return: TOA reflectance and the Jacobian
        """
        if self.__jacobean__ is False:
            self.interpolation_settings(jacobean=True, caching=self.__caching__)
        assert len(pt) >= max(self.L0["idx"]) + + self.n_rho_lin

        ee, j_ee = self.ee(pt)
        tt, j_tt = self.tt(pt)
        ss, j_ss = self.ss(pt)
        l0, j_l0 = self.l0(pt)

        # calculate surface reflectance and its Jacobian from the surface reflectance model
        rho, j_rho = self.rj_to_rho_J(pt[-self.n_rho_lin:])

        # calculate TOA reflectance
        ll = ee * rho * tt / (-rho * ss + 1) + l0 * np.pi

        # calculate Jacobian
        jj = np.zeros((self.n_jac_at + self.n_rho_lin, self.n_wvl))
        jj[0:self.n_jac_at, :] = (j_l0 * np.pi * (rho * ss - 1) ** 2 + j_ss * ee * rho ** 2 * tt - rho * (
            j_ee * tt + j_tt * ee) * (rho * ss - 1)) / (rho * ss - 1) ** 2
        jj[self.n_jac_at:, :] = j_rho * ee * tt / (rho * ss - 1) ** 2

        return ll, jj

    def radiance_toa_j(self, pt):
        """
        Convert TOA reflectance, calculated by the simplified solution of the RTE, to radiance.
        Additionally, the Jacobian is calculated.
        :param pt: atmospheric state
        :return: TOA radiance and the Jacobian
        """
        ll, jj = self.reflectance_toa_j(pt)
        return (self.reflectance_to_radiance(ll, pt),
                self.reflectance_to_radiance(jj, pt))

    def mu_sun(self, pt):
        """
        Compute cosine of solar incidence angle for given background state pt.
        :param pt: pt numpy ndarray which holds background information for data, e.g. 1-D array with
        state (water vapor, observation angles, ...) or e.g. 3-D array with first two dimensions
        for the 'image' and the last for the state
        :return: cosine of solar angle
        """
        if self.idx_dim_sza is not None:
            assert isinstance(pt, np.ndarray)
            return np.cos(np.deg2rad(
                pt.__getitem__((pt.ndim-1)*[slice(None)] + [self.idx_dim_sza])))
        else:
            return np.cos(np.deg2rad(self.sza_reduced))

    def reflectance_boa(self, pt, toa_radiance=None, toa_reflectance=None):
        """
        Calculate surface reflectance for a given atmospheric state and for given TOA reflectance or radiance
        by interpolating in the LUT and applying the simplified solution of the RTE.
        :param pt: atmospheric state
        :param toa_radiance: TOA radiance
        :param toa_reflectance: TOA reflectance
        :return: surface reflectance
        """
        if self.__jacobean__:
            self.interpolation_settings(jacobean=False, caching=self.__caching__)
        # if TOA radiance is given, convert to TOA reflectance
        if toa_reflectance is None and toa_radiance is not None:
            toa_reflectance = self.radiance_to_reflectance(toa_radiance, pt)

        ll = toa_reflectance
        ee = self.ee(pt)
        tt = self.tt(pt)
        ss = self.ss(pt)
        l0 = self.l0(pt)

        ld = ll - l0 * np.pi
        return ld / (ee * tt + ld * ss)

    def reflectance_boa_j(self, pt, toa_radiance=None, toa_reflectance=None):
        """
        Calculate surface reflectance for a given atmospheric state and for given TOA reflectance or radiance
        by interpolating in the LUT and applying the simplified solution of the RTE.
        Additionally, the Jacobian is calculated.
        :param pt: atmospheric state
        :param toa_radiance: TOA radiance
        :param toa_reflectance: TOA reflectance
        :return: surface reflectance and the Jacobian
        """
        if self.__jacobean__ is False:
            self.interpolation_settings(jacobean=True, caching=self.__caching__)
        # if TOA radiance is given, convert to TOA reflectance
        if toa_reflectance is None and toa_radiance is not None:
            toa_reflectance = self.radiance_to_reflectance(toa_radiance, pt)

        ll = toa_reflectance
        ee, j_ee = self.ee(pt)
        tt, j_tt = self.tt(pt)
        ss, j_ss = self.ss(pt)
        l0, j_l0 = self.l0(pt)

        ld = ll - l0 * np.pi
        # calculate surface reflectance
        rr = ld / (ee * tt + ld * ss)
        # calculate Jacobian
        jj = -(j_l0 * np.pi * (ee * tt + ss * (ll - l0 * np.pi)) + (ll - l0 * np.pi) * (
            j_ee * tt - j_l0 * np.pi * ss + j_ss * (ll - l0 * np.pi) + j_tt * ee)) / (ee * tt +
                                                                                      ss * (ll - l0 * np.pi)) ** 2
        return rr, jj

    def __reduce_LUT__(self, fkt, reduce_suffix, reduce_dims):
        """
        Reduce dimension of LUT by defining fixed values for chosen state parameters.
        :param fkt: table of atmospheric function
        :param reduce_suffix: suffix of the name for LUT subset
        :param reduce_dims: state parameters to be fixed
        :return: None
        """

        def get_int_dx(dims, value):
            """
            dims: numpy array, monotonly rising, scale
            value: scalar, within dims
            returns: lower index for bin containing value, fraction of value within bin
            """
            ii, dd = None, None  # init count variables with None, will raise error if not found
            for ii, dd in enumerate(dims):
                if dd >= value:
                    break
            return ii - 1, (dd - value) / (dd - dims[ii - 1])

        principal_keys = ["range", "idx", "dims", "dat", "jacobean_switch"]
        for key in principal_keys:  # rename principal keys to key_orig if necessary
            new_key = key + "_orig"
            if new_key not in fkt:
                fkt[new_key] = fkt.pop(key)
        if "int_orig" not in fkt:
            fkt["int_orig"] = fkt.pop("int")

        dat = copy(fkt["dat_orig"])
        idx = list(copy(fkt["idx_orig"]))
        dms = copy(fkt["dims_orig"])
        rng = copy(fkt["range_orig"])
        jac = copy(fkt["jacobean_switch_orig"])

        # perform reduction trough linear interpolation
        for reduce_dim, value in reduce_dims.items():
            if reduce_dim in dms:
                rdx = dms.index(reduce_dim)
                rii, rpp = get_int_dx(self.dims[reduce_dim], value)

                slc1 = len(dat.shape) * [slice(None)]
                slc2 = copy(slc1)
                slc1[rdx] = rii
                slc2[rdx] = rii + 1

                dat = rpp * dat[tuple(slc1)] + (1.0 - rpp) * dat[tuple(slc2)]
                _ = dms.pop(rdx)
                _ = idx.pop(rdx)
                _ = rng.pop(rdx)
                jac = np.delete(jac, rdx, axis=0)

        idx = np.array(idx, dtype=int)

        for key, val in [("dat", dat), ("idx", idx), ("dims", dms), ("range", rng), ("jacobean_switch", jac)]:
            fkt["%s_%s" % (key, reduce_suffix)] = val

        fkt["reduce_dims_%s" % reduce_suffix] = reduce_dims

        fkt["int_%s" % reduce_suffix] = self.interp[len(dat.shape) - 1].intp(data=fkt["dat_%s" % reduce_suffix],
                                                                             caching=True,
                                                                             axes=[self.dims[dim] for dim in
                                                                                   fkt["dims_%s" % reduce_suffix][:-1]],
                                                                             hash_pattern="".join(
                                                                                 [self.hash_formats[dim] for dim in
                                                                                  fkt["dims_%s" % reduce_suffix][:-1]]),
                                                                             )

    def reduce_luts(self, reduce_suffix, reduce_dims, set_new_luts=True):
        """
        Function to call for reducing dimension of LUT.
        :param reduce_suffix: suffix of the name for LUT subset
        :param reduce_dims: state parameters to be fixed
        :param set_new_luts:
        :return: None
        """
        for fkt in self.LUTS:
            self.__reduce_LUT__(fkt, reduce_suffix, reduce_dims)
        if reduce_suffix not in self.LUT_suffixs:
            self.LUT_suffixs.append(reduce_suffix)
        if set_new_luts is True:
            self.set_luts(reduce_suffix)

    def set_luts(self, suffix):
        """
        Assigns a LUT to the forward operator.
        :param suffix: suffix of the LUT's name
        :return: None
        """
        principal_keys = {"range", "idx", "dims", "dat", "int", "jacobean_switch"}
        for fkt in self.LUTS:
            for key in principal_keys:
                try:
                    fkt[key] = fkt["%s_%s" % (key, suffix)]
                except KeyError:
                    if suffix != "orig":
                        raise

        self.__jacobean_range__ = np.arange(len(self.SS["idx"]))
        self.n_jac_at = len(self.__jacobean_range__)
        self.n_jac_fl = len(self.L0["idx"])
        try:
            self.idx_dim_sza = self.L0["dims"].index(self.dim_sza)
        except ValueError:
            self.idx_dim_sza = None
            self.sza_reduced = self.L0["reduce_dims_%s" % suffix]["sza"]

        # noinspection PyBroadException
        try:
            self.idx_dim_vza = self.L0["dims"].index(self.dim_vza)
        except Exception:
            self.idx_dim_vza = None
            self.vza_reduced = self.L0["reduce_dims_%s" % suffix]["vza"]

    def get_wvl_idx(self, data_wvls, sensor_name=None):
        """
        :param sensor_name:
        :param data_wvls: numpy array with wavelength as used in the data
        :return: numpy array with ints which give the closest indices to the wavelength in data_wvls
        """
        if sensor_name is None:
            return np.array([np.argmin(np.abs(data_wvls - wv)) for wv in self.wvl], dtype=int)
        else:
            return np.array([np.argmin(np.abs(data_wvls - wv)) for wv in self.wvl_sensors[sensor_name]], dtype=int)


# noinspection PyProtectedMember,PyDictCreation,PyUnresolvedReferences
def __minimize__(pt_index, p0, pt_names, data, opt_func, zoom_factor=None, opt_range="full",
                 opt_options=None, update_p0=True, zoom_interpolation_order=1, debug=False,
                 monitor=True, processes=None):

    if not opt_options:
        opt_options = {"maxiter": 50, "disp": False}

    if processes is None:
        processes = np.max([1, int(np.ceil(cpu_count() / 2) - 2)])

    if zoom_factor is None:
        zoom_factor = np.ones(3, dtype=float)
    elif len(zoom_factor) == 1:
        zoom_factor = np.array([zoom_factor, zoom_factor, 1.0], dtype=float)
    elif len(zoom_factor) == 2:
        zoom_factor = np.array([zoom_factor[0], zoom_factor[1], 1.0], dtype=float)
    else:
        raise ValueError("Wrong zoom_factor")

    globs = {}

    globs["__p0__"] = __zm__(p0[:, :, pt_index], zoom_factor, order=zoom_interpolation_order)
    globs["__ff__"] = opt_func
    globs["__opt_options__"] = opt_options
    globs["__data__"] = __zm__(data, zoom_factor, order=zoom_interpolation_order)
    res_shape = list(globs["__data__"].shape[:2]) + [opt_func.n_x]

    globs["__res__"] = SharedNdarray(res_shape, default_value=np.NaN)
    globs["__norm__"] = SharedNdarray(res_shape[:2])
    globs["__meta__"] = SharedNdarray(res_shape[:2] + [data.shape[2]])

    if opt_range == "full":
        rng = list(product(np.arange(0, res_shape[0], 1), np.arange(0, res_shape[1], 1)))
    else:
        funcs = (np.ceil, np.floor, np.ceil)
        opt_range_x = [int(fun(val)) for fun, val in zip(funcs, np.array(opt_range[0]) * zoom_factor[0])]
        opt_range_y = [int(fun(val)) for fun, val in zip(funcs, np.array(opt_range[1]) * zoom_factor[1])]
        rng = list(product(np.arange(*opt_range_x), np.arange(*opt_range_y)))

    if monitor is True:
        with Pool(processes=processes, initializer=initializer, initargs=(globals(), globs,)) as pl:
            result = pl.map_async(__min__, rng)
            p_bar = pyprind.ProgBar(result._number_left, monitor=True, width=130)
            while not result.ready():
                p_bar.cnt = p_bar.max_iter - result._number_left
                p_bar.update()
                p_bar.cnt -= 1
                sleep(1)
    else:
        if debug is True:
            initializer(globals(), globs)
            for rr in rng:
                __min__(rr)
        else:
            with Pool(processes=processes, initializer=initializer, initargs=(globals(), globs,)) as pl:
                pl.map(__min__, rng)

    for ii, (up, dn) in enumerate(zip(opt_func.x_bounds_up, opt_func.x_bounds_dn)):
        globs["__res__"].np[globs["__res__"].np[:, :, ii] > up, ii] = up
        globs["__res__"].np[globs["__res__"].np[:, :, ii] < dn, ii] = dn

    res = __rezoom__(globs["__res__"].np, data.shape, order=zoom_interpolation_order)
    norm = __rezoom__(globs["__norm__"].np, data.shape[:2], order=zoom_interpolation_order)
    meta = __rezoom__(globs["__meta__"].np, data.shape, order=zoom_interpolation_order)

    for ii, (up, dn) in enumerate(zip(opt_func.x_bounds_up, opt_func.x_bounds_dn)):
        res[res[:, :, ii] > up, ii] = up
        res[res[:, :, ii] < dn, ii] = dn

    if update_p0 is True:
        res_to_pt = [list(pt_names).index(dim) for dim in opt_func.jjsc_names if dim in pt_names]
        if opt_range == "full":
            p0[:, :, res_to_pt] = res[:, :, :opt_func.n_atm]
        else:
            slx = slice(*opt_range[0])
            sly = slice(*opt_range[1])
            p0[slx, sly, res_to_pt] = res[slx, sly, :opt_func.n_atm]
    elif update_p0 is False:
        pass
    else:
        res_to_pt = [list(pt_names).index(dim) for dim in globs["__ff__"].jjsc_names if
                     dim in pt_names and dim in update_p0]
        res_id = [ii for ii, dim in enumerate(globs["__ff__"].dim_names) if dim in update_p0]
        print(res_to_pt, res_id)
        if opt_range == "full":
            p0[:, :, res_to_pt] = res[:, :, res_id]
        else:
            slx = slice(*opt_range[0])
            sly = slice(*opt_range[1])
            p0[slx, sly, res_to_pt] = res[slx, sly, res_id]

    del globs["__norm__"]
    del globs["__res__"]
    del globs["__meta__"]

    return res, meta, norm


# noinspection PyUnresolvedReferences
def __min__(ii, debug=False, only_success=False):
    """
    Core function of the optimization process. Optimization is done by looping through all pixels.
    :param ii: row/column index of each enmap pixel
    :param debug:
    :param only_success:
    :return:
    """
    from scipy.optimize import minimize  # import here to avoid static TLS ImportError

    i1, i2 = ii
    if __data__[i1, i2, 0] == 0.0:
        return

    if __opt_options__ is None:
        __res__[i1, i2, :] = __ff__.fo.x_scaled_to_phys(__ff__.x0(p0=__p0__[i1, i2, :], data=__data__[i1, i2, :]))
    else:
        if np.all(np.isfinite(__data__[i1, i2, :])):

            ress_full = [
                minimize(fun=__ff__, x0=__ff__.x0(p0=__p0__[i1, i2, :], data=__data__[i1, i2, :], first_guess=fg),
                         args=(__p0__[i1, i2, :], __data__[i1, i2, :]), jac=True,
                         method='BFGS', options=__opt_options__)
                for fg in [0.06, 0.1]]

            # choose the optimization with the lowest norm value between modeled and measured TOA reflectance
            # => best one
            ress_full = sorted(ress_full, key=lambda k: k['fun'])
            res = ress_full[0]

            if debug is True:
                print(__opt_options__)
                print((__p0__[i1, i2, :], __data__[i1, i2, :]))
                print(__ff__.x0(p0=__p0__[i1, i2, :], data=__data__[i1, i2, :]))
                return res
            else:
                if only_success is True:
                    if res["success"] is True:
                        __res__[i1, i2, :] = __ff__.x_scaled_to_phys(res["x"])
                    else:
                        __res__[i1, i2, :] = np.NaN
                else:
                    # create array containing the optimization result, the norms and the modeled TOA reflectance
                    __res__[i1, i2, :] = __ff__.x_scaled_to_phys(res["x"])

                __norm__[i1, i2] = np.sqrt(res["fun"]) / np.mean(__data__[i1, i2, :])
                __meta__[i1, i2, :] = __ff__(res["x"], __p0__[i1, i2, :], __data__[i1, i2, :], model_output=True)


def __rezoom__(res, data_shape, order=3):
    from scipy.ndimage import zoom  # import here to avoid static TLS ImportError
    sh0, sh1 = np.array(res.shape, dtype=float), np.array(res.shape, dtype=float)
    sh1[:2] = np.array(data_shape)[:2]
    fac = sh1 / sh0
    if np.mean(fac) == 1.0:
        return np.copy(res)
    else:
        return zoom(input=res, zoom=fac, order=order)


def __zm__(data, fac, order=3):
    from scipy.ndimage import zoom  # import here to avoid static TLS ImportError
    if fac is None:
        return data
    elif np.mean(fac) == 1.0:
        return data
    else:
        try:
            return zoom(data, fac, output=data.dtype, order=order)
        except RuntimeError:
            return zoom(np.array(data, dtype=np.float32), fac, output=np.float32, order=order)


# noinspection PyShadowingNames
class FF(object):
    def __init__(self, fo, optimize_dims_atm, weight=None, wvl_sel=slice(None)):
        self.weight = weight
        self.fo = fo
        self.optimize_dims_atm = optimize_dims_atm
        self.n_rho_lin = self.fo.n_rho_lin
        self.n_atm = len(self.optimize_dims_atm)
        self.n_x = self.n_rho_lin + self.n_atm
        self.wvl_sel = wvl_sel

        if not all([dim in self.fo.L0["dims"] for dim in self.optimize_dims_atm]):
            raise ValueError("Missing:", self.optimize_dims_atm, self.fo.L0["dims"])

        self.atm_idx = np.array([idx for dim, idx in zip(self.fo.L0["dims"], self.fo.L0["idx"])], dtype=int)
        self.atm_opt_idx = np.array(
            [idx for dim, idx in zip(self.fo.L0["dims"], self.fo.L0["idx"]) if dim in self.optimize_dims_atm],
            dtype=int)
        self.atm_bgr_idx = np.array(
            [idx for dim, idx in zip(self.fo.L0["dims"], self.fo.L0["idx"]) if dim not in self.optimize_dims_atm],
            dtype=int)

        dim_names = list(optimize_dims_atm) + [self.fo.dim_names[dx] for dx in self.atm_bgr_idx]
        self.dim_names = [dim for dim in self.fo.L0["dims"] if dim in dim_names] + self.n_rho_lin * ["rj"]

        # not all lut parameters are in the jacobean (view directions)
        jjsc = (self.fo.bounds_up - self.fo.bounds_dn) / (self.fo.scale_up - self.fo.scale_dn)
        self.jjsc = [jj for jj, dim in zip(jjsc, self.dim_names) if dim == "rj" or dim in self.fo.SS["dims"]]
        self.jjsc_names = [dim for jj, dim in zip(jjsc, self.dim_names) if dim == "rj" or dim in self.fo.SS["dims"]]

        self.pt = np.zeros(np.max(self.fo.L0["idx"]) + 1 +  # atmospheric indices
                           self.fo.n_rho_lin,  # surface indices
                           dtype=float)
        self.pt_bounds_up = np.zeros(len(self.pt))
        self.pt_bounds_dn = np.zeros(len(self.pt))
        for ii, idx in enumerate(self.fo.L0["idx"]):
            self.pt_bounds_up[idx] = self.fo.bounds_up[ii]
            self.pt_bounds_dn[idx] = self.fo.bounds_dn[ii]

        try:
            self.pt_bounds_up[-self.n_rho_lin:] = self.fo.rj_to_rho_J.bounds_up[:]
        except AttributeError:
            self.pt_bounds_up[-self.n_rho_lin:] = 1.0
        try:
            self.pt_bounds_dn[-self.n_rho_lin:] = self.fo.rj_to_rho_J.bounds_dn[:]
        except AttributeError:
            self.pt_bounds_dn[-self.n_rho_lin:] = 0.0

        self.n_atm_all = len(self.atm_idx)
        self.n_x_all = self.n_rho_lin + self.n_atm_all

        self.x_bounds_up = np.zeros(self.n_x)
        self.x_bounds_dn = np.zeros(self.n_x)
        self.x_bounds_up[:self.n_atm] = self.pt_bounds_up[self.atm_opt_idx]
        self.x_bounds_dn[:self.n_atm] = self.pt_bounds_dn[self.atm_opt_idx]

        try:
            self.x_bounds_up[self.n_atm:] = self.fo.rj_to_rho_J.bounds_up
        except AttributeError:
            self.x_bounds_up[self.n_atm:] = 1.0

        try:
            self.x_bounds_dn[self.n_atm:] = self.fo.rj_to_rho_J.bounds_dn
        except AttributeError:
            self.x_bounds_dn[self.n_atm:] = 0.0

        self.jac_sel = np.array([False] * len(self.jjsc))
        for ii, dim in enumerate(self.jjsc_names):
            if dim in self.optimize_dims_atm or dim == "rj":
                self.jac_sel[ii] = True

    @staticmethod
    def apply_bounds(xii, bounds_up, bounds_dn):
        nn = xii.shape[0]
        for ii in range(nn):
            if xii[ii] >= bounds_up[ii]:
                xii[ii] = bounds_up[ii]
            if xii[ii] < bounds_dn[ii]:
                xii[ii] = bounds_dn[ii]

    def __norm__(self, aa, bb):
        if self.weight is None:
            return (aa - bb) ** 2
        else:
            return self.weight * (aa - bb) ** 2

    def __d_bb_norm__(self, aa, bb):
        if self.weight is None:
            return -2 * (aa - bb)
        else:
            return -2 * (aa - bb) * self.weight

    def x_phys_to_scaled(self, xx):
        return (xx - self.x_bounds_dn) / (self.x_bounds_up - self.x_bounds_dn)

    def x_scaled_to_phys(self, xx):
        return (self.x_bounds_up - self.x_bounds_dn) * xx + self.x_bounds_dn

    def x0(self, p0=None, data=None, first_guess=None):
        """
        Estimation of the first guess solution x0.
        x0 contains a first guess solution of parameter concentration as well as estimated reflectance values at
        the two continuum levels of the chosen absorption feature.
        :param p0:
        :param data:
        :param first_guess:
        :return:
        """
        xx = np.ones(self.n_x)  # initial first guess

        if p0 is not None and data is not None:
            self.pt[self.atm_opt_idx] = p0[self.atm_opt_idx]
            self.pt[self.atm_bgr_idx] = p0[self.atm_bgr_idx]
            self.apply_bounds(self.pt, self.pt_bounds_up, self.pt_bounds_dn)

            xx[-self.n_rho_lin:] = self.fo.rho_to_rj(
                self.fo.reflectance_boa(pt=self.pt, toa_reflectance=data))
            # copy first guess for atm
            xx[:self.n_atm] = p0[self.atm_opt_idx]

            self.apply_bounds(xx, self.x_bounds_up, self.x_bounds_dn)

            # values are scaled => (value - lower bound) / (upper bound - lower bound)
            xx = self.x_phys_to_scaled(xx)
            if first_guess is not None:
                xx[:self.n_atm] = first_guess

        return xx

    def __call__(self, xx, pt, dt, xx_is_scaled=True, model_output=False):

        if xx_is_scaled:  # scale back
            xx = self.x_scaled_to_phys(xx)

        self.pt[self.atm_opt_idx] = xx[:self.n_atm]  # copy x to pt
        self.pt[self.atm_bgr_idx] = pt[self.atm_bgr_idx]  # copy bg data
        self.pt[-self.n_rho_lin:] = xx[-self.fo.n_rho_lin:]  # copy surface data
        self.apply_bounds(self.pt, self.pt_bounds_up, self.pt_bounds_dn)

        ff, jj = self.fo.reflectance_toa_j(self.pt)

        if model_output is True:
            return ff
        else:
            f = (np.sum(self.__norm__(dt[self.wvl_sel], ff[self.wvl_sel])))
            j = (np.sum(jj[:, self.wvl_sel] * self.__d_bb_norm__(dt[self.wvl_sel], ff[self.wvl_sel]), axis=1))
            if xx_is_scaled:
                j = j * self.jjsc

            n = float(len(dt))
            return f / n, j[self.jac_sel] / n


# noinspection PyDictCreation
if __name__ == "__main__":

    solar = SolarIrradiance(path_thuillier="./databases/solar_irradiance/Solar_irradiance_Thuillier_2002.xls",
                            path_fontenla="./databases/solar_irradiance/SUNp1fontenla.asc",
                            path_earth_sun_distance='./databases/solar_distance/Earth_Sun_distances_per_day_edited.csv'
                            )

    instruments = {
        "sat_1": sat(wvl_inst=np.arange(450, 650, 20.0), wvl_rsp=np.arange(250, 950, 0.2), sigma=5.0, solar=solar),
        "sat_2": sat(wvl_inst=np.arange(1450, 1650, 2.0), wvl_rsp=np.arange(1250, 2050, 0.2), sigma=5.0, solar=solar),
        "EnMap_Gauss": sat(wvl_inst=np.arange(450, 2450, 5.0), wvl_rsp=np.arange(400, 2540, 0.1), sigma=7.0,
                           solar=solar),
        "MS": sat(wvl_inst=np.arange(450, 2450, 25.0), wvl_rsp=np.arange(400, 2540, 0.1), sigma=15.0, solar=solar),
        "MS2": sat(wvl_inst=np.arange(450, 2450, 125.0), wvl_rsp=np.arange(400, 2540, 0.1), sigma=45.0, solar=solar)}

    wvl_enmap, sigmas_enmap = (lambda x: (x[:, 0], x[:, 1]))(np.loadtxt("./databases/SRF_EnMap.txt"))
    instruments["EnMap"] = sat(wvl_inst=wvl_enmap, wvl_rsp=np.arange(wvl_enmap[0], wvl_enmap[-1], 0.2),
                               sigma=sigmas_enmap, solar=solar)

    atm_tables_fn = "./linear_atm_functions_ncwv_3_npre_3_ncoz_3_ntmp_4_wvl_350.0_2550.0_1.00_pca.h5"
    self = RtFo(atm_tables_fn=atm_tables_fn,
                n_pcs=15,
                hash_formats={'spr': '%.0f,', 'coz': '%.0f,', 'cwv': '%.0f,', 'tmp': '%0f,', 'tau_a': '%.2f,',
                              'vza': '%.0f,'},
                slices={"tmp": slice(0, 4, 1)},
                dim_scat=["tau_a"],
                table_path="/table_aerosol/type_1",
                only_toa=False,
                sensors=instruments,
                sensor_interpolation_reference=["sensor", "pca", "error"][0])

    fig = figure(figsize=(10, 7))
    self.set_sensor()
    rho_pca = -1 * (self.wvl_pca - self.wvl_pca[0]) ** 2 / 10 ** 7 + 0.5
    pt = np.array([1015.0, 350., 1.5, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0])
    plot(self.wvl, self.reflectance_toa(pt, rho_pca), "0.7")

    for sat, col, ls in zip(['EnMap_Gauss', 'EnMap'], ["r", "c", "c", "y", "b", "m"],
                            [".", ".", ".", "-", ".", ".", ".", "."]):
        self.set_sensor(sat)
        plot(self.wvl, self.reflectance_toa(pt, np.interp(x=self.wvl, xp=self.wvl_pca, fp=rho_pca)), linestyle=ls,
             color=col, markersize=3, marker="<")
    show()

    print("EEooFF")
