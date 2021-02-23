# -*- coding: utf-8 -*-
"""Base module of SICOR, contains most IO and data handling code."""
import json
import logging
from itertools import product
from multiprocessing import Pool
from os import makedirs, rename, sep
from os.path import abspath, dirname, basename, join
from shutil import copy
from time import sleep, time
from types import MethodType
from types import SimpleNamespace
from xml.dom.minidom import parseString
import gdal
import mpld3
import PIL
import numpy as np
from dicttoxml import dicttoxml
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime, timedelta
import sys

from .Tools import inpaint, fl, cl, itt2d, nanmean_filter
from .Tools import write_raster_gdal
from sicor.ECMWF import ECMWF_variable


def get_ecmwf_data(variable, image, options, logger=None):
    """
    Wrapper for sicor.ECMWF.ECMWF_variable. For a given observation date, go back in time day by day
    in ECMWF database (given in options["ECMWF"]['path_db']) until a valid file is found. This time is set in
    options["ECMWF"]["max_delta_day"]. Adjust ECMWF step according to the days needed to go back in time until data
    was available.

    :param variable: Name of ECMWF variable, needs to be present in database root directory
    :param image:    object derived from sicor.sensors.RSImage
    :param options:  dictionary with options.
                     Minimum is: {"ECMWF": {"path_db": [path to ecmwf db], "max_delta_day": [number of days],
                     "target_resolution": 20}}
    :param logger:   None or instance of logging
    :return:         numpy array with interpolated variable at given [target_resolution] for [variable] and [image] geo
                     position
    """
    logger = logger or logging.getLogger(__name__)
    ecmwf_xi = image.ecmwf_xi()
    sensing_date = image.metadata['SENSING_TIME'].date()
    delta_day = 0
    for delta_day in range(0, options["ECMWF"]["max_delta_day"]):
        try:
            if delta_day < 2:
                logger.info("Look %i day back in time to find suitable ECMWF data." % delta_day)
            else:
                logger.info("Look %i days back in time to find suitable ECMWF data." % delta_day)
            return ECMWF_variable(variable=variable, path_db=options["ECMWF"]['path_db'], delta_day=delta_day,
                                  var_date=sensing_date - timedelta(days=delta_day))(
                shape=image.spatial_sampling_shapes[options["ECMWF"]["target_resolution"]],
                lons=ecmwf_xi["lons"], lats=ecmwf_xi["lats"],
                order=ecmwf_xi["order"],
                step=ecmwf_xi["step"] + delta_day * 24)
        except FileNotFoundError:
            pass
    raise FileNotFoundError("ECMWF data not found after looking back %i days." % delta_day)


def conv(scale, dtype):
    """Function to create custom data conversion functions
    :param scale: Scaling factor, scalar value
    :param dtype: Numpy dtype of output
    :returns: Functions which applys this scaling to numpy arrays
    """
    def conv_scale(x, nodata_value=None):
        """Generic linear scaling function."""
        xx = np.array(x * scale, dtype=dtype)
        if nodata_value is not None:
            xx[np.isnan(x)] = nodata_value
        return xx

    return conv_scale


# GMS compatibilty layer
# noinspection PyDefaultArgument,PyArgumentList
class StrippedInstance(object):
    """Generic stripped down version of any object - used to debug interfaces with GeoMultiSens."""
    def __init__(self, inp, cls, attributes=[], metadata_keys=[], methods=[], logger=None, verbose=False):
        for at in attributes:
            try:
                setattr(self, at, getattr(inp, at))
                if verbose is True:
                    logger.info("%s:%s" % (at, StrippedInstance.pp(getattr(inp, at))))
            except AttributeError:
                logger = logger or logging.getLogger(__name__)
                logger.warning("Attribute: %s is missing -> continue." % str(at))

        for mt in methods:
            setattr(self, mt, MethodType(getattr(o=cls, name=mt), self))

        self.metadata = {k: v for k, v in inp.metadata.items() if k in metadata_keys}
        if verbose is True:
            logger.info("Metadata:")
            for key, value in self.metadata.items():
                logger.info("%s:%s" % (key, StrippedInstance.pp(value)))

    @staticmethod
    def pp(inp):
        """Create sane description strings including numpy arrays."""
        if isinstance(inp, dict):
            ss = "{\n" + ",\n".join(["%s:%s" % (key, StrippedInstance.pp(value))
                                     for key, value in inp.items()]) + "\n}"
            return ss

        if isinstance(inp, np.ndarray):
            return "ndarray(dtype=%s)" % str(inp.dtype)
        else:
            return str(inp)


# noinspection PyShadowingNames
def pretty_print(obj):
    """
    Pretty print object
    :param obj: Any python object.
    """

    def shr(st):
        """
        :param st: string
        :return: shortened string
        """
        if len(st) > 40:
            return st[0:20] + " [..] " + st[-20:]
        else:
            return st

    # noinspection PyShadowingNames
    def __dc__(ob, nsep):
        for k, v in ob.items():
            if isinstance(v, dict):
                if isinstance(v, np.ndarray):
                    print("%s key:%s, value_type:%s, shape:%s, dtype:%s repr: %s" % (
                        nsep * sep, k, type(v), str(v.shape), str(v.dtype),
                        shr(str(v).replace('\n', ' ').replace("  ", "").strip())))
                else:
                    print("%s key:%s, value_type:%s, repr: %s" % (
                        nsep * sep, k, type(v), shr(str(v).replace('\n', ' ').replace("  ", "").strip())))
            else:
                print("%s key:%s" % (nsep * sep, k))
                __dc__(v, nsep + 1)

    sep = "___"
    for name, ob in obj.__dict__.items():
        if isinstance(ob, dict):
            print("%s attribute: %s, type:%s" % (sep, name, type(ob)))
            __dc__(ob, 2)
        if hasattr(ob, "__dict__"):
            print("%s attribute: %s, type:%s" % (sep, name, type(ob)))
            __dc__(ob.__dict__, 2)
        else:
            print("%s attribute: %s, type:%s" % (sep, name, type(ob)))


def slp2spr(slp, t, h, dt_dh=-0.006, m=0.02896, r=8.314, g=9.807):
    """
    Convert Sea level pressure to given height using barometric formula and linear temperature profile:
    T = T0 + dTdH * h, in general: dTdH is negative.

    :param r:
    :param slp: seal level pressure
    :param m: molar weight of air in kg / mol
    :param g: gravitation in m/ s^2
    :param t: temperature at height h
    :param h: height in m
    :param dt_dh: temperature height gradient
    :return: pressure in same units as slp
    """
    return slp * (1.0 + (dt_dh * h) / (t - dt_dh * h)) ** (m * g / r / (-1 * dt_dh))


def barometric_formula(h, p0=1013.0, t0=288.15):
    """
    Surface pressure for standard conditions
    :param t0: Surface temperature in K
    :param h: height in m
    :param p0: surface pressure
    :return: surface pressure in units of p0
    """
    return p0 * (1.0 - 0.0065 * h / t0) ** 5.244


def include_missing_spatial_samplings(data, samplings, order=0, base_key=None):
    """ Add data of additional spatial samplings to data dict

    :param data: dict with spatial_sampling:data
    :param samplings: additional spatial samplings to be included in data
    :param order: interpolation order
    :param base_key: if None, first key:value pairs in data is used, otherwise this one
    :return:
    """
    from scipy.ndimage import zoom  # import here avoids static TLS ImportError

    if base_key is None:
        base_spatial_sampling = list(data.keys())[0]
    else:
        assert base_key in data
        base_spatial_sampling = base_key
    base_dtype = data[base_spatial_sampling].dtype
    base_data = np.array(data[base_spatial_sampling], dtype=float)

    for key in samplings:
        if key not in data:
            zoom_fac = base_spatial_sampling / key
            data[key] = np.array(zoom(base_data, zoom=zoom_fac, order=order), dtype=base_dtype)


def prepare_s2_wv(n_smpl, bands, fo, rho_bounds):
    """ Prepare unstructured table for interpolation of water vapour.
    :param rho_bounds:
    :param bands:
    :param n_smpl:
    :param fo: instance of RtFo
    :returns: dictionary {"points":points,"values":values} to be directly used by griddata
    """

    n_params = np.prod(list(n_smpl.values()))
    points = np.zeros((n_params, len(["spr", "tau_a"] + bands)), dtype=float)
    values = np.zeros(n_params, dtype=float)  # cwv

    params = product(*([np.linspace(rho_bounds[0], rho_bounds[1], n_smpl["rho"])] +
                       [np.linspace(np.min(fo.dims[dim]), np.max(fo.dims[dim]), n_smpl[dim])
                        for dim in ["cwv", "spr", "tau_a"]]))

    pt = np.zeros(np.max(fo.L0["idx"] + 1), dtype=float)

    ids = {dim: fo.L0["idx"][fo.L0["dims"].index(dim)] for dim in ["cwv", "spr", "tau_a"]}

    for ii, (rho, cwv, spr, tau_a) in enumerate(params):
        pt[ids["cwv"]] = cwv
        pt[ids["spr"]] = spr
        pt[ids["tau_a"]] = tau_a

        b8a, b09 = fo.reflectance_toa(pt, rho)
        points[ii, :] = [spr, tau_a, b8a, b09]
        values[ii] = cwv

    assert np.sum(np.isnan(points)) == 0
    assert np.sum(np.isnan(values)) == 0

    return {"points": points, "values": values}


def get_egl_lut(fo, spr_lim, dim_spr, dim_wv):
    """
    Interpolation of solar downward irradiance for a given atmospheric state to build a small cwv and spr LUT.
    :param fo: Forward operator to use
    :param spr_lim: Lower and upper limit of spr in given data.
    :param dim_spr: Number of spr values.
    :param dim_wv: Number of cwv values.
    :return: E_DN LUT for different spr and cwv.
    """
    pt = np.zeros(np.max(fo.L0["idx"] + 1), dtype=float)
    ids = {dim: fo.L0["idx"][fo.L0["dims"].index(dim)] for dim in ["cwv", "spr"]}
    egl_lut = np.zeros((dim_spr, dim_wv, len(fo.wvl)))

    for i in range(0, dim_spr):
        for j in range(0, dim_wv):
            pt[ids["spr"]] = spr_lim[i]
            pt[ids["cwv"]] = fo.dims["cwv"][j]
            egl_lut[i, j, :] = fo.ee(pt)

    return egl_lut


def wv(fo, s2img, clear_areas, s2spr, s2tau, cloud_fraction, nanmean, sigma, rho_bounds,
       bands, target_resolution, int_order, n_smpl, n_std, logger=None, **kwargs):
    """
    Generic two-band water vapor retrieval

    :param fo:                forward operator to use
    :param s2img:             RSImage derived at-sensor reflectance
    :param clear_areas:       dict of {spatial_sampling:clear_area_map}
    :param s2spr:             dict {spatial_sampling:surface_pressure_map}
    :param s2tau:             dict {spatial_sampling:aerosol_optical_thickness_map}
    :param cloud_fraction:    fraction of cloud covered image pixels
    :param nanmean:           TODO
    :param sigma:             TODO
    :param rho_bounds:        lower und upper reflectance bounds
    :param bands:             TODO
    :param target_resolution: value of spatial sampling in meter to retrieve the product
    :param int_order:         order of polynomial interpolation for output product
    :param n_smpl:            TODO
    :param n_std:             TODO
    :param logger:            None or logging instance
    :returns:                 retrieved water vapor map.
    """
    from scipy.interpolate import griddata  # import here avoids static TLS ImportError

    logger = logger or logging.getLogger(__name__)
    # prep data
    data = s2img.image_subsample(channels=bands,
                                 target_resolution=target_resolution,
                                 order=int_order)

    good_data = np.logical_and(np.isfinite(data[:, :, 0]), np.isfinite(data[:, :, 1]))

    # collect data for water vapour retrieval
    mask = np.logical_and(good_data, clear_areas[target_resolution])
    xi = np.squeeze(np.dstack((s2spr[target_resolution][mask],  # spr
                               s2tau[target_resolution][mask],  # tau aerosol
                               data[mask, 0],  # B8A
                               data[mask, 1],  # B09
                               )))
    # create field for water vapor
    cwv = np.empty(mask.shape)
    cwv[:, :] = np.nan
    try:
        cwv[mask] = griddata(xi=xi, fill_value=np.NAN, method='linear', **prepare_s2_wv(
            n_smpl=n_smpl, bands=bands, fo=fo, rho_bounds=rho_bounds))
    except RuntimeError:
        logger.warning("Water vapor retrieval based on initial unstructured grid points failed, "
                       "most likely due to high cloud fraction of %.3f." % cloud_fraction)
        logger.info("Try to reduce unstructured grid points to enable a successful water vapor retrieval. "
                    "This may take a while.")
        grid = prepare_s2_wv(n_smpl=n_smpl, bands=bands, fo=fo, rho_bounds=rho_bounds)
        points = grid["points"]
        values = grid["values"]
        for ii in np.arange(0, 1.01, 0.01):
            threshold = points[:, 2].min() + ii
            try:
                cwv[mask] = griddata(xi=xi, fill_value=np.NAN, method='linear', points=points[points[:, 2] > threshold],
                                     values=values[points[:, 2] > threshold])
                logger.info("Water vapor retrieval succeeded based on reduced unstructured grid points.")
                break
            except RuntimeError:
                if ii == 1.0:
                    logger.warning("Water vapor retrieval failed even based on reduced unstructured grid points. "
                                   "Exit AC due to too high cloud cover of input image.")
                    logger.info("EEooFF")
                    sys.exit()
                else:
                    pass

    # filter water vapor retrieval results
    cwv_mean, cwv_std = np.nanmean(cwv), np.nanstd(cwv)
    with np.errstate(invalid='ignore'):
        # cwv might contains nan's so comparison might trigger a warning, but the comparison with nan
        # results in False which is just fine here
        cwv_bad = np.logical_or(cwv > cwv_mean + n_std * cwv_std,
                                cwv < cwv_mean - n_std * cwv_std)
    cwv[cwv_bad] = np.nan

    cwv_polished = inpaint(array=nanmean_filter(cwv, nanmean),
                           mask=np.logical_not(s2img.nodata[target_resolution]),
                           fill_remaining="broom",
                           post_processing="gaussian_filter",
                           sigma=sigma,
                           logger=logger)

    # make for all spatial samplings
    s2cwv = {target_resolution: np.array(cwv_polished, dtype=np.float16)}
    include_missing_spatial_samplings(data=s2cwv, samplings=s2img.metadata["spatial_samplings"].keys(), order=0)
    return s2cwv


def wv_band_ratio(fo, s2img, clear_areas, s2spr, nanmean, sigma,
                  bands, target_resolution, int_order, n_std, logger=None, **kwargs):
    """
    Two-band water vapor retrieval based on the logarithm of the water vapor transmittance at 940 nm.
    :param fo: Forward operator to use
    :param s2img: RSImage derived at-sensor reflectance
    :param clear_areas: Dict of {spatial_sampling:clear_area_map}
    :param s2spr: Dict {spatial_sampling:surface_pressure_map}
    :param nanmean:
    :param sigma:
    :param bands:
    :param target_resolution: Value of spatial sampling in meter to retrieve the product
    :param int_order: Order of polynomial interpolation for output product
    :param n_std:
    :param logger: None or logging instance
    :return: Retrieved water vapor map.
    """

    data = s2img.image_subsample(channels=bands,
                                 target_resolution=target_resolution,
                                 order=int_order)
    good_data = np.logical_and(np.isfinite(data[:, :, 0]), np.isfinite(data[:, :, 1]))
    mask = np.logical_and(good_data, clear_areas[target_resolution])
    cnt_land = len(np.ndarray.flatten(data[mask, 0]))
    num_bd = data.shape[2]

    toa_sub = np.zeros((cnt_land, num_bd))
    for i in range(0, num_bd):
        toa_sub[:, i] = data[mask, i]
    cnt_land = len(toa_sub[:, 0])

    spr_lim = [np.min(s2spr[target_resolution]), np.max(s2spr[target_resolution])]
    dim_spr = len(spr_lim)
    dim_wv = len(fo.dims["cwv"])

    egl_lut = get_egl_lut(fo=fo, spr_lim=spr_lim, dim_spr=dim_spr, dim_wv=dim_wv)

    alog_rat_wv_lut = np.zeros((dim_spr, dim_wv))
    rat_wv_lut = egl_lut[:, :, 1] / egl_lut[:, :, 0]
    alog_rat_wv_lut[:, :] = np.log(rat_wv_lut)

    cf_arr = np.zeros((3, dim_spr))
    for ind_spr in range(0, dim_spr):
        cf_arr[:, ind_spr] = np.polyfit(alog_rat_wv_lut[ind_spr, :], fo.dims["cwv"], 2)

    alog_rat_wv_img = np.log(toa_sub[:, 1] / toa_sub[:, 0])
    wh = np.isinf(alog_rat_wv_img)
    cnt = np.count_nonzero(wh)
    if cnt > 0:
        alog_rat_wv_img[wh] = 1.

    wv_arr = np.empty(cnt_land)
    wv_arr[:] = np.nan

    if spr_lim[1] != spr_lim[0]:
        spr_fac = (s2spr[target_resolution] - spr_lim[0]) / (spr_lim[1] - spr_lim[0])
        spr_fac = np.ndarray.flatten(spr_fac)
    else:
        spr_fac = np.zeros(cnt_land)

    for ind in range(0, cnt_land):
        spr_fac_pix = spr_fac[ind]
        cf_int = (1. - spr_fac_pix) * cf_arr[:, 0] + spr_fac_pix * cf_arr[:, 1]
        wv = cf_int[0] + alog_rat_wv_img[ind] * cf_int[1] + alog_rat_wv_img[ind] * alog_rat_wv_img[ind] * cf_int[2]
        wv_arr[ind] = wv

    wv_img = np.empty(mask.shape)
    wv_img[:, :] = np.nan
    wv_img[mask] = wv_arr

    cwv_mean, cwv_std = np.nanmean(wv_img), np.nanstd(wv_img)
    with np.errstate(invalid='ignore'):
        cwv_bad = np.logical_or(wv_img > cwv_mean + n_std * cwv_std,
                                wv_img < cwv_mean - n_std * cwv_std)
    wv_img[cwv_bad] = np.nan

    cwv_polished = inpaint(array=nanmean_filter(wv_img, nanmean),
                           mask=np.logical_not(s2img.nodata[target_resolution]),
                           fill_remaining="broom",
                           post_processing="gaussian_filter",
                           sigma=sigma,
                           logger=logger)

    s2cwv = {target_resolution: np.array(cwv_polished, dtype=np.float16)}
    include_missing_spatial_samplings(data=s2cwv, samplings=s2img.metadata["spatial_samplings"].keys(), order=0)
    return s2cwv


def nan_gaussian_filter(data, sigma):
    """A gaussian filter that works on array with NaN values."""
    from scipy.ndimage import gaussian_filter  # import here avoids static TLS ImportError

    vv = data.copy()
    vv[data != data] = 0
    vv_g = gaussian_filter(vv, sigma=sigma)

    ww = 0 * data.copy() + 1
    ww[data != data] = 0
    ww_g = gaussian_filter(ww, sigma=sigma)

    zz = vv_g / ww_g
    zz[np.isnan(data)] = np.NaN

    return zz


def __mkd__(min_v, max_v, min_fo, max_fo, dd):
    """
    if min - max < dd, then shift intervall such that is withon _fo bounds
    :param min_v:
    :param max_v:
    :param min_fo:
    :param max_fo:
    :param dd:
    :return: min*,max*
    """
    if max_v - min_v < dd:
        min_v -= dd / 2
        max_v += dd / 2
        if min_v < min_fo:
            min_v = min_fo
        if max_v >= max_fo:
            max_v = max_fo
    return min_v, max_v


def quality_check_data_ac_vs_clear_areas(s2img, logger=None):
    """
    Use s2img.data_ac and s2img.clear_areas for a quality check. Creates a copy of s2img.clear_areas and updates areas
    with False which are orignally True but data_ac is none. This means that these areas were not successfully processed
    with the ac algorithm

    :param s2img: Should be S2MSI.S2Image instance. At least s2img.data_ac and s2img.clear_areas are neeeed
    :param logger: logger instance
    :return: clear_areas, dictionary with {[spatial sampling]:[boolean array]}
    """
    logger = logger or logging.getLogger(__name__)
    # make copy of clear_areas dictionary
    clear_areas = {k: np.copy(v) for k, v in s2img.clear_areas.items()}
    # loop over all bands for test
    for band in sorted(s2img.data_ac.keys()):
        ss = s2img.band_spatial_sampling[band]
        # where data_ac is NaN but clear_area == True -> additional area where algo failed
        additionally_bad_areas = np.logical_and(np.isnan(s2img.data_ac[band]), clear_areas[ss])
        n_additionally_bad_areas = s2img.data_ac[band][additionally_bad_areas].shape[0]
        if n_additionally_bad_areas > 0:
            logger.info(
                "Band: %s: %s pixels are not processed -> update product mask for affected spatial sampling." % (
                    band, n_additionally_bad_areas))
            clear_areas[ss][additionally_bad_areas] = False
        else:
            logger.info("Band: %s: All clear data processed." % band)
    return clear_areas


def prepare_s2_ac(s2spr, s2cwv, s2tau, clear_areas,
                  n_smpl, bands, fo, target_resolution, parameter_bounds,
                  logger=None, **kwarg):
    """Generate needed input for atmospheric correction."""
    logger = logger or logging.getLogger(__name__)

    n_params = np.prod(list(n_smpl.values()))
    points = np.zeros((n_params, len(n_smpl.keys())), dtype=float)

    rfls = np.zeros((n_params, len(bands)), dtype=float)
    rhos = np.zeros(n_params, dtype=float)

    spr_min_fo, spr_max_fo = np.min(fo.dims["spr"]), np.max(fo.dims["spr"])
    cwv_min_fo, cwv_max_fo = np.min(fo.dims["cwv"]), np.max(fo.dims["cwv"])
    tau_min_fo, tau_max_fo = np.min(fo.dims["tau_a"]), np.max(fo.dims["tau_a"])
    tr = target_resolution
    if parameter_bounds == "image":
        # spr
        spr_min_img = fl(np.nanmin(s2spr[tr][clear_areas[tr]]), 0)
        spr_max_img = cl(np.nanmax(s2spr[tr][clear_areas[tr]]), 0)
        spr_min, spr_max = __mkd__(max(spr_min_img, spr_min_fo), min(spr_max_img, spr_max_fo), spr_min_fo, spr_max_fo,
                                   1.0)
        # cwv
        cwv_min_img = fl(np.nanmin(s2cwv[tr][clear_areas[tr]]), 0)
        cwv_max_img = cl(np.nanmax(s2cwv[tr][clear_areas[tr]]), 0)
        cwv_min, cwv_max = __mkd__(max(cwv_min_img, cwv_min_fo), min(cwv_max_img, cwv_max_fo), cwv_min_fo, cwv_max_fo,
                                   1.0)
        # tau_a
        tau_min_img = fl(np.nanmin(s2tau[tr][clear_areas[tr]]), 1)
        tau_max_img = cl(np.nanmax(s2tau[tr][clear_areas[tr]]), 1)
        tau_min, tau_max = __mkd__(max(tau_min_img, tau_min_fo), min(tau_max_img, tau_max_fo), tau_min_fo, tau_max_fo,
                                   0.1)
    elif parameter_bounds == "full":
        pass
    else:
        raise ValueError("!")

    logger.info("spr bounds: %.1f<->%.1f" % (spr_min, spr_max))
    logger.info("cwv bounds: %.2f<->%.2f" % (cwv_min, cwv_max))
    logger.info("tau bounds: %.2f<->%.2f" % (tau_min, tau_max))

    params = product(*([np.hstack((np.linspace(0.0, 1.0, n_smpl["rho"] - 2), np.linspace(1.0, 3.0, 3)[1:])),  # rho
                        np.linspace(spr_min, spr_max, n_smpl["spr"]),  # spr
                        np.linspace(cwv_min, cwv_max, n_smpl["cwv"]),  # cwv
                        np.linspace(tau_min, tau_max, n_smpl["tau_a"]),  # tau_a
                        ]))

    pt = np.zeros(np.max(fo.L0["idx"] + 1), dtype=float)
    ids = {dim: fo.L0["idx"][fo.L0["dims"].index(dim)] for dim in ["spr", "cwv", "tau_a"]}

    for ii, (rho, spr, cwv, tau_a) in enumerate(params):
        pt[ids["spr"]] = spr
        pt[ids["cwv"]] = cwv
        pt[ids["tau_a"]] = tau_a

        points[ii, :] = [spr, cwv, tau_a, 0.0]
        rhos[ii] = rho

        rfls[ii, :] = fo.reflectance_toa(pt, rho)

    return points, rhos, rfls


def ac_interpolation(iband, band, s2img, s2spr, s2cwv, s2tau, clear_areas, points, rhos, rfls, max_pixel_processing,
                     reduce_lut=True):
    """Atmospheric correction based on interpolation in unstructured grid."""
    from scipy.interpolate import griddata  # import here avoids static TLS ImportError

    ss = s2img.band_spatial_sampling[band]
    points[:, -1] = rfls[:, iband]

    data_ac = np.empty(s2img.data[band].shape, dtype=np.float32)
    data_ac[:] = np.nan

    dd = max(1, int(np.sqrt(np.floor(np.prod(data_ac.shape) / max_pixel_processing))))
    for sx, sy in itt2d(shape=data_ac.shape, dd=dd):
        mask = np.logical_and(np.isfinite(s2img.data[band][sx, sy]),
                              clear_areas[s2img.band_spatial_sampling[band]][sx, sy])
        xi = np.squeeze(np.dstack((s2spr[ss][sx, sy][mask],
                                   s2cwv[ss][sx, sy][mask],
                                   s2tau[ss][sx, sy][mask],
                                   s2img.data[band][sx, sy][mask],
                                   )))
        if xi.shape[0] > 0:

            if reduce_lut is False:
                res = griddata(points=points, values=rhos, xi=xi)  # old version
            else:
                try:
                    x_min, x_max = np.min(xi[:, -1]), np.max(xi[:, -1])
                    r_min, r_max = (lambda x: (x[0], x[-1]))(
                        rhos[np.logical_and(x_min <= points[:, -1], points[:, -1] <= x_max)])

                    r_min, r_max = np.max(rhos[rhos < r_min]), np.min(rhos[rhos > r_max])
                    sel = np.logical_and(r_min <= rhos, rhos <= r_max)
                    points_sel = points[sel, :]
                    values_sel = rhos[sel]
                    for ii in range(points_sel.shape[0]):
                        index = points_sel.shape[0] - ii
                        try:
                            res = griddata(points=points_sel[:index, :], values=values_sel[:index], xi=xi)
                            break
                        except RuntimeError:
                            pass
                except (ValueError, IndexError):
                    for ii in range(points.shape[0]):
                        index = points.shape[0] - ii
                        try:
                            res = griddata(points=points[:index, :], values=rhos[:index], xi=xi)  # old version
                            break
                        except RuntimeError:
                            pass

            res[res == 0.0] = np.nan
            data_ac[sx, sy][mask] = res
    return data_ac


def get_stats(img, stat, dd):
    """Collect some statistical metrics for data in img.data and img.data_ac."""
    return {band: (float(stat(img.data[band][img.clear_areas[img.band_spatial_sampling[band]]][::dd])),
                   float(stat(img.data_ac[band][img.clear_areas[img.band_spatial_sampling[band]]][::dd])),
                   float(stat(img.data_errors[band][img.clear_areas[img.band_spatial_sampling[band]]][::dd]))
                   if img.data_errors is not None else float(-1.0))
            for band in img.data_ac.keys()}


# noinspection PyDefaultArgument,PyShadowingNames
class IO(object):
    """SICOR Input / Output handler."""
    @staticmethod
    def rename_tmp_product(outputs, run_suffix, logger=None):
        logger = logger or logging.getLogger(__name__)
        if run_suffix != "":
            logger.info("run_suffix=%s -> renaming directory" % run_suffix)
            for fn in [opts["fn"] for opts in outputs if opts["type"] == "L2A" and "fn" in opts]:
                dst = fn.split(run_suffix)[0]
                logger.info("Rename: %s -> %s" % (fn, dst))
                rename(src=fn, dst=dst)

    @staticmethod
    def wait_jobs_dict(jobs, logger=None, sleep_interval=1.0, max_time_minutes=20):
        """Wait until all jobs un jobs are done. Print status if requested."""
        logger = logger or logging.getLogger(__name__)
        t0 = time()
        while len(jobs) > 0:
            jobs_done = {fn: job for fn, job in jobs.items() if job.ready() is True}
            jobs_open = {fn: job for fn, job in jobs.items() if fn not in jobs_done}
            for fn in jobs_done:
                logger.info(fn)
            jobs = jobs_open
            sleep(sleep_interval)
            if (time() - t0) / 60.0 > max_time_minutes:
                raise ValueError

    @staticmethod
    def and_and_check_output_fns(options, logger=None, create_output_dirs=True, run_suffix=True):
        """Check output path in options for existence, create if needed."""
        logger = logger or logging.getLogger(__name__)

        gp = [pp for pp in options["S2Image"]["granule_path"].split(sep) if pp != '']
        suffix = ".p_%s" % datetime.now().strftime("%Y%m%d_%H:%M:%S") if run_suffix is True else ""

        l2a_product_name = gp[-1].replace("L1C", "L2A")
        l2a_rel_path = join(gp[-3].replace("MSIL1C", "MSIL2A").replace("PDMC", "GFZ"), "GRANULE",
                            l2a_product_name + suffix)

        for opts in options["output"]:
            if opts["type"] == "metadata":
                dir_inp = abspath(options["S2Image"]["granule_path"])
                if "out_dir" in opts:
                    out_dir = opts["out_dir"]
                else:
                    out_dir = dirname(dir_inp)

                opts["fn"] = join(out_dir, l2a_rel_path, l2a_product_name.replace("L2A", "META") + "." + opts["format"])

            elif opts["type"] == "rgb_jpeg":
                dir_inp = abspath(options["S2Image"]["granule_path"])
                if "out_dir" in opts:
                    out_dir = opts["out_dir"]
                else:
                    out_dir = dirname(dir_inp)

                opts["fn"] = join(out_dir, l2a_rel_path, l2a_product_name.replace("L2A", "RGB") + ".jpg")

            elif opts["type"] == "L2A":
                if "out_dir" in opts:
                    out_dir = opts["out_dir"]
                else:
                    out_dir = dirname(dir_inp)

                opts["fn"] = join(out_dir, l2a_rel_path)
            else:
                raise ValueError("output type: %s not implemented" % opts["type"])

            logger.info("Output type: %s -> %s" % (opts["type"], opts["fn"]))

        # create output directories
        if create_output_dirs is True:
            for opts in options["output"]:
                makedirs(dirname(opts["fn"]), exist_ok=True)

        return suffix if run_suffix is True else None

    @staticmethod
    def write_results(s2img, options, logger=None):
        """Write all in options requested output formats."""
        logger = logger or logging.getLogger(__name__)
        for opts in options["output"]:
            if opts["type"] == "metadata":
                IO.write_metadata(options=options, opts=opts, logger=logger)
            elif opts["type"] == "rgb_jpeg":
                IO.write_rgb_jpeg(s2img=s2img, opts=opts, logger=logger)
            elif opts["type"] == "L2A":
                IO.write_l2a(granule_path=opts["fn"],
                             band_fns=s2img.band_fns,
                             projection=s2img.metadata["projection"],
                             data=s2img.data_ac,
                             uncert=s2img.data_errors,
                             msk=s2img.mask_clouds,
                             tau=s2img.s2tau,
                             cwv=s2img.s2cwv,
                             clear_areas=s2img.clear_areas,
                             max_value_uncert=opts["max_value_uncert"],
                             nodata_value_data=opts["nodata_value_data"],
                             nodata_value_mask=opts["nodata_value_mask"],
                             driver=opts["gdal_driver"],
                             options_lossless=opts["options_lossless"],
                             options_lossy=opts["options_lossy"],
                             options_mask=opts["options_mask"],
                             n_cores=opts["n_cores"],
                             level_1c_xml=s2img.granule_xml_file_name,
                             logger=logger,
                             max_time_minutes=opts["max_time_minutes"],
                             mask_ss=opts["mask_ss"],
                             mask_geo_band=opts["mask_geo_band"],
                             output_bands=opts["output_bands"],
                             )
            else:
                raise ValueError("output type: %s not implemented" % opts["type"])

    @staticmethod
    def write_rgb_jpeg(s2img, opts, logger=None):
        """Write jpeg rgm image of image according to options in opts."""
        logger = logger or logging.getLogger(__name__)
        s2rgb = s2img.image_to_rgb(output_size=opts["output_size"],
                                   hist_chop_off_fraction=opts["hist_chop_off_fraction"])
        logger.info("Write: %s" % str(opts["fn"]))
        PIL.Image.fromarray(s2rgb).save(opts["fn"], quality=opts["quality"], optimize=True, progressive=True)

    @staticmethod
    def write_metadata(opts, options, logger=None):
        """Write metadata to logfile."""
        logger = logger or logging.getLogger(__name__)

        def d2d(dic):
            """Convert dictionary to something json can serialize - only a hack for now."""
            def fmt(i):
                if isinstance(i, slice):
                    return str(i)
                if isinstance(i, float):
                    return str(i)
                else:
                    return i

            try:
                return {str(k): d2d(v) if isinstance(v, dict) else fmt(v) if not isinstance(v, list) else [
                    d2d(a) for a in v] for k, v in dic.items()}
            except Exception:
                return dic

        if opts["format"] == "json":
            logger.info("Write: %s" % opts["fn"])
            with open(opts["fn"], "w") as fl:
                fl.writelines(json.dumps(d2d(options), indent=4))
        elif opts["format"] == "xml":
            logger.info("Write: %s" % opts["fn"])
            with open(opts["fn"], "w") as fl:
                logging.getLogger("dicttoxml").setLevel(logging.WARNING)
                fl.writelines(parseString(dicttoxml(d2d(options))).toprettyxml())
        else:
            raise ValueError("Output type not implemented: %s" % str(opts["type"]))

    @staticmethod
    def write_l2a(granule_path, band_fns, projection, data=None, uncert=None, msk=None, driver="JP2OpenJPEG",
                  logger=None,
                  options_lossless={"JP2OpenJPEG": ["QUALITY=100", "REVERSIBLE=YES"]}, clear_areas=None,
                  options_lossy={"JP2OpenJPEG": ["QUALITY=30", "REVERSIBLE=NO"]},
                  options_mask={"JP2OpenJPEG": ["QUALITY=100", "REVERSIBLE=YES", "WRITE_METADATA=YES"]},
                  n_cores=3, max_time_minutes=20, mask_ss=[10.0, 20.0, 60.0], mask_geo_band="B11",
                  level_1c_xml=None, nodata_value_data=65535, max_value_uncert=0.2,
                  nodata_value_mask=255, tau=None, cwv=None, ss_other=(20.0,),
                  output_bands={
                      10.0: ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B11', 'B12', 'B8A'],
                      20.0: ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B11', 'B12', 'B8A'],
                      60.0: ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B11', 'B12', 'B8A']}
                  ):
        """Write Sentinel-2 Level-2A product to file system."""

        logger = logger or logging.getLogger(__name__)
        logger.info("Write data to: %s" % granule_path)

        outputs = []

        projection_ss = {pr['mapinfo'][5]: pr for pr in projection.values()}

        def include_l1c_string(fname):
            """Insert 'L1C_' between dirname and basename of fname."""
            ffname = basename(fname)
            if "L1C" not in ffname:
                return join(dirname(fname), "L1C_" + ffname)
            else:
                return fname

        band_fns = {band_name: include_l1c_string(fns) for band_name, fns in band_fns.items()}

        if output_bands is not None and data is not None:
            outputs += [{
                "data": data[band],
                "order": 3,
                "filename": join(granule_path, "IMG_DATA", "R%im" % ss, basename(
                    band_fns[band]).replace("L1C", "L2A").replace(".jp2", "_%im.jp2" % ss)),
                "gdal_type": gdal.GDT_UInt16,
                "driver": driver,
                "nodata_value": nodata_value_data,
                "output_ss": ss,
                "projection": projection[band]["prj"],
                "geotransform": projection[band]["gt"],
                "logger": None if n_cores != 1 else logger,
                "options": options_lossless[driver],
                "metadata": {"scaling_value": 10000},
                "fmt_funktion": conv(scale=10000, dtype=np.uint16)} for ss, bands in output_bands.items() for band in
                bands if band in data]

        if output_bands is not None and uncert is not None:
            def mk_conv_error(nodata_value, max_value, dtype):
                scaling_value = int(np.floor((nodata_value - 1) / max_value))

                def conv_scale(x, nodata_value=nodata_value):
                    """Input conversion function."""
                    xx = np.array(x * scaling_value, dtype=dtype)
                    with np.errstate(invalid='ignore'):
                        xx[x >= max_value] = nodata_value - 1
                    xx[np.isnan(x)] = nodata_value
                    return xx

                return scaling_value, conv_scale

            scaling_value, conv_scale = mk_conv_error(nodata_value=255, max_value=max_value_uncert, dtype=np.uint8)

            outputs += [{
                "data": uncert[band],
                "filename": join(granule_path, "QI_DATA", "R%im" % ss, basename(
                    band_fns[band]).replace("L1C", "uncertainty").replace(".jp2", "_%im.jp2" % ss)),
                "gdal_type": gdal.GDT_Byte,
                "driver": driver,
                "output_ss": ss,
                "order": 1,
                "metadata": {"scaling_value": scaling_value, "max_value": max_value_uncert},
                "nodata_value": 255,
                "projection": projection[band]["prj"],
                "geotransform": projection[band]["gt"],
                "logger": None if n_cores != 1 else logger,
                "options": options_lossy[driver],
                "fmt_funktion": conv_scale} for ss, bands in output_bands.items() for band in bands if band in uncert]

        if clear_areas is not None:
            outputs += [{
                "data": clear_areas[ss],  # resampling to correct spatial sampling happens in write_raster_gdal
                "order": 0,
                "filename": join(granule_path, basename(
                    band_fns[mask_geo_band]).replace("L1C", "PML2A").replace(
                        "_%s" % mask_geo_band, "").replace(".jp2", "_%im.jp2" % ss)),
                "gdal_type": gdal.GDT_Byte,
                "driver": driver,
                "output_ss": ss,
                "nodata_value": nodata_value_mask,
                "projection": projection_ss[ss]["prj"],
                "geotransform": projection_ss[ss]["gt"],
                "logger": None if n_cores != 1 else logger,
                "options": options_mask[driver],
                "metadata": {"L2A": 1, "L1C": 0},
                "fmt_funktion": conv(scale=1, dtype=np.uint8)} for ss in clear_areas.keys()]

        if msk is not None:
            outputs += [{
                "data": msk.mask_array,  # resampling to correct spatial sampling happens in write_raster_gdal
                "order": 0,
                "filename": join(granule_path, basename(
                    band_fns[mask_geo_band]).replace("L1C", "MSK").replace(
                        "_%s" % mask_geo_band, "").replace(".jp2", "_%im.jp2" % ss)),
                "gdal_type": gdal.GDT_Byte,
                "driver": driver,
                "output_ss": ss,
                "nodata_value": nodata_value_mask,
                "projection": projection[mask_geo_band]["prj"],
                "geotransform": projection[mask_geo_band]["gt"],
                "logger": None if n_cores != 1 else logger,
                "options": options_mask[driver],
                "metadata": {str(k): str(v) for k, v in msk.mask_legend.items()},
                "fmt_funktion": conv(scale=1, dtype=np.uint8)} for ss in mask_ss]

            if hasattr(msk, "novelty"):
                if msk.novelty is not None:
                    ss = 20.0
                    outputs.append({
                        "data": msk.novelty,  # resampling to correct spatial sampling happens in write_raster_gdal
                        "order": 0,
                        "filename": join(granule_path, basename(
                            band_fns[mask_geo_band]).replace("L1C", "NVT").replace(
                                "_%s" % mask_geo_band, "").replace(".jp2", "_%im.jp2" % ss)),
                        "gdal_type": gdal.GDT_Byte,
                        "driver": driver,
                        "output_ss": ss,
                        "nodata_value": nodata_value_mask,
                        "projection": projection[mask_geo_band]["prj"],
                        "geotransform": projection[mask_geo_band]["gt"],
                        "logger": None if n_cores != 1 else logger,
                        "options": options_mask[driver],
                        "metadata": {"nodata_value": nodata_value_mask,
                                     "novel_data": 0,
                                     "known_data": 1},
                        "fmt_funktion": conv(scale=1, dtype=np.uint8)})

        if tau is not None:
            outputs += [{
                "data": tau[20.0],  # resampling to correct spatial sampling happens in write_raster_gdal
                "order": 0,
                "filename": join(granule_path, basename(
                    band_fns[mask_geo_band]).replace("L1C", "AOT").replace(
                        "_%s" % mask_geo_band, "").replace(".jp2", "_%im.jp2" % ss)),
                "gdal_type": gdal.GDT_UInt16,
                "driver": driver,
                "output_ss": ss,
                "nodata_value": nodata_value_data,
                "projection": projection[mask_geo_band]["prj"],
                "geotransform": projection[mask_geo_band]["gt"],
                "logger": None if n_cores != 1 else logger,
                "options": options_lossless[driver],
                "metadata": {"scaling_value": 1000, "name": "aerosol optical thickness at 550nm", "unit": 1},
                "fmt_funktion": conv(scale=1000, dtype=np.uint16)} for ss in ss_other]

        if cwv is not None:
            outputs += [{
                "data": cwv[20.0],  # resampling to correct spatial sampling happens in write_raster_gdal
                "order": 0,
                "filename": join(granule_path, basename(
                    band_fns[mask_geo_band]).replace("L1C", "CWV").replace(
                        "_%s" % mask_geo_band, "").replace(".jp2", "_%im.jp2" % ss)),
                "gdal_type": gdal.GDT_UInt16,
                "driver": driver,
                "output_ss": ss,
                "nodata_value": nodata_value_data,
                "projection": projection[mask_geo_band]["prj"],
                "geotransform": projection[mask_geo_band]["gt"],
                "logger": None if n_cores != 1 else logger,
                "options": options_lossless[driver],
                "metadata": {"scaling_value": 100, "name": "columnar water vapour", "unit": "mm"},
                "fmt_funktion": conv(scale=100, dtype=np.uint16)} for ss in ss_other]

        for dd in set([dirname(opts["filename"]) for opts in outputs]):
            makedirs(dd, exist_ok=True)

        __tw0__ = time()
        if n_cores == 1:
            logger.info("Proceed with serial writing.")
            for opts in outputs:
                write_raster_gdal(**opts)

        else:
            logger.info("Proceed with parallel writing:%i" % n_cores)
            pl = Pool(processes=n_cores)
            IO.wait_jobs_dict({opts["filename"]: pl.apply_async(write_raster_gdal, kwds=opts)
                               for opts in outputs}, logger=logger, max_time_minutes=max_time_minutes)
            pl.terminate()
            pl.close()
            del pl

        if level_1c_xml is not None:
            copy(level_1c_xml, granule_path)

        __tw1__ = time()
        logger.info("Total write time: %f.1s" % (__tw1__ - __tw0__))

    @staticmethod
    def get_mx(data, nbins=100, hist_th=0.95, data_dd=100):
        """

        :param data: numpy array, 2D with error values
        :param nbins: number of bins for cumulative histogram
        :param hist_th: cumulative histogram threshold
        :param data_dd: stride value for data to spped things up
        :return:
        """
        bf = data.flatten()[::data_dd]  # no NaN's allowed in histogram
        hh, xx = np.histogram(bf[np.isfinite(bf)], bins=nbins, normed=True)
        cs = np.cumsum(hh) * (xx[1] - xx[0])
        return xx[np.argmax(cs > hist_th)]

    @staticmethod
    def err_out_arr(data, v_max=254, data_dd=10, hist_th=0.94, nodata_value=255):
        try:
            max_error = IO.get_mx(data=data, data_dd=data_dd, hist_th=hist_th, nbins=100)
            mx = int(np.ceil(v_max / max_error))
            err = np.array(data * mx, dtype=np.uint8)
            err[data > mx] = v_max
            err[np.isnan(data)] = nodata_value
            return SimpleNamespace(array=err, scaling_value=mx)
        except OverflowError:
            return SimpleNamespace(array=np.zeros(data.shape, dtype=np.uint8), scaling_value=0)


class Figs(object):
    """General plotting of internal ac products."""
    def __init__(self, s2rgb=None, s2cwv=None, s2tau=None, s2msk_rgb=None, s2dem=None, s2spr=None,
                 logger=None, fs=16, ss=500):
        self.s2rgb = s2rgb
        self.s2cwv = s2cwv
        self.s2tau = s2tau
        self.s2dem = s2dem
        self.s2spr = s2spr
        self.s2msk_rgb = s2msk_rgb
        self.fs = fs
        self.ss = ss
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def dat_2show(data, nodata):
        """
        Convert data to float and set nodata as nan -> useful when plotting with imshow
        :param data:
        :param nodata: value which will be replaced with NaN
        :return:
        """
        bf = np.array(data, dtype=float)
        bf[data == nodata] = np.NaN
        return bf

    def _to_mpl_(self, inp):
        """Tyop conversion to numpy types that matplotlib can use."""
        if isinstance(inp, np.ndarray):
            ar = inp
        else:
            ar = next(iter(inp.values()))

        d1, d2 = np.array(np.floor(np.array(ar.shape) / self.ss), dtype=int)[:2]
        if len(ar.shape) == 2:
            return np.array(ar[::d1, ::d2], dtype=np.float32)
        elif len(ar.shape) == 3:
            return np.array(ar[::d1, ::d2, :], dtype=np.float32)
        else:
            raise ValueError("Array shape not understood.")

    def rgb(self, ax):
        """Plot pseude rgb of scene."""
        ax.set_title("RGB image", fontsize=self.fs)
        ax.imshow(self._to_mpl_(self.s2rgb), interpolation="none")

    def dem(self, ax):
        """Plot elevation map."""
        ax.set_title("dem image", fontsize=self.fs)
        im = ax.imshow(self._to_mpl_(self.s2dem), interpolation="none", vmin=0.0, cmap=plt.cm.Greys)
        cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.15)
        plt.colorbar(im, cax=cax)

    def spr(self, ax):
        """Plot surface pressure map."""
        ax.set_title("spr image", fontsize=self.fs)
        im = ax.imshow(self._to_mpl_(self.s2spr), interpolation="none", cmap=plt.cm.Blues)
        cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.15)
        plt.colorbar(im, cax=cax)

    def cwv(self, ax):
        """Plot water vapour map."""
        ax.set_title("CWV image", fontsize=self.fs)
        im = ax.imshow(self._to_mpl_(self.s2cwv), interpolation="none", cmap=plt.cm.Oranges)
        cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.15)
        plt.colorbar(im, cax=cax)

    def aot(self, ax):
        """Plot AOT map."""
        ax.set_title("AOT image", fontsize=self.fs)
        im = ax.imshow(self._to_mpl_(self.s2tau), interpolation="none", cmap=plt.cm.Reds)
        cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.15)
        plt.colorbar(im, cax=cax)

    def mak_rgb(self, ax):
        """Plot Mask."""
        ax.set_title("mask image", fontsize=self.fs)
        ax.imshow(self._to_mpl_(self.s2msk_rgb), interpolation="none")

    def plot(self, figs, export_html=None, export_jpg=None, return_figure=False, n_cols=1, dpi=150):
        """Internal plotting on a larger canvas."""
        n_plots = len(figs.keys())
        n_rows = np.ceil(n_plots / n_cols)
        wd = 10

        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure

        fig = Figure(figsize=(wd * n_cols, wd * n_rows))

        FigureCanvas(fig)  # standard way is this: canvas = FigureCanvas(fig)

        plot_names = sorted(figs.keys())
        for ip, plot_name in enumerate(plot_names):
            plot_options = figs[plot_name]
            self.logger.info("Plot: %s" % plot_name)
            ax = fig.add_subplot(n_rows, n_cols, ip + 1)
            getattr(self, plot_name)(ax=ax, **plot_options)

        if export_jpg is not None:
            self.logger.info("Export to jpg:%s" % export_jpg)
            makedirs(dirname(export_jpg), exist_ok=True)
            plt.savefig(export_jpg, bbox_inches='tight', dpi=dpi)

        if export_html is not None:
            self.logger.info("Export to html page:%s" % export_html)
            makedirs(dirname(export_html), exist_ok=True)
            mpld3.save_html(fig=fig, fileobj=export_html)

        if return_figure is False:
            plt.cla()
            plt.clf()
            plt.close()
            del fig
            del canvas
            del ax
            import gc
            gc.collect()
            return None
        elif return_figure is True:
            return fig
        else:
            raise ValueError("return_figure: %s" % str(return_figure))
