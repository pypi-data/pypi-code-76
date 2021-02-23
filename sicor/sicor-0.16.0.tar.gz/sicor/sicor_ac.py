#!/usr/bin/env python
# coding: utf-8
"""Sensor Independent  Atmospheric CORrection (SICOR) AC module.

The module exposes methods for atmospheric correction of multi and hyper spectral Earth observation data.
"""

import argparse
import json
import logging
import pprint
import sys
import traceback
import inspect
import os
import shutil
import re
import platform
import warnings
import gdown

from datetime import date
from io import StringIO
from multiprocessing import Pool
from os import path, makedirs, rmdir
from time import sleep
from time import time
from types import SimpleNamespace
from glob import glob
from os.path import dirname
from os import remove
from os.path import basename
from numbers import Number

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import gdal

from .AC.RtFo import Rho2Rj_const, Rj2RhoJ_const, RtFo
from .AC.ACG import instrument_subset
from .Tools import linear_error_modeling
from .Tools.cB import CloudMask
# noinspection PyProtectedMember
from .options.options import get_options, _processing_dict
from .sensors import SensorSRF
from .sensors.S2MSI import S2Image, GranuleDEM
from .sensors.S2MSI.S2Image.S2Image import s2_snr_model
from .sensors.RSImage import const_snr_model

from .sicor import Figs
from .sicor import StrippedInstance
from .sicor import barometric_formula
from .sicor import get_stats
from .sicor import include_missing_spatial_samplings
from .sicor import quality_check_data_ac_vs_clear_areas
from .sicor import slp2spr
from .sicor import wv, ac_interpolation, IO, prepare_s2_ac
from .sicor import get_ecmwf_data
from .version import __version__

from arosics import DESHIFTER, COREG_LOCAL
from geoarray import GeoArray


__setup__ = False


def is_interactive():
    """Check whether code is executed in an interactive interpreter."""
    import __main__ as main
    return not hasattr(main, '__file__')


if is_interactive() is False:
    if matplotlib.get_backend() != "agg":
        plt.switch_backend('agg')

__t0__ = time()
__tIO__ = 0.0


class Status(object):
    def __init__(self):
        """Collecting exceptions along a program, use .status so signal overall ok'ness
        self.status = 0 -> all is ok (like in Unix)
        self.status != 0 -> we have a problem
        Exceptions can be collected using the self.add_exception method and are stored in
        the list self.exceptions = [([class of error],[traceback]),]
        """
        self.status = 0
        self.exceptions = []

    def add_exception(self, exception):
        self.status = 1
        self.exceptions.append((str(type(exception)),
                                str(traceback.format_exc())))


def coreg_s2(granule="", ref_image_fn=None, ref_image_basepath=None, window_size=(256, 256), force=False,
             suffix="_coreg", n_local_points=30, settings=None,
             image_pattern="IMG_DATA/**/*B[0-9][0-9A]_[1,2,6]0m.jp2", logdir=None, logger=None, fmt_out='JP2KAK',
             msk_pattern="*MSK_*_[1,2,6]0m.jp2", msk_proxy={"10m": "B02_10m", "20m": "B05_20m", "60m": "B01_60m"},
             ref_raster_band_for_s2_band={'B01': 3, 'B02': 3, 'B03': 2, 'B04': 1, 'B05': 1, 'B06': 1, 'B07': 1,
                                          'B08': 1, 'B8A': 1, 'B11': 1, 'B12': 1}):
    """
    Add coregistered images to a Sentinel product, naming is based on [suffix], images are placed in the same location

    :param settings:
    :param ref_image_basepath:
    :param fmt_out
    :param ref_raster_band_for_s2_band:
    :param suffix:
    :param logdir:
    :param logger:
    :param n_local_points:
    :param msk_proxy:
    :param msk_pattern:
    :param granule: path to granule
    :param ref_image_fn: base path for reference image, if None, ref_image is searched in ref_image_basepath
    :param window_size: coreg option
    :param force: True / False, if True, overwrite existing images
    :param image_pattern: tuple how to find images in products, glob pattern
    :return: processing status (0:successful, 1:errors)
    """
    _t0 = time()
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        stream = StringIO()
        logger.addHandler(logging.StreamHandler(stream))
        logging.basicConfig(stream=sys.stdout, filemode='w', datefmt='%H:%M:%S', level=logging.DEBUG,
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
    else:
        stream = None

    options = get_options(target=settings)
    option_loseless = options["output"][0]["options_lossless"][fmt_out]

    try:  # -> e.g. "33UUU"
        tile = re.search('_T[0-9]{2,2}[A-Z]{3,3}_', granule).group(0).replace("_", "")[1:]
    except AttributeError:
        raise ValueError("Can't get granule name from filename:", granule)

    image_fns = sorted(glob(path.join(granule, image_pattern), recursive=True))
    msk_fns = {img.split("_")[-1].split(".jp2")[0]: img for img in sorted(
        glob(path.join(granule, msk_pattern), recursive=True))}

    status = Status()
    fn_grid_images = []

    if ref_image_fn is None:
        try:
            ref_image_fn = glob(path.join(ref_image_basepath, "*%s*" % tile))[0]
        except FileNotFoundError:
            logger.warning("No reference image available for tile: %s" % tile)
            raise

    logger.info("Reference image: %s" % ref_image_fn)

    footprint_poly_ref = None
    footprint_poly_tgt = None

    for image_fn in image_fns:

        band_name = image_fn.split("_")[-2]

        image_fn_out = image_fn.replace(".jp2", suffix + ".jp2")

        if path.exists(image_fn_out) is True and force is False:
            logger.info("skip:%s" % image_fn_out)
        else:
            try:
                logger.info("coreg:%s" % image_fn_out)

                if path.exists(image_fn_out):
                    logger.info("Remove: %s" % image_fn_out)
                    remove(image_fn_out)

                logger.info("Use local shift algorithm.")
                img_spatial_sampling = int(image_fn.split("_")[-1].split("m.jp2")[0])

                img_shape = 10980 / (img_spatial_sampling / 10)
                grid_res = img_shape / n_local_points

                r_b4match = ref_raster_band_for_s2_band[band_name]

                logger.info(
                    "Grid_res: %.0f, ref band used: %i, window size: %s" % (
                        grid_res, r_b4match, str(window_size)))

                masktest, baddata_mask = get_cloud_mask(image_fn)
                if masktest is True:

                    cr = COREG_LOCAL(im_ref=ref_image_fn,
                                     im_tgt=image_fn,
                                     grid_res=grid_res,
                                     window_size=window_size,
                                     path_out=image_fn_out,
                                     mask_baddata_tgt=baddata_mask,
                                     fmt_out=fmt_out,
                                     out_crea_options=option_loseless,
                                     r_b4match=r_b4match,
                                     s_b4match=1,
                                     max_iter=5, max_shift=5, calc_corners=True,
                                     footprint_poly_ref=footprint_poly_ref,
                                     footprint_poly_tgt=footprint_poly_tgt,
                                     tieP_filter_level=3,
                                     CPUs=1,
                                     v=False, q=True, progress=False,
                                     )

                else:
                    raise ValueError("Error while getting cloud_mask for coreg_local")

                # save corner coo to save time
                footprint_poly_ref = cr.COREG_obj.ref.poly
                footprint_poly_tgt = cr.COREG_obj.shift.poly

                logger.info("Start correct shifts.")
                cr.correct_shifts()

                fn_grid_image = image_fn_out.replace(".jp2", "_grid.jpg")
                cr.view_CoRegPoints(figsize=(20, 20), backgroundIm='tgt', savefigPath=fn_grid_image,
                                    hide_filtered=False)
                fn_grid_images.append(fn_grid_image)

                if cr.success is False:
                    raise Exception("Did not correct due to internal errors (most likely: "
                                    "no matching window left after filtering (%s))" % image_fn)

                test, message = check_if_processed(image_fn, image_fn_out)
                if test is False:
                    for kk, vv in message.items():
                        logger.info("Size Test:%s -> %s" % (kk, str(vv)))
                    raise FileExistsError("Processing went wrong cause output file to small or does not exist.")

                # test if reusable for mask
                if msk_proxy is not None:
                    for res, identifier in msk_proxy.items():
                        if identifier in image_fn:
                            logger.info("%s -> %s" % (res, msk_fns[res]))
                            DESHIFTER(im2shift=msk_fns[res],
                                      resamp_alg="nearest",
                                      coreg_results=cr.coreg_info,
                                      CPUs=1, progress=False, v=False, q=True,
                                      path_out=msk_fns[res].replace(".jp2", suffix + ".jp2"),
                                      fmt_out=fmt_out,
                                      out_crea_options=option_loseless,
                                      ).correct_shifts()

            # except NotImplementedError as err:
            except Exception as err:
                status.add_exception(err)
                logger.exception(repr(err))
                band = re.search('_B[0-9A]{2,2}_', image_fn).group(0).replace("_", "")[1:]
                if band == "01":
                    logger.info("Error in 60m Band, skipping cleanup...")
                else:
                    cleanup_coreg(granule, logger=logger)
                break

    if logdir is not None:
        dt = date.today()
        logfn = path.join(logdir, str(dt.year), str(dt.month), str(dt.day),
                          "processing_status_%s" % status.status, tile,
                          basename(path.normpath(granule)) + ".json")
        logger.info("Write logs to: %s" % logfn)
        logdict = {
            "interface": (lambda ii: {nn: ii.locals[nn] for nn in ii.args if nn not in ["logger"]})(
                inspect.getargvalues(inspect.currentframe())),
            "log": stream.getvalue().split("\n") if stream is not None else "",
            "processing": {"status": status.status, "exceptions": status.exceptions},
            "reference_image": ref_image_fn,
            "granule": granule,
            "tile": tile,
            "suffix": suffix,
        }
        makedirs(path.dirname(logfn), exist_ok=True)
        map(os.remove, glob(logfn[:-18] + "*.json") + glob(logfn[:-18] + "*.jpg"))
        with open(logfn, "w") as fl:
            json.dump(logdict, fl, indent=4)

        # copy grid images
        dd = dirname(logfn)
        try:
            for fn in fn_grid_images:
                logger.info("Copy: %s -> %s" % (fn, dd))
                shutil.copy(fn, dd)
        except Exception:
            pass

    else:
        logger.info("No log is written.")

    logger.info("Runtime:%s" % (time() - _t0))
    logger.info("return status %s" % status.status)
    logger.info("EEooFF(coreg_s2)")

    return status


def cleanup_coreg(granule, logger=None):
    """
    If an error occurs, delete all files containing "coreg" in the granule path.

    :param granule: str
    :param logger: logger
    """
    logger.info("Cleanup and exit...")
    msk_files = glob(granule + "/*coreg*", recursive=True)
    if len(msk_files) == 0:
        logger.info("No MSKfiles to delete found")
        logger.info("glob-command: " + granule + "/*coreg*")
    for mfi in msk_files:
        remove(mfi)
        logger.info("Removing Masks: %s" % mfi)
    band_files = glob(granule + "/IMG_DATA/*/*coreg*", recursive=True)
    if len(band_files) == 0:
        logger.info("No Bandfiles to delete found")
        logger.info("glob-command: " + granule + "/IMG_DATA/*/*coreg*")
    for bfi in band_files:
        remove(bfi)
        logger.info("Removing Bands: %s" % bfi)


def check_if_processed(orig_image_fn, cor_image_fn, threshold=0.2):
    """
    checks output jp2 for size
    if in the range of +-10% of the original image, continue, otherwise delete corrected image
    """
    if path.exists(cor_image_fn):
        size_orig = float(path.getsize(orig_image_fn))
        size_cor = float(path.getsize(cor_image_fn))
        if ((size_orig - size_orig * threshold) < size_cor) & ((size_orig + size_orig * threshold) > size_cor):
            return True, {""}
        else:
            try:
                rem_list = glob(cor_image_fn.replace(".jp2", "*"))
                for fi in rem_list:
                    remove(fi)
                return False, {"Error": "Deleted because size did not match original (orig:%s, coreg:%s, file:%s)"
                                        % (size_orig / 1024., size_cor / 1024., cor_image_fn)}
            except Exception as err:
                return False, {"Exception": repr(err)}
    else:
        return False, {"Error": "file does not exist: %s" % cor_image_fn}


def get_cloud_mask(image_fn):
    """
    Gets the cloudmask from corresponding MSK*.jp2 file
    param: image_fn (str) : filename of the data file .jp2
    return: GeoArray of cloudmask (boolean) baddata(cloud)=True, clear=False
    """
    try:

        resstr = str.split(str.split(image_fn, "_")[-1], ".")[0]
        fn_mask = glob(path.join(path.dirname(image_fn), path.pardir, path.pardir, "*MSK*_" + resstr + ".jp2"))[0]

        ds = gdal.Open(fn_mask)
        mask = np.array(ds.GetRasterBand(1).ReadAsArray())
        del ds

        outmask = np.zeros_like(mask, dtype=bool)
        outmask[:] = False
        cidx = np.where((mask == 40) | (mask == 50))

        if len(cidx[0]) != 0:
            outmask[cidx] = True

        geo_arr_img = GeoArray(image_fn)
        geo_arr_mask = GeoArray(outmask, geo_arr_img.gt, geo_arr_img.prj)

        return True, geo_arr_mask

    except Exception as err:
        return False, {"Exception": repr(err)}

####


# noinspection PyShadowingNames
def arguments(ignore=("logger",)):
    """
    Return a tuple containing dictionary of calling function's, named arguments and a list of
    calling function's unnamed positional arguments.
    """
    from inspect import getargvalues, stack
    posname, kwname, kwargs = getargvalues(stack()[1][0])[-3:]
    args = kwargs.pop(posname, [])
    kwargs.update(kwargs.pop(kwname, []))
    return {"args": args, "kwargs": {k: v for k, v in kwargs.items() if k not in ignore}}


# noinspection PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames
def ac(granule_path, out_dir, settings, aerosol_type="aerosol_1", logger=None, raise_on_memory_exception=False,
       catch_all_exceptions=True, logdir=None, persist_result=False, coregistration=None, ignore_coreg_status=False):
    """SICOR Atmospheric Correction on file system level
    Defines logger settings, gets sensor specific options, sets outpath and -filename,
    loads input image, performs AC using function 'ac_gms'.
    :param granule_path: path to Sentinel-2 granule
    :param out_dir: path to output directory
    :param settings: path to settings file (json)
    :param aerosol_type: default aerosol type, fallback if ECMWF is not available
    :param logger: None or logging instance
    :param raise_on_memory_exception: True / False
    :param catch_all_exceptions: True / False
    :param logdir: path to logging directory
    :param persist_result: whether to write result to file system
    :param coregistration: dictionary of options for coreg_s2 (None for omitting coreg_s2)
    :param ignore_coreg_status: True / False
    :return: None
    """
    # if True:
    calling_arguments = arguments(ignore=["logger"])
    t0 = time()
    # get options
    options = get_options(target=settings)
    options["processing"]["interface"] = calling_arguments

    # logger settings
    if logger is None:
        # prepare logging to variable if set
        logger = logging.getLogger(name=options["logger"]["name"])
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        stream = StringIO()
        logger.addHandler(logging.StreamHandler(stream))
        logging.basicConfig(stream=sys.stdout,
                            format=options["logger"]["format"],
                            datefmt=options["logger"]["datefmt"],
                            level=getattr(logging, options["logger"]["level"]))

    try:
        logger.info("AC Version: %s" % str(__version__))

        options["S2Image"]["granule_path"] = granule_path
        logger.info("Granule path: %s" % options["S2Image"]["granule_path"])

        options["AC"]["default_aerosol_type"] = aerosol_type

        # set output path
        for opt in options["output"]:
            opt['out_dir'] = out_dir

        # generate output file names
        options["run_suffix"] = IO.and_and_check_output_fns(options=options, logger=logger, run_suffix=True)
        # test if products already exist
        all_output_exists = all(
            [path.exists(opts["fn"].replace(options["run_suffix"], "")) for opts in options["output"]]) is True

        # core of atmospheric correction
        if all_output_exists is False:  # do AC
            # load image
            s2img = load_product(options=options, logger=logger)
            # do ac
            s2img = ac_gms(s2img, options=options, logger=logger, script=False)

            # save some memory -> discard the band that are not needed anymore
            needed_l1c_bands = set(sum([oo[kk] for kk in ("rgb_bands",) for oo in options["output"] if kk in oo], []))
            obsolete_bands = [band for band in s2img.data.keys() if band not in needed_l1c_bands]
            for band in obsolete_bands:
                del s2img.data[band]  # remove L1C data from memory

            tbf = time()
            IO.write_results(s2img=s2img, options=options, logger=logger)
            del s2img  # free memory

            options["processing"]["tIO"] += time() - tbf
            options["processing"]["tRT"] = time() - t0
            logger.info("Full runtime: %.2fm, IO time: %.2f, IO fraction: %.2f" % (
                options["processing"]["tRT"] / 60.0,
                options["processing"]["tIO"] / 60.0,
                options["processing"]["tIO"] / options["processing"]["tRT"]))

            coreg_status = 0
            if coregistration is not None:
                tbf = time()
                granule_l2a = next((d["fn"] for d in options["output"] if d["type"] == "L2A"), None)
                if granule_l2a is not None:
                    logger.info("Perform coreg:%s" % granule_l2a)
                    coregistration["granule"] = granule_l2a
                    cor_stat = coreg_s2(logger=logger, settings=settings, **coregistration)
                    options["processing"]["coreg"] = {"status": cor_stat.status,
                                                      "exceptions": cor_stat.exceptions,
                                                      "tCoReg": time() - tbf,
                                                      "options": coregistration}
                    coreg_status = cor_stat.status

            # renaming of tmp dir folder
            if ignore_coreg_status is True:
                if "run_suffix" in options:
                    IO.rename_tmp_product(outputs=options["output"], run_suffix=options["run_suffix"], logger=logger)
            else:
                if (coreg_status == 0) & ("run_suffix" in options):
                    IO.rename_tmp_product(outputs=options["output"], run_suffix=options["run_suffix"], logger=logger)

        else:
            logger.info("Products already exist -> skip processing.")
            if options["run_suffix"] != "":
                try:
                    fn = [o["fn"] for o in options["output"] if o["type"] == "L2A"][0]
                    try:
                        logger.info("Remove tmp folder:%s" % fn)
                        rmdir(fn)
                    except OSError:
                        logger.info("Failed since folder is not empty.")
                except IndexError:
                    pass  # means that "L2A" was not part of output options

        options["processing"]["status"] = 0
        options["processing"]["Exception"] = None
        logger.info("EEooFF(AC)")
    except Exception as err:
        # recover options
        # noinspection PyBroadException
        try:
            if isinstance(options, dict) is False:
                raise ValueError
        except Exception:
            options = {"processing": _processing_dict()}

        options["processing"]["status"] = 1
        options["processing"]["Exception"] = traceback.format_exc()
        options["processing"]["Exception_type"] = str(type(err))

    finally:
        # recover logger
        try:
            log = stream.getvalue()
        except Exception:
            log = ""

        if catch_all_exceptions is False and options["processing"]["status"] == 1:
            if logger is None:
                print(options["processing"]["Exception"])
            else:
                logger.exception(options["processing"]["Exception"])
            raise Exception()

        result = {"logger": log,
                  "options": {k: v for k, v in options.items() if k not in ["processing"]},
                  "processing": options["processing"]}

        if persist_result is False:
            return result
        else:
            dt = date.today()
            assert logdir is not None
            logfn = path.join(
                logdir, str(dt.year), str(dt.month), str(dt.day),
                "processing_status_%s" % str(result["processing"]["status"]),
                path.basename(path.normpath(granule_path)))

            logger.info("Write AC logfile to:%s" % logfn)
            makedirs(path.dirname(logfn), exist_ok=True)

            result["logger"] = result["logger"].rstrip().split("\n")
            with open(logfn + ".json", "w") as fl:
                json.dump(d2d(result), fl, indent=4, sort_keys=True)

            options["log"] = log.rstrip().split("\n")
            for opts in options["output"]:
                if opts["type"] == "metadata":
                    opts["fn"] = opts["fn"].replace(options["run_suffix"], "")
                    if os.path.isfile(opts["fn"]):
                        IO.write_metadata(opts, options, logger=logger)

        try:
            if raise_on_memory_exception is True and options["processing"]["Exception_type"] == "<class 'MemoryError'>":
                raise MemoryError()
        except KeyError:
            pass


def d2d(dic):
    """Recurse to dict and replace None with "None" and slices with str(slice) - only a hack"""
    def fmt(i):
        """Replace None with "None" and slices with str(slice)"""
        if isinstance(i, slice):
            return str(i)
        elif isinstance(i, float):
            return str(i)
        elif i is None:
            return "None"
        else:
            return i

    try:
        return {str(k): d2d(v) if isinstance(v, dict) else fmt(v) if not isinstance(v, list) else [d2d(a) for a in v]
                for k, v in dic.items()}
    except Exception:
        return dic


# noinspection PyShadowingNames
def load_product(options, logger=None):
    """Load Earth Observation product, currently supported is Sentinel-2.
    :param options: Options dictionary
    :param logger: None or logging instance
    :returns Object derived from RSImage
    """
    logger = logger or logging.getLogger(__name__)
    if platform.system() == "Linux":
        # set RAM and limits
        from .Tools import RAM
        ram = RAM(unit=options["ram"]["unit"])
        ram.set_limit(options["ram"]["upper_limit"])
    if platform.system() == "Windows":
        warnings.warn("RAM limits are not available on Windows"
                      "as long as there is no alternative implementation for it.")

    # ################
    # ## load image ##
    # ################

    if "s2img" not in locals():
        tbf = time()
        debug = True
        if debug is True:
            s2img = S2Image(logger=logger, **options["S2Image"])
        else:
            s2img_orig = S2Image(logger=logger, **options["S2Image"])
            s2img = StrippedInstance(s2img_orig, S2Image,
                                     attributes=["data", "target_resolution", "dtype_float", "nodata", "tile_name",
                                                 "unit", 'bad_data_value', 'logger', 'yesdata',
                                                 'aux_fields', 'band_list', "band_spatial_sampling", "band_fns",
                                                 "granule_xml_file_name"],
                                     metadata_keys=['spatial_samplings', 'SENSING_TIME', "aux_data", "sun_mean_zenith",
                                                    'viewing_zenith', 'sun_mean_azimuth', 'viewing_azimuth',
                                                    "projection"],
                                     methods=['image_to_rgb', 'image_subsample', 'ecmwf_xi'])
        options["processing"]["tIO"] += time() - tbf
    return s2img


if __name__ == "__main__":
    if is_interactive():
        if __setup__ is False:
            import ipython_memory_usage.ipython_memory_usage as imu

            imu.start_watching_memory()
            # imu.stop_watching_memory()
            # %load_ext autoreload')
            # %autoreload 2')
            # %matplotlib inline')
            # %load_ext memory_profiler')
            __setup__ = True
        args = SimpleNamespace()
        args.granule_path = ''

        args.out_dir = "./tmp_out"
        args.external_data_dir = "/misc/gts2/aux_data/"
        args.aerosol_type = "aerosol_1"
        args.settings = ""  # json file
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--granule_path", action="store", required=True, type=str)
        parser.add_argument("-o", "--out_dir", action="store", required=True, type=str)
        parser.add_argument("-s", "--settings", action="store", required=True, type=str, default="/data/opts.json")
        parser.add_argument("-a", "--aerosol_type", action="store", required=False, default=None,
                            choices=("auto", "aerosol_0", "aerosol_1", "aerosol_2", "aerosol_3"))
        args = parser.parse_args()
        args.external_data_dir = None
    # get and set options
    options = get_options(target=args.settings)
    options["processing"] = _processing_dict()
    logging.basicConfig(stream=sys.stdout,
                        format=options["logger"]["format"],
                        datefmt=options["logger"]["datefmt"],
                        level=getattr(logging, options["logger"]["level"]))
    logger = logging.getLogger(name=options["logger"]["name"])
    logger.setLevel(getattr(logging, options["logger"]["level"]))
    logger.info("AC Version: %s" % str(__version__))

    # set input path
    options["S2Image"]["granule_path"] = args.granule_path
    logger.info("Granule path: %s" % options["S2Image"]["granule_path"])
    # set aerosol
    options["AC"]["default_aerosol_type"] = args.aerosol_type
    # set output path
    for opt in options["output"]:
        opt['out_dir'] = args.out_dir

    if options["logger"]["logg_options"] is True:
        pp = pprint.PrettyPrinter(**options["logger"]["pprint"])
        logger.info(pp.pformat(options))

    s2img = load_product(options)


# noinspection PyShadowingNames
def ac_gms(s2img, options, logger=None, script=True):
    """In memory interface to SICOR.
    Core function of AC.
    :param s2img: Object derived from RSImage -> should be at-sensor reflectance image
    :param options: Dictionary with needed options
    :param logger: None or logging instance
    :param script: True / False: if True, call sys.exit() if cloud coverage is above threshold
    :returns Surface reflectance image.
    """

    # logger settings
    logger = logger or logging.getLogger(__name__)
    # set Sentinel 2 Version
    sensor = options["SRF"]
    sensor_wv = "%s_WV" % sensor
    sensor_ac = "%s_AC" % sensor
    sensor_aot = "%s_AOT" % sensor

    # check if AC tables are available
    logger.info("Check if AC tables are available.")
    from . import tables
    sicor_table_path = path.dirname(tables.__file__)
    for scat_type, op in options["RTFO"].items():
        default_table_path = path.join(sicor_table_path, op['atm_tables_fn'])
        if path.isfile(op['atm_tables_fn']):
            logger.info("AC table for scattering type %s is available at user-provided path, proceed." % scat_type)
        elif path.isfile(default_table_path):
            logger.info("No valid path to AC table for scattering type %s is provided by the user." % scat_type)
            logger.info("Instead, AC table for scattering type %s is available at default tables path, "
                        "proceed." % scat_type)
            op['atm_tables_fn'] = default_table_path
        else:
            logger.info("AC table for scattering type %s is neither available at user-provided path "
                        "nor in default tables path." % scat_type)
            logger.info("Download AC table for scattering type %s from google drive "
                        "and store at default tables path." % scat_type)
            url = 'https://drive.google.com/uc?export=download&id=1-__e8dMlJMC_Lbt5q9-LwS-L5wghKYnn'
            gdown.download(url, default_table_path, quiet=False)
            # check if AC table was properly downloaded
            try:
                assert os.path.getsize(default_table_path) == op["atm_tables_size"]
                logger.info("AC table for scattering type %s was properly downloaded "
                            "and is available for AC!" % scat_type)
            except AssertionError:
                options["processing"]["status"] = 1
                raise AssertionError("AC table for scattering type %s was not properly downloaded. "
                                     "Please restart AC and try again." % scat_type)
            except FileNotFoundError:
                options["processing"]["status"] = 1
                raise FileNotFoundError("AC table could not be properly downloaded, the path provided is incorrect. "
                                        "Please restart AC and try again.")

            op['atm_tables_fn'] = default_table_path

    # check if cloud mask persistence file is available
    logger.info("Check if cloud mask persistence file is available.")
    default_cld_msk_path = path.join(sicor_table_path, options["cld_mask"]["persistence_file"])
    if path.isfile(options["cld_mask"]["persistence_file"]):
        logger.info("Cloud mask persistence file is available at user-provided path, proceed.")
    elif path.isfile(default_cld_msk_path):
        logger.info("No valid path to cloud mask persistence file is provided by the user.")
        logger.info("Instead, cloud mask persistence file is available at default tables path, proceed.")
        options["cld_mask"]["persistence_file"] = default_cld_msk_path
    else:
        logger.info("Cloud mask persistence file is neither available at user-provided path "
                    "nor in default tables path.")
        logger.info("Download cloud mask persistence file from google drive and store at default tables path.")
        url = 'https://drive.google.com/uc?export=download&id=1PHmX24B_LkbGRgfntQbYc8NWlSkdIX-M'
        gdown.download(url, default_cld_msk_path, quiet=False)
        # check if cloud mask persistence file was properly downloaded
        try:
            assert os.path.getsize(default_cld_msk_path) == options["cld_mask"]["persistence_file_size"]
            logger.info("Cloud mask persistence file was properly downloaded and is available for AC!")
        except AssertionError:
            options["processing"]["status"] = 1
            raise AssertionError("Cloud mask persistence file was not properly downloaded. "
                                 "Please restart AC and try again.")
        except FileNotFoundError:
            options["processing"]["status"] = 1
            raise FileNotFoundError("Cloud mask could not be properly downloaded, the path provided is incorrect. "
                                    "Please restart AC and try again.")

        options["cld_mask"]["persistence_file"] = default_cld_msk_path

    # check if novelty detector is available
    logger.info("Check if novelty detector is available.")
    default_nov_det_path = path.join(sicor_table_path, options["cld_mask"]["novelty_detector"])
    if path.isfile(options["cld_mask"]["novelty_detector"]):
        logger.info("Novelty detector is available at user-provided path, proceed.")
    elif path.isfile(default_nov_det_path):
        logger.info("No valid path to novelty detector is provided by the user.")
        logger.info("Instead, novelty detector is available at default tables path, proceed.")
        options["cld_mask"]["novelty_detector"] = default_nov_det_path
    else:
        logger.info("Novelty detector is neither available at user-provided path nor in default tables path.")
        logger.info("Download novelty detector from google drive and store at default tables path.")
        url = 'https://drive.google.com/uc?export=download&id=1k0m5fJCBiJbVAoPQPfN0iqn3LnI3UVvu'
        gdown.download(url, default_nov_det_path, quiet=False)
        # check if novelty detector was properly downloaded
        try:
            assert os.path.getsize(default_nov_det_path) == options["cld_mask"]["novelty_detector_size"]
            logger.info("Novelty detector was properly downloaded and is available for AC!")
        except AssertionError:
            options["processing"]["status"] = 1
            raise AssertionError("Novelty detector was not properly downloaded. Please restart AC and try again.")
        except FileNotFoundError:
            options["processing"]["status"] = 1
            raise FileNotFoundError("Novelty detector could not be properly downloaded, the path provided is incorrect. "
                                    "Please restart AC and try again.")

        options["cld_mask"]["novelty_detector"] = default_nov_det_path

    # preprocessing => derive cloud mask
    # if input image provides no cloud mask, derive own mask from cld_mask persistence file
    if not hasattr(s2img, "mask_clouds"):
        logger.info("Cloud mask missing -> derive own cloud mask.")
        # derive cloud mask instance, which is build from parent class S2cB
        cld_msk = CloudMask(logger=logger, persistence_file=options["cld_mask"]["persistence_file"],
                            processing_tiles=options["cld_mask"]["processing_tiles"],
                            novelty_detector=options["cld_mask"]["novelty_detector"])
        s2img.mask_clouds = cld_msk(img=s2img, target_resolution=options["cld_mask"]["target_resolution"],
                                    majority_filter_options=options["cld_mask"]["majority_mask_filter"],
                                    nodata_value=options["cld_mask"]['nodata_value_mask'])
        del cld_msk

    if not hasattr(s2img, "dem"):
        logger.info("DEM data missing -> get from database")
        # get elevation model object
        granule_dem = GranuleDEM(fn=options["DEM"]["fn"], logger=logger,
                                 slice_x=options["S2Image"]["sliceX"],
                                 slice_y=options["S2Image"]["sliceY"],
                                 target_resolution=options["DEM"]["target_resolution"])
        # get dem for granule and calculate dem missing fraction
        dem = granule_dem(s2img.tile_name, return_zeros_if_missing=options["DEM"]["return_zeros_if_missing"])
        dem_mean = np.nanmean(dem)
        dem_mean = dem_mean if np.isfinite(dem_mean) else 0.0
        # noinspection PyTypeChecker
        dem_missing_fraction = (np.sum(np.isnan(dem)) + np.sum(dem == 0.0)) / np.prod(dem.shape)
        logger.info("DEM missing fraction: %.2f -> replace with: %.2f" % (float(dem_missing_fraction), float(dem_mean)))
        dem[np.isnan(dem)] = dem_mean
        s2img.dem = dem
        s2img.dem_missing_fraction = dem_missing_fraction
        del dem

    if not hasattr(s2img, "dem_missing_fraction"):
        s2img.dem_missing_fraction = (np.sum(np.isnan(s2img.dem)) + np.sum(s2img.dem == 0.0)) / np.prod(s2img.dem.shape)

    if not hasattr(s2img, "srf"):
        logger.info("SRF missing -> get from database.")
        # get spectral response functions
        s2img.srf = SensorSRF(sensor=sensor)

    # get path to quicklook
    quicklook_fn = path.join(options["report"]["report_path"],
                             "%s_ql_%s_%s." % (
                                 sensor, s2img.metadata["SENSING_TIME"].strftime("%Y%m%d_%H:%S"), s2img.tile_name,))

    if options["report"]["reporting"] is True:
        s2rgb = s2img.image_to_rgb(**options["report"]["RGB"])  # make rgb
        s2msk_rgb = s2img.mask_clouds.mask_rgb_array()  # make rgb for mask

    # prep suitable masks for processing
    areas_to_process = s2img.mask_clouds.mk_mask_at_spatial_scales(flags=options["AC"]["labels_to_process"],
                                                                   samplings=s2img.metadata["spatial_samplings"].keys())
    clear_pixels = s2img.mask_clouds.mk_mask_at_spatial_scales(flags=["Clear", "Snow", "Water", "Shadow"],
                                                               samplings=s2img.metadata["spatial_samplings"].keys())
    cloud_pixels = s2img.mask_clouds.mk_mask_at_spatial_scales(flags=["Cirrus", "Cloud"],
                                                               samplings=s2img.metadata["spatial_samplings"].keys())

    clear_fraction = (
        lambda x: np.sum(x == np.True_) / np.sum(s2img.yesdata[options["cld_mask"]["target_resolution"]]))(
            clear_pixels[options["cld_mask"]["target_resolution"]])
    if np.isfinite(clear_fraction) == np.False_:  # keep the '==' over 'is', since np.isfinite returns numpy boolean
        clear_fraction = 0.0  # most likely there are no clear areas in the product
    logger.info("Clear fraction: %.3f" % clear_fraction)
    options["processing"]["clear_fraction"] = clear_fraction

    cloud_fraction = (
        lambda x: np.sum(x == np.True_) / np.sum(s2img.yesdata[options["cld_mask"]["target_resolution"]]))(
        cloud_pixels[options["cld_mask"]["target_resolution"]])
    if np.isfinite(cloud_fraction) == np.False_:  # keep the '==' over 'is', since np.isfinite returns numpy boolean
        cloud_fraction = 0.0  # most likely there are no clouds in the product
    logger.info("Cloud fraction: %.3f" % cloud_fraction)
    options["processing"]["cloud_fraction"] = cloud_fraction

    threshold = options["AC"]["min_clear_fraction"]
    if clear_fraction < threshold:
        if "Cloud" or "Cirrus" in options["AC"]["labels_to_process"]:
            logger.warning("Clear fraction is only %.3f. However, you set 'Cloud' and/or 'Cirrus' as areas to be "
                           "processed so that AC will continue and also cover cloudy pixels." % clear_fraction)

    # calculate novelty fraction
    if hasattr(s2img.mask_clouds, "novelty"):
        if s2img.mask_clouds.novelty is not None:
            novelty_fraction = len(s2img.mask_clouds.novelty[s2img.mask_clouds.novelty == 0]) / np.product(
                s2img.mask_clouds.novelty.shape)
            logger.info("Novelty fraction is: %.4f" % novelty_fraction)

    # check if fraction of pixels to be processed is above predefined threshold, if not, quit AC
    process_fraction = (
        lambda x: np.sum(x == np.True_) / np.sum(s2img.yesdata[options["cld_mask"]["target_resolution"]]))(
        areas_to_process[options["cld_mask"]["target_resolution"]])
    if process_fraction < options["AC"]["min_clear_fraction"]:
        logger.info("Clear fraction is below %.2f -> quit here." % options["AC"]["min_clear_fraction"])
        if options["report"]["reporting"] is True:
            figs = Figs(s2rgb=s2rgb, s2dem=s2img.dem, s2msk_rgb=s2msk_rgb, logger=logger)
            logger.info("Write report to: %s" % quicklook_fn)
            figs.plot(
                export_html=quicklook_fn.replace("[TYPE]", "html") +
                "html" if options["report"]["HTML"] is True else None,
                export_jpg=quicklook_fn.replace("[TYPE]", "jpg") + "jpg" if options["report"]["JPG"] is True else None,
                dpi=options["report"]["dpi"], n_cols=options["report"]["n_cols"], figs=options["report"]["figs_clouds"])

        if script is True:
            # write clear fraction to log file
            for opts in options["output"]:
                fn_log = opts["fn"] + ".log"
                logger.info("Write clear fraction to:%s" % fn_log)
                with open(fn_log, "w") as fl:
                    fl.writelines("Clear fraction %.2f is below %.2f -> quit here." % (
                        process_fraction, options["AC"]["min_clear_fraction"]))
            logger.info("EEooFF")
            sys.exit()
        else:
            logger.info(
                "Cloud coverage is too high -> skip AC, limit output to those given in options[base_output_types]")
            if "output" in options:
                # limit output types to the ones given in "output" TODO: Move outside AC_GMS
                options["output"] = [opts for opts in options["output"] if opts["type"] in options["base_output_types"]]
                for opt in options["output"]:
                    if "output_bands" in opt:
                        opt["output_bands"] = None
            s2img.data_ac = None
            s2img.data_errors = None
            s2img.clear_areas = None
            s2img.s2tau = None
            s2img.s2cwv = None
            return s2img
    # prep cirrus areas
    if "Cirrus" in s2img.mask_clouds.mask_legend.keys():
        cirrus_areas = s2img.mask_clouds.mk_mask_at_spatial_scales(
            flags=["Cirrus"], samplings=s2img.metadata["spatial_samplings"].keys())
    # get surface pressure,  either from ECMWF or DEM alone
    ecmwf_opts = {"image": s2img, "options": options, "logger": logger}
    try:
        logger.info("Derive surface pressure from NWP model.")
        slp = get_ecmwf_data(variable="fc_SLP", **ecmwf_opts) / 100.0  # -> Pa to hPa
        t2m = get_ecmwf_data(variable="fc_T2M", **ecmwf_opts)

        spr = np.array(slp2spr(slp=slp, t=t2m, h=s2img.dem, dt_dh=options["dT/dh"]), dtype=np.float16)
        del slp
        del t2m
    except Exception as err:
        logger.warning("ECMWF surface pressure is missing -> proceed with standard values calculated from DEM.")
        logger.warning("Error message was: %s" % str(repr(err)))
        spr = np.array(barometric_formula(h=s2img.dem), dtype=np.float16)
    s2spr = {options["ECMWF"]["target_resolution"]: spr}
    del spr
    include_missing_spatial_samplings(data=s2spr, samplings=s2img.metadata["spatial_samplings"].keys(), order=0)

    # ########################
    # ## get aux data right ##
    # ########################
    # get ozone
    try:
        mean_ozo = s2img.aux_fields["ozo"] * options["ozo_to_DU"]
        logger.info("Got Ozone from metadata.")
    except AttributeError:
        try:
            logger.info("Ozone missing in metadata -> fallback to ECMWF.")
            mean_ozo = np.mean(options["ozo_to_DU"] * get_ecmwf_data(variable="fc_O3", **ecmwf_opts))
            logger.info("Mean Ozone value: %.2f" % mean_ozo)
        except Exception as err:
            logger.warning("ECMWF ozone value is missing -> proceed with default value.")
            mean_ozo = options["ozone_fallback"]
            logger.info("Default ozone value: %.2f DU" % mean_ozo)
            logger.error("Error message was: %s" % str(repr(err)))

    # get sun and viewing angles
    mean_sza = s2img.metadata['sun_mean_zenith']

    if "values" in dir(s2img.metadata["viewing_zenith"]):
        mean_vza = np.mean([np.nanmean(val.astype(np.float32))
                            for val in s2img.metadata["viewing_zenith"].values()])
    else:
        mean_vza = float(s2img.metadata["viewing_zenith"])
    if not np.isfinite(mean_vza):
        mean_vza = 0.0

    if "values" in dir(s2img.metadata["viewing_azimuth"]):
        mean_azi = (s2img.metadata["sun_mean_azimuth"]
                    - (np.nanmean([np.nanmean(val.astype(np.float32))
                                   for val in s2img.metadata["viewing_azimuth"].values()]))
                    % 180.0)
    else:
        mean_azi = s2img.metadata["sun_mean_azimuth"] - (float(s2img.metadata["viewing_azimuth"]) % 180.0)
    if not np.isfinite(mean_azi):
        mean_azi = 0.0

    assert np.isfinite(mean_ozo)
    assert np.isfinite(mean_sza)
    assert np.isfinite(mean_vza)
    assert np.isfinite(mean_azi)

    # ##############################################
    # ## aot default reasonable values from ECMWF ##
    # ##############################################

    try:
        # get total AOT from data base
        s2tau = {options["ECMWF"]["target_resolution"]: get_ecmwf_data(
            variable=options["ECMWF"]["total_AOT"], **ecmwf_opts)}
        include_missing_spatial_samplings(data=s2tau, samplings=s2img.metadata["spatial_samplings"].keys())

        logger.info("Get AOT prior based on ECMWF forecast fields, mean aot:%.2f." %
                    np.nanmean(s2tau[sorted(s2tau.keys())[-1]][::10, ::10]))

        if options["AC"]["aerosol_type_estimation"] == "maximum_ECMWF_type":
            # get aot fraction per type
            aots = {variable: np.mean(get_ecmwf_data(variable=variable, **ecmwf_opts))
                    for variable in options["ECMWF"]["variables_aerosol"]}
            aots = {name: value / aots[options["ECMWF"]["total_AOT"]] for name, value in aots.items() if
                    name != options["ECMWF"]["total_AOT"]}
            # get type with highest fraction
            types_aot = sorted(aots, key=aots.get, reverse=True)
            for name in types_aot:
                logger.info("ECMWF variable: %s -> fraction: %.2f" % (name, aots[name]))
            # sum up contribution of ECMWF type versus aerosol models in rt lut -> get model with max value
            aerosol_portions = {k: 0 for k in options["ECMWF"]["var2type"].values()}
            for aerosol_type, portion in aots.items():
                aerosol_portions[options["ECMWF"]["var2type"][aerosol_type]] += portion
            aerosol_type = max(aerosol_portions.keys(), key=(lambda key: aerosol_portions[key]))
            logger.info("Aerosol type: %s" % aerosol_type)
        else:
            aerosol_type = options["AC"]["default_aerosol_type"]
            logger.info("Fallback to default aerosol type: %s." % aerosol_type)
    except Exception as err:
        # ECMWF data not available -> proceed with fallback value and type
        logger.warning("ECMWF AOT value is missing -> proceed with default value and type.")
        default_aot = options["AC"]["default_aot_value"]
        aerosol_type = options["AC"]["default_aerosol_type"]
        logger.info("Default AOT value: %.2f" % default_aot)
        logger.info("Default aerosol type: %s" % aerosol_type)
        s2tau = {smpl: np.full(field.shape, default_aot, dtype=np.float16)
                 for smpl, field in s2spr.items()}
        logger.error("Error message was: %s" % str(repr(err)))

    # #######################
    # ## sensor definition ##
    # #######################
    sensors = {sensor: s2img.srf.instrument(s2img.band_list)}
    # specify channels for atmospheric correction
    sensors[sensor_ac] = instrument_subset(
        instrument=sensors[sensor], subset=np.array([s2img.band_list.index(band) for band in options["AC"]["bands"]]))
    if options["water_vapor"]["type"] == "retrieval":
        # specify water vapour sensor
        sensors[sensor_wv] = instrument_subset(
            instrument=sensors[sensor],
            subset=np.array([s2img.band_list.index(band) for band in options["water_vapor"]["bands"]]))
    if "aot_retrieval" in options:
        # set channels for AOT retrieval
        sensors[sensor_aot] = instrument_subset(
            instrument=sensors[sensor],
            subset=np.array([s2img.band_list.index(band) for band in options["aot_retrieval"]["bands"]]))

    # ###########################
    # ## init forward operator ##
    # ###########################

    fo = RtFo(sensors=sensors, **options["RTFO"][aerosol_type])
    fo.reduce_luts(reduce_suffix="AC", reduce_dims={
        "azi": mean_azi, "coz": mean_ozo, "vza": mean_vza, "sza": mean_sza, "tmp": 0})
    if options["water_vapor"]["type"] == "retrieval":
        fo.reduce_luts(reduce_suffix="WV", reduce_dims={
            "azi": mean_azi, "coz": mean_ozo, "vza": mean_vza, "sza": mean_sza, "tmp": 0})
    if "aot_retrieval" in options:
        fo.reduce_luts(reduce_suffix="AOT", reduce_dims={
            "azi": mean_azi, "coz": mean_ozo, "vza": mean_vza, "sza": mean_sza, "tmp": 0, "cwv": fo.dims["cwv"][0]})

    # get border for spr
    spr_min, spr_max = fo.dims["spr"][[0, -1]]
    spr_max = np.floor(spr_max)
    spr_min = np.ceil(spr_min)
    # cut spr range to allowed values in fo table
    for spr in s2spr.values():
        spr[spr >= spr_max] = spr_max
        spr[spr <= spr_min] = spr_min

    # ###################
    # ## cwv retrieval ##
    # ###################

    if options["water_vapor"]["type"] == "retrieval":
        fo.reduce_luts(reduce_suffix="WV", reduce_dims={
            "azi": mean_azi, "coz": mean_ozo, "vza": mean_vza, "sza": mean_sza, "tmp": 0})

        fo.set_sensor(sensor_wv)
        fo.set_luts("WV")
        # constant surface reflectance model
        fo.set_rho_lin(Rho2Rj=Rho2Rj_const(rho_wvl=fo.wvl_sensors[sensor_wv]),
                       Rj2RhoJ=Rj2RhoJ_const(rho_wvl=fo.wvl_sensors[sensor_wv]))
        fo.interpolation_settings(jacobean=False, caching=False)
        s2cwv = wv(fo=fo, s2img=s2img, s2spr=s2spr, s2tau=s2tau, clear_areas=areas_to_process,
                   cloud_fraction=cloud_fraction, logger=logger, **options["water_vapor"])

        # fallback to ECMWF:
        finite_test = (lambda x: [np.isfinite(np.nanmin(x)), np.isfinite(np.nanmax(x))])(s2cwv[sorted(s2cwv.keys())[0]])
        if np.False_ in finite_test:
            logger.info("CWV values are not valid -> fallback to ECMWF.")

            s2cwv = {options["ECMWF"]["target_resolution"]: get_ecmwf_data(
                variable=options["ECMWF"]["variable_tcwv"], **ecmwf_opts)}
            include_missing_spatial_samplings(data=s2cwv, samplings=s2img.metadata["spatial_samplings"].keys())

    elif options["water_vapor"]["type"] == "ECMWF":
        try:
            s2cwv = {options["ECMWF"]["target_resolution"]: get_ecmwf_data(
                variable=options["ECMWF"]["variable_tcwv"], **ecmwf_opts)}
            include_missing_spatial_samplings(data=s2cwv, samplings=s2img.metadata["spatial_samplings"].keys())
        except Exception as err:
            # ECMWF data not available -> proceed with default value
            logger.warning("ECMWF CWV value is missing -> proceed with default value.")
            default_cwv = options["AC"]["default_cwv_value"]
            logger.info("Default CWV value: %.2f mm" % default_cwv)
            s2cwv = {smpl: np.full(field.shape, default_cwv, dtype=np.float16)
                     for smpl, field in s2spr.items()}
            logger.error("Error message was: %s" % str(repr(err)))
    else:
        raise ValueError('options["water_vapor"]["type"]=%s is not implemented' % str(options["water_vapor"]["type"]))

    # ############################
    # ## intermediate reporting ##
    # ############################
    if options["report"]["reporting"] is True:
        logger.info("Write report to: %s" % quicklook_fn)
        figs = Figs(s2rgb=s2rgb, s2cwv=s2cwv, s2tau=s2tau, s2msk_rgb=s2msk_rgb, s2dem=s2img.dem, s2spr=s2spr,
                    logger=logger)
        figs.plot(
            export_html=quicklook_fn.replace("[TYPE]", "html") + "html" if options["report"]["HTML"] is True else None,
            export_jpg=quicklook_fn.replace("[TYPE]", "jpg") + "jpg" if options["report"]["JPG"] is True else None,
            dpi=options["report"]["dpi"], n_cols=options["report"]["n_cols"], figs=options["report"]["figs"]
        )
    # ########
    # ## ac ##
    # ########
    fo.set_sensor(sensor_ac)
    fo.set_luts("AC")
    # constant surface reflectance model
    fo.set_rho_lin(Rho2Rj=Rho2Rj_const(rho_wvl=fo.wvl_sensors[sensor_ac]),
                   Rj2RhoJ=Rj2RhoJ_const(rho_wvl=fo.wvl_sensors[sensor_ac]))
    fo.interpolation_settings(jacobean=False, caching=False)
    points, rhos, rfls = prepare_s2_ac(
        s2spr=s2spr, s2cwv=s2cwv, s2tau=s2tau, clear_areas=areas_to_process, fo=fo, **options["AC"])

    ac_kw = {"points": points, "rhos": rhos, "rfls": rfls,
             "max_pixel_processing": options["AC"]["max_pixel_processing"],
             's2img': s2img, 's2spr': s2spr, 's2cwv': s2cwv, 's2tau': s2tau, 'clear_areas': areas_to_process}

    logger.info("Start ac processing using %i processes." % options["AC"]["n_cores"])
    if options["AC"]["n_cores"] == 1:
        data_ac = {band: ac_interpolation(band=band, iband=iband, **ac_kw) for iband, band in
                   enumerate(options["AC"]["bands"])}
    else:
        try:

            if options["debug"] is True:
                from multiprocessing.dummy import Pool as dPool
                pl = dPool(processes=options["AC"]["n_cores"])
            else:
                pl = Pool(processes=options["AC"]["n_cores"])

            jobs = {band: pl.apply_async(func=ac_mp, args=(iband, band)) for iband, band in
                    enumerate(options["AC"]["bands"])}

            if options["AC"]["monitor_mp"] is True:
                readies = {band: job.ready() for band, job in jobs.items()}
                n_ready = sum(readies.values())
                n_jobs = len(jobs)
                t0_mp = time()
                while n_ready < n_jobs:
                    readies = {band: job.ready() for band, job in jobs.items()}
                    nrb = sum(readies.values())
                    if n_ready < nrb:
                        n_ready = nrb
                        logger.info("Wait for %i out of %i jobs to complete." % (n_ready, n_jobs))
                    sleep(0.2)
                    if options["AC"]["timeout_mp"] is not None:
                        if (time() - t0_mp) > options["AC"]["timeout_mp"]:
                            raise TimeoutError("AC in mp did not finish in time.")
            data_ac = {band: job.get() for band, job in jobs.items()}
            logger.info("Finished AC in multiprocessing mode.")

        except Exception as ex:
            logger.info("Error during multi processing: %s,%s" % (str(ex), str(repr(ex))))
            logger.error(traceback.format_exc())
            data_ac = {band: None for iband, band in enumerate(options["AC"]["bands"])}
        finally:
            logger.info("Terminating Pool.")
            try:
                pl.terminate()
                pl.close()
                del pl
            except Exception:
                pass

        for iband, band in enumerate(options["AC"]["bands"]):
            if data_ac[band] is None:
                logger.info("Error for band :%s -> retry in single processing." % band)
                data_ac[band] = ac_interpolation(band=band, iband=iband, **ac_kw)
    logger.info("Append results to input object.")

    s2img.wvl_ac = fo.wvl_sensors[sensor_ac]
    s2img.clear_areas = areas_to_process
    if "Cirrus" in s2img.mask_clouds.mask_legend.keys():
        s2img.cirrus_areas = cirrus_areas
    s2img.data_ac = data_ac
    s2img.s2tau = s2tau
    s2img.s2cwv = s2cwv

    if options["AC"]["fill_nonclear_areas"]:
        s2img.copied_areas = {ss: np.logical_and(s2img.yesdata[ss], s2img.clear_areas[ss] == np.False_) for ss in
                              s2img.yesdata.keys()}
        for band in s2img.data_ac.keys():
            copy_area = s2img.copied_areas[s2img.band_spatial_sampling[band]]
            s2img.data_ac[band][copy_area] = s2img.data[band][copy_area]
        logger.info("Fill nonclear %.2f%% of the image with L1C data." % float(
            100 * np.sum(copy_area) / np.prod(copy_area.shape)))

    # remove tau, cwv, and spr for nonclear areas from final products
    for ss, clear_area in areas_to_process.items():
        s2tau[ss][np.logical_not(clear_area)] = np.nan
        s2cwv[ss][np.logical_not(clear_area)] = np.nan
        s2spr[ss][np.logical_not(clear_area)] = np.nan

    # #####################################################
    # ## quality check: compare data_ac with clear_areas ##
    # #####################################################

    s2img.clear_areas = quality_check_data_ac_vs_clear_areas(s2img, logger)

    # ###########################
    # ## compute uncertainties ##
    # ###########################

    if "uncertainties" in options:
        rfl_to_rad = {
            band: sol_irr * s2img.metadata["U"] * np.cos(np.deg2rad(s2img.metadata['sun_mean_zenith'])) / np.pi for
            band, sol_irr in s2img.metadata['solar_irradiance'].items()}

        from .sensors import S2MSI
        sicor_s2_uncertainties_path = path.dirname(S2MSI.__file__)
        if isinstance(options["uncertainties"]["snr_model"], Number):
            s2snr = const_snr_model(options["uncertainties"]["snr_model"])
        elif path.isfile(path.join(sicor_s2_uncertainties_path, "data", options["uncertainties"]["snr_model"])):
            options["uncertainties"]["snr_model"] = path.join(sicor_s2_uncertainties_path, "data",
                                                              options["uncertainties"]["snr_model"])
            s2snr = s2_snr_model(s2_snr_csv_file=options["uncertainties"]["snr_model"], rfl_to_rad=rfl_to_rad)
        else:
            raise ValueError('options["uncertainties"]["snr_model"] = {val} is not understood.'.format(
                val=str(options["uncertainties"]["snr_model"])))

        data_errors = {}
        options['processing']["uncertainties"] = {}
        options['processing']["uncertainties"]["rfl_to_rad"] = rfl_to_rad
        for bid in s2img.data_ac.keys():
            _t0 = time()
            inp_model = {'spr': points[:, 0], 'cwv': points[:, 1], "tau": points[:, 2], "r": rhos,
                         "I": rfls[:, options["AC"]["bands"].index(bid)]}

            inp = dict(**{ii: jj[s2img.band_spatial_sampling[bid]] for ii, jj in
                          [("tau", s2tau), ("spr", s2spr), ("cwv", s2cwv)]},
                       **options["uncertainties"]["default_errors"],
                       **{"I": s2img.data[bid], "r": s2img.data_ac[bid],
                          "dI": s2snr.noise(band_name=bid, reflectance=s2img.data[bid])})

            res = linear_error_modeling(n_max_test=5000, n_max_fit=10000, logger=logger,
                                        mdl_vars=options["uncertainties"]["model_vars"],
                                        data_dict=inp, inp_model=inp_model,
                                        s1=options["uncertainties"]["model_linear"],
                                        s2=options["uncertainties"]["model_quadratic"])
            _t1 = time()

            data_errors[bid] = res["error"]
            options['processing']["uncertainties"][bid] = {key: value for key, value in res.items()
                                                           if key in ["coef", "f", "f_error", "fit_quality"]}
            options['processing']["uncertainties"][bid]['runtime'] = _t1 - _t0

        s2img.data_errors = data_errors
    else:
        s2img.data_errors = None

    s2img.median_values = get_stats(s2img, np.median, options["AC"]["dd_statistics"])
    s2img.std_values = get_stats(s2img, lambda x: np.std(np.array(x, dtype=np.float32)), options["AC"]["dd_statistics"])

    logger.info("Band medians and standard deviations: before and after AC ")
    for band in sorted(s2img.median_values.keys()):
        # noinspection PyStringFormat
        logger.info(band + ", median: %.3f -> %.3f(+/-%.3f), std: %.3f -> %.3f(+/-%.6f)" % (
            s2img.median_values[band] + s2img.std_values[band]))
    options["processing"]["median_values"] = s2img.median_values
    options["processing"]["std_values"] = s2img.std_values

    return s2img


def ac_mp(iband, band):
    """Bare ac in multiprocessing mode, all is global, only specify iband and band."""
    # noinspection PyGlobalUndefined
    global ac_kw  # from initializer in multiprocessing
    try:
        return ac_interpolation(iband, band, **ac_kw)
    except Exception:
        return None


# ############################
# ## write results and exit ##
# ############################

if __name__ == "__main__":
    # call ac if oin ops mode
    if "AC_GMS" in locals():
        s2img = ac_gms(s2img, options, logger=logger, script=True)
    # write output
    twr = time()
    IO.write_results(s2img=s2img, options=options, logger=logger)
    __tIO__ += time() - twr
    __tRT__ = (time() - __t0__)
    logger.info(
        "Full runtime: %.2fm, IO time: %.2f, IO fraction: %.2f" % (__tRT__ / 60.0, __tIO__ / 60.0, __tIO__ / __tRT__))
    # exit if not interactive
    if is_interactive() is False:
        logger.info("EEooFF")
        sys.exit()


# __EEooFF__
