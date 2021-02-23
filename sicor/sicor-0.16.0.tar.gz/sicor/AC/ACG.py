import errno
import logging
import pickle
import shutil
from contextlib import closing
from copy import copy
from datetime import datetime
from multiprocessing import Pool
from os import remove
import numpy as np
import tables
from tqdm import tqdm

from ..Tools import get_memory_use
from ..Tools import tqdm_joblist
from .RtFo import Rho2Rj_LinInterp
from .RtFo import Rj2RhoJ_LinInterp

__author__ = "Niklas Bohn, Andre Hollstein"


def log_memory():
    logging.info("Total used memory: %.2fGB" % (get_memory_use() / 1024.))


# noinspection PyShadowingNames
def get_logger(msg=None, fmt="%(asctime)s - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"):
    """
    Init a logger and set formater.
    :param msg: string, first call to info
    :param fmt: format to set the Formater
    :param datefmt: format for Formater
    :return: logging instance
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    for hdl in logger.handlers:
        logger.removeHandler(hdl)
    logger.addHandler(ch)
    if msg is not None:
        logger.info(msg)
    return logger


# noinspection PyShadowingNames,PyDictCreation
def get_settings():
    settings = {}

    settings["atm_fields"] = ["spr", "coz", "cwv", "ch4", "tau_a",
                              "tau_c"]  # names of atmospharic field which are saved for later output
    settings["n_atm_fields"] = len(settings["atm_fields"])
    settings["EnMap_SRF_file"] = "./databases/SRF_EnMap.txt"

    settings["fo_default_arguments"] = {
        # forward operator settings
        "n_pcs": 35,
        "hash_formats": {'spr': '%.0f,', 'coz': '%.0f,', 'cwv': '%.0f,', 'tmp': '%0f,', 'tau_a': '%.2f,',
                         'vza': '%.0f,', 'sza': '%.0f,'},
        "slices": {},  # {"tmp":slice(0,4,1)}
        "only_toa": True,
        "sensor_interpolation_reference": ["sensor", "pca", "error"][0],
        "default_sensor": "EnMap",
    }

    settings["SolarIrradiance"] = {"path_thuillier": "./databases/solar_irradiance/Solar_irradiance_Thuillier_2002.xls",
                                   "path_fontenla": "./databases/solar_irradiance/SUNp1fontenla.asc",
                                   "path_earth_sun_distance":
                                       './databases/solar_distance/Earth_Sun_distances_per_day_edited.csv',
                                   "irr_unit": 'mW/m**2/nm',
                                   "dataset": "Thuillier2002", }

    basepath = "tables/20150427_high_angles/"
    basepath2 = "tables/20150508_methane/"
    table_atm = "linear_atm_functions_ncwv_3_npre_3_ncoz_3_ntmp_4_wvl_350.0_2550.0_1.00_pca.h5"
    table_ch4 = "linear_atm_functions_ncwv_4_npre_2_ncoz_2_ntmp_1_nch4_4_wvl_350.0_2550.0_1.00_pca.h5"

    settings["default_fo"] = 'aerosol1'
    settings["fo_instances"] = {
        "aerosol1": {
            "atm_tables_fn": basepath2 + table_ch4,
            "table_path": "/table_aerosol/type_0_tmp_0",
            "dim_scat": ["tau_a"],
            "dim_atm": ["spr", "coz", "cwv", "ch4"],
            "flag": 10,
        },

        "cirrus": {
            "atm_tables_fn": basepath + table_atm,
            "table_path": "/table_cirrus",
            "dim_scat": ["tau_c", "eff_rad_cirrus"],
            "dim_atm": ["spr", "coz", "cwv", "tmp"],
            "flag": 20,
        },
        "cloud": {
            "atm_tables_fn": basepath + table_atm,
            "table_path": "/table_cloud",
            "dim_scat": ["tau_lq", "eff_rad_cloud"],
            "dim_atm": ["spr", "coz", "cwv", "tmp"],
            "flag": 30,
        }

    }

    for fo_type, fo_dict in settings["fo_instances"].items():
        for opt, val in settings["fo_default_arguments"].items():
            if opt not in fo_dict:
                fo_dict[opt] = val

    # initial values
    settings["default_values"] = {'spr': 1013.0, 'coz': 350.0, 'cwv': 1.0, 'ch4': 0.7,
                                  'tau_a': 0.1, 'vza': 0.0, 'sza': 10.0, 'azi': 0.0,
                                  'tau_c': 0.1, 'eff_rad_cirrus': 20.0, 'tmp': 1.0,
                                  'tau_lq': 1.0, 'eff_rad_cloud': 25.0}

    # upcasling settings
    settings["nn_spec_i1"] = 15  # no of samples used for upscaling
    settings["nn_spec_i2"] = 15  # no of samples used for upscaling
    settings[
        "guess_dims_upscale"] = None  # ["spr","coz","cwv","ch4","tau_a"] # dims to upscale, None of [] if not wanted
    settings["opt_args_upscale"] = {"rho_0": {"method": "guess", "sigma": 1, "fill": 0.1}, "n_iter": 10,
                                    "ftol": None, "ftol_rel": 1e3, "compute_errors": False, "ee": 1.05, "n_bad": 3,
                                    "debug": False, "g": 0.0, "sc_OE_thres": 0.05}

    # optimization
    settings["error_scale"] = 1e5
    settings["opt_args_defaults"] = {"n_iter": 3, "optimization": True, "ftol": None, "ftol_rel": 1e3,
                                     "compute_errors": True, "ee": 1.05, "n_bad": 3, "debug": False, "g": 0.0,
                                     "sc_OE_thres": 0.05}
    settings["opt_args"] = [{"rho_0": {"method": "guess", "sigma": 1, "fill": 0.1}},
                            # {"rho_0":{"method":"prescribed"}}
                            ]

    linear_segments = (
        [580.0, 600.0],  # ozone
        [750.0, 770.0],  # oxygene
        [880.0, 1010.0], [1110.0, 1160.0], [1340.0, 1470.0], [1790, 1960],  # water vapour
        [2300.0, 2400.0]  # methane
    )
    # noinspection PyTypeChecker
    settings["rho_models"] = {"EnMAP_full_lin_segs": {"type": "linear_segments", "linear_segments": linear_segments,
                                                      'rho_wvl': slice(None, None, 1)},
                              # {"type":"pca","spectral_db":"./EnMap_spectral_db_berlin.h5","n_pca":25}
                              }

    settings["output_file_filters"] = tables.Filters(complevel=1, complib='zlib')  # can ne None
    settings["kwargs_image_cube"] = {"rgb": np.array([212, 64, 12]), "figsize": (10, 5), "scatter_size": 50,
                                     "show_background": True,
                                     "n_pca": 10, "n_data": 10000, "width_ratios": [2, 1], "scatter_alpha": 0.00,
                                     "max_x": 60, "max_y": 60}

    """Propagate default optimization settings to all models"""
    for dic in settings["opt_args"]:
        for key, value in settings["opt_args_defaults"].items():
            if key not in dic:
                dic[key] = value
    return settings


# noinspection PyShadowingNames
def get_arguments():
    args = {}

    """
    args["open_file_mode"] = "file_extension"
    args["input_file"] = "./../../EnMap/eetes/sim_201506_ch4_cirrus_clouds/L1_SIM.hdr"
    #args["input_file_truth"] = './../../EnMap/berlin/data/berlin.hdr'  # can be None
    args["input_file_truth"] = None #'./../../EnMap/berlin/data/berlin.hdr'  # can be None
    args["input_type"] = ["radiance", "reflectance"][0]
    aux_data_path = dirname(args["input_file"]) + "/pt/"
    args["aux_data"] = {  # "sza":{"type":"scalar","value":25.0,"error_scale":1e-5},
                          # "ch4":{"type":"mmap","value":"./../../EnMap/eetes/sim/pt/berlin_ch4.mmap","error_scale":0.01},
                          "sza": {"type": "mmap", "value": aux_data_path + "berlin_sza.mmap", "error_scale": 0.01},
                          "vza": {"type": "mmap", "value": aux_data_path + "berlin_vza.mmap", "error_scale": 0.01},
                          # "spr":{"type":"mmap","value":aux_data_path+"berlin_spr.mmap","error_scale":0.01},
                          # "cwv":{"type":"mmap","value":"./../../EnMap/eetes/sim/pt/berlin_cwv.mmap","error_scale":0.01},
                          # "coz":{"type":"mmap","value":"./../../EnMap/eetes/sim/pt/berlin_coz.mmap","error_scale":0.01},
                          # "tau_a":{"type":"mmap","value":"./../../EnMap/eetes/sim/pt/berlin_tau_a.mmap","error_scale":0.01},
                          }
    args["import_options"] = {}
    """

    # """
    # args["open_file_mode"] = "AVIRIS_C"
    # args["input_file"] = "./../../AVIRIS/f080619t01p00r05/" # coast
    # args["input_file"] = "./../../AVIRIS/f080918t01p00r04/"

    # args["open_file_mode"] = "file_extension"
    # args["default_instrument"] ="AVIRIS_C"
    # args["input_file"] = "./../../AVIRIS/simulated/hispiri/result/f080918t01p00r04rdn_c_sc01_ort_30.hdr"

    args["input_file"] = "./../../AVIRIS-NG/4corners/ang20150422t163638_rdn_v1e/"
    args["default_instrument"] = "AVIRIS_C"
    args["open_file_mode"] = "AVIRIS_NG"

    args["input_file_truth"] = None  # can be None
    args["input_type"] = ["radiance", "reflectance"][0]
    args["aux_data"] = {}
    args["import_options"] = {}
    args["now_timestring"] = datetime.now().strftime('%Y%m%d_%H:%M')
    args["quick_look_file"] = ["./ql_%s.%s" % (args["now_timestring"], ftype) for ftype in ("html", "pdf")]  # or None
    args["output_file"] = ["./L2_AC_%s.%s" % (args["now_timestring"], ext) for ext in ("h5", "hdr")]
    args["instruments_file"] = "./instruments.pkl"  # file to read from / write to the instrument dictionary
    args["instruments_file_mode"] = ["read", "create"][0]
    args["instruments_create"] = "EnMap"  # comma separated list of instrument names
    args["multiprocessing"] = True
    args["max_processes"] = 12  # might be ok for None
    args["use_memory"] = True
    args["memmap_dir"] = "./tmp_dir/"
    # (950, 980, 1)  # which sample subset to process, should be arguments as for range, or None
    args["subset_lines"] = None
    # which sample subset to process, should be arguments as for range, or None
    args["subset_sample"] = None  # (920, 940, 1)
    return args


# noinspection PyShadowingNames
def aux_data_to_p0_e0(data, aux_data):
    """
    Follow aux data protocol
    :param data: input data field, needed for shape
    :param aux_data: dict of dict
    :return: 2D fields for p0,e0 for each key in aux_data, content defined by aux data protocol
    """
    shape = data.shape[:2]
    p0 = np.zeros(shape)
    e0 = np.zeros(shape)
    if aux_data["type"] == "scalar":
        p0[:, :] = aux_data["value"]
        e0[:, :] = p0[:, :] * aux_data["error_scale"]
    elif aux_data["type"] == "mmap":
        mmap = np.memmap(aux_data["value"], dtype=float, mode="r", shape=shape)
        p0[:, :] = mmap[:, :]
        e0[:, :] = p0[:, :] * aux_data["error_scale"]
    else:
        raise ValueError("Undefined aux_data_type:%s" % aux_data["type"])
    return p0, e0


def copy_anything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


# noinspection PyGlobalUndefined,PyShadowingNames
def test_for_memmap(data):
    """
    if data is memmao, append it to global variable memmaps for delete on done
    :param data:
    :return:
    """
    global logger, memmaps
    if type(data) is np.core.memmap:
        logger.info("Adding %s to memmaps." % data.filename)
        memmaps.append(data)


# noinspection PyGlobalUndefined,PyShadowingNames
def rho_models_to_kwargs(rtfo, rho_model, wvls, logger):
    """
    :param wvls:
    :param rtfo:
    :param rho_model: dict with opts
    :return: list of instances of rho to ry and vice versa
    """
    from sklearn.decomposition import PCA  # import here to avoid static TLS ImportError

    logger.info("Include rho model of type: %s" % rho_model["type"])
    if rho_model["type"] == "pca":

        if "spectral_db" in rho_model:
            with tables.open_file(rho_model["spectral_db"], "r") as fl:
                logger.info("Reading:%s" % rho_model["spectral_db"])
                pca_data = fl.root.spectra.read()
            logger.info("Perform PCA using %i components." % rho_model["n_pca"])
            rfl_pca = PCA(n_components=rho_model["n_pca"]).fit(pca_data)
            logger.info("Add rho model to PCA list.")
            pca_opts = {"components": rfl_pca.components_, "mean": rfl_pca.mean_, "rho_wvl": wvls}
        else:
            pca_opts = {op: rho_model[op] for op in ["components", "mean", "bounds"]}
            pca_opts["rho_wvl"] = wvls

        kwargs = {"Rho2Rj": rtfo.Rho2Rj_PCA(**pca_opts), "Rj2RhoJ": rtfo.Rj2RhoJ_PCA(**pca_opts)}

    elif rho_model["type"] == "linear_segments":
        # noinspection PyBroadException
        try:
            if type(rho_model["rho_wvl"]) == slice:
                logger.info("Slice given, use wvls and slice: %s" % str(rho_model["rho_wvl"]))
                rho_wvl = copy(wvls[rho_model["rho_wvl"]])
            else:
                rho_wvl = np.array(rho_model["rho_wvl"], dtype=float)
        except Exception:
            logger.info("Rho_wvl not given for linear model, take all wvls.")
            rho_wvl = copy(wvls[::1])

        bf_args = {"wvl": copy(wvls), "rho_wvl": rho_wvl, "linear_segments": rho_model["linear_segments"]}
        logger.info("Add linear rho model to PCA list.")
        kwargs = {"Rho2Rj": Rho2Rj_LinInterp(**bf_args),
                  "Rj2RhoJ": Rj2RhoJ_LinInterp(**bf_args)}
    else:
        raise ValueError("Unsupported rho_model:%s" % rho_model["type"])
    return kwargs


# noinspection PyGlobalUndefined,PyShadowingNames
def get_instruments(rtfo, metadata=None, expand_wvl=20.0, wvl_rsp_resolution=0.2):
    """
    set up of the instruments dictionary
    :return: dict with instrument spec for rt_fo
    """
    global args, settings, logger, SolarIrradiance
    instruments = {}
    if args["instruments_file_mode"] == "read":
        with open(args["instruments_file"], "rb") as fl:
            logger.info("Reading: %s" % args["instruments_file"])
            instruments.update(pickle.load(fl))
    elif args["instruments_file_mode"] == "create":
        for instrument_name in args["instruments_create"].split(","):
            logger.info("Create instrument description for: %s" % instrument_name)
            if instrument_name == "EnMap":
                s2f = 2.0 * np.sqrt(2.0 * np.log(2.0))
                logger.info("Load: %s" % settings["EnMap_SRF_file"])
                wvl_enmap, fwhms_enmap = (lambda x: (x[:, 0], x[:, 1]))(np.loadtxt(settings["EnMap_SRF_file"]))
                wvl_rsp = np.arange(wvl_enmap[0] - expand_wvl, wvl_enmap[-1] + expand_wvl, wvl_rsp_resolution)
                solar = SolarIrradiance(**settings["SolarIrradiance"])
                instruments["EnMap"] = rtfo.sat(rspf_type="gaussian", wvl_inst=wvl_enmap, wvl_rsp=wvl_rsp,
                                                sigma=fwhms_enmap / s2f, solar=solar)
            else:
                raise ValueError("instrument_name:%s is undefined" % instrument_name)
        if args["instruments_file"] is not None:
            with open(args["instruments_file"], "wb") as fl:
                logger.info("Write to: %s" % args["instruments_file"])
                pickle.dump(instruments, fl)
    else:
        raise ValueError("Wrong mode for instruments_file_mode:%s" % args["instruments_file_mode"])

    if metadata is not None:
        if "instrument_name" in metadata:
            logger.info("Found metadata for %s, create instrument description." % metadata["instrument_name"])
            solar = SolarIrradiance(**settings["SolarIrradiance"])

            if "sigma" in metadata:
                sigma = metadata["sigma"]
            elif "fwhm" in metadata:
                s2f = 2.0 * np.sqrt(2.0 * np.log(2.0))
                sigma = metadata["fwhm"] / s2f
            else:
                raise ValueError("Need to have sigma or fwhm in metadata")

            try:
                instruments[metadata["instrument_name"]] = rtfo.sat(
                    rspf_type="gaussian",
                    wvl_inst=metadata["wavelength"],
                    wvl_rsp=np.arange(metadata["wavelength"][0] - expand_wvl, metadata["wavelength"][-1] + expand_wvl,
                                      wvl_rsp_resolution),
                    sigma=sigma,
                    solar=solar)
            except KeyError as err:
                logger.warning("Unsifficient metadata to create instrument specification")
                logger.warning("Missing data:" + str(repr(err)))

    return instruments


# noinspection PyGlobalUndefined,PyShadowingNames
def get_output_fields(data):
    global args, settings, logger, memmaps
    data_atmosphere_fields = np.zeros(list(data.shape[:2]) + [settings["n_atm_fields"]], dtype=float)
    if args["use_memory"] is True:
        logger.info("Store all resulting fields in Memory.")
        data_surface_reflectance = np.zeros(data.shape, dtype=float)
        data_surface_reflectance_model = np.zeros(data.shape, dtype=float)
    else:
        logger.info("Use memmap objects to store resulting fields.")
        data_surface_reflectance = np.memmap(
            "%sdata_surface_reflectance_%s.memmap" % (args["memmap_dir"], args["now_timestring"]), dtype=float,
            mode='w+', shape=data.shape)
        data_surface_reflectance_model = np.memmap(
            "%sata_surface_reflectance_model_%s.memmap" % (args["memmap_dir"], args["now_timestring"]), dtype=float,
            mode='w+', shape=data.shape)
        memmaps.append(data_surface_reflectance)
        memmaps.append(data_surface_reflectance_model)
    return data_atmosphere_fields, data_surface_reflectance, data_surface_reflectance_model


# noinspection PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined
def adjust_sample_definition():
    global args, logger, data
    if args["subset_sample"] is None:
        args["subset_sample"] = (0, data.shape[0], 1)
    elif type(args["subset_sample"]) == int:
        args["subset_sample"] = (0, data.shape[0], args["subset_sample"])
    logger.info("Subset sample is: " + str(args["subset_sample"]))

    if args["subset_lines"] is None:
        args["subset_lines"] = (0, data.shape[1], 1)
    elif type(args["subset_lines"]) is int:
        args["subset_lines"] = (0, data.shape[1], args["subset_lines"])
    logger.info("Subset lines is: " + str(args["subset_lines"]))


# noinspection PyGlobalUndefined,PyShadowingNames
def get_point_and_error_fields(data, metadata, pt_dims, default_value=-999.0):
    global logger, settings, args
    # arrays of initial point and error
    p0 = np.zeros(list(data.shape[:2]) + [len(pt_dims)], dtype=np.float16)
    e0 = np.zeros(list(data.shape[:2]) + [len(pt_dims)], dtype=np.float16)
    for ii, key in enumerate(pt_dims):
        if "obs" in metadata:
            if key in metadata["obs"]:
                logger.info("Using metadata data for:%s" % key)
                p0[:, :, ii] = metadata["obs"][key]
                e0[:, :, ii] = 0.0
        elif key in args["aux_data"]:
            logger.info("Using aux data for:%s" % key)
            p0[:, :, ii], e0[:, :, ii] = aux_data_to_p0_e0(data=data, aux_data=args["aux_data"][key])
        else:
            try:
                logger.info("Set default aux value %.2f for %s" % (settings["default_values"][key], key))
                p0[:, :, ii] = settings["default_values"][key]
                e0[:, :, ii] = settings["default_errors"][key]
            except KeyError:
                logger.info("No default value profided for %s, using default:%f" % (key, default_value))
                p0[:, :, ii] = default_value
                e0[:, :, ii] = default_value

    return p0, e0


# noinspection PyGlobalUndefined,PyShadowingNames
def convert_data_to_reflectance(data, pt, fo, args):
    if args["input_type"] == "radiance":
        fo.radiance_to_reflectance(radiance=data, pt=pt, in_place=True)
    elif args["input_type"] == "reflectance":
        pass
    else:
        raise ValueError("Unknown input type: %s" % args["input_type"])


# noinspection PyTypeChecker,PyGlobalUndefined
def opt(i1, i2, fo="flags", raise_flag=True, wvl_idxs=slice(None), **opt_args):
    global rtfo, data_flags, fo_flags, flag_to_fo_name, pt_indexes, fos, p0, e0

    if fo == "flags":
        flag = data_flags[i1, i2]
        if flag in fo_flags:
            name = flag_to_fo_name[flag]
            idxs = pt_indexes[name]
            fo = fos[name]
        else:
            if raise_flag is True:
                raise ValueError("Flag is not associated with an retreival.")
            else:
                return None

        return rtfo.opt(self=fo,
                        y_rfl=data[i1, i2, wvl_idxs],
                        pt0=p0[i1, i2, idxs],
                        ssai=e0[i1, i2, idxs],
                        ssei=data[i1, i2, wvl_idxs] / settings["error_scale"],
                        rho_fg=data_surface_reflectance_model[i1, i2, wvl_idxs],
                        **opt_args)


# noinspection PyGlobalUndefined,PyShadowingNames
def sample_optimization_and_upscale_results(data, p0):
    global logger, settings
    if settings["guess_dims_upscale"] is not None or settings["guess_dims_upscale"] == []:
        # import here to avoid static TLS ImportError
        from scipy.ndimage.interpolation import zoom  # upscale p0 from some sample

        default_value = -999.0
        flag = settings["fo_instances"][settings["default_fo"]]["flag"]
        logger.info("Use sample points estimates to upscale estimate for whole image.")
        ii_spec_i1 = np.linspace(0, data.shape[0] - 1, settings["nn_spec_i1"], dtype=int)
        ii_spec_i2 = np.linspace(0, data.shape[1] - 1, settings["nn_spec_i2"], dtype=int)
        logger.info("Using %i,%i samples." % (settings["nn_spec_i1"], settings["nn_spec_i2"]))

        pt_spec = default_value * np.ones(
            (settings["nn_spec_i1"], settings["nn_spec_i2"], len(fos[settings["default_fo"]].pt_dims)))
        zoom_fac = [float(ss) / float(nn) for ss, nn in
                    zip(p0.shape[:2], [settings["nn_spec_i1"], settings["nn_spec_i2"]])]
        logger.info("Zoom factors are: %.2f,%.2f" % tuple(zoom_fac))
        logger.info("Upscaling is used for:" + str(settings["guess_dims_upscale"]))
        upscale_ind = np.array(
            [ii for ii, dim in enumerate(fos[settings["default_fo"]].pt_dims) if dim in settings["guess_dims_upscale"]],
            dtype=int)
        logger.info("Upscale indices are: " + str(upscale_ind))

        for s1, i1 in tqdm(enumerate(ii_spec_i1), total=len(ii_spec_i1)):
            for s2, i2 in enumerate(ii_spec_i2):
                if data_flags[i1, i2] == flag:
                    res = opt(i1, i2, **settings["opt_args_upscale"])
                    if res is not None:
                        pt_spec[s1, s2, :] = res["pt"]

        for ii in range(pt_spec.shape[-1]):
            is_default = pt_spec[:, :, ii] == default_value
            nt_default = pt_spec[:, :, ii] != default_value
            pt_spec[is_default, ii] = np.mean(pt_spec[nt_default, ii])
        p0[:, :, upscale_ind] = zoom(pt_spec[:, :, upscale_ind], zoom_fac + [1], order=1)
    else:
        logger.info("No prior guessing from image sampling, guess_dims_upscale was set to None.")


# noinspection PyGlobalUndefined,PyShadowingNames
def ac_for_line(i1, **opt_args):
    global args, pt_ind_atm_save, flag_to_indexes_common, flag_to_indexes_res
    data_atmosphere_fields = np.zeros([data.shape[1], len(pt_ind_atm_save)])
    shape = data.shape[1:]
    data_surface_reflectance = np.zeros(shape)
    data_surface_reflectance_model = np.zeros(shape)

    for i2 in range(*args["subset_lines"]):
        res = opt(i1, i2, **opt_args)
        if res is not None:
            data_atmosphere_fields[i2, flag_to_indexes_common[data_flags[i1, i2]]] = res["pt"][
                flag_to_indexes_res[data_flags[i1, i2]]]
            data_surface_reflectance[i2, :] = res["rho_ac"]
            data_surface_reflectance_model[i2, :] = res["rho_rj"]
    return i1, (data_atmosphere_fields, data_surface_reflectance, data_surface_reflectance_model)


# noinspection PyGlobalUndefined,PyGlobalUndefined,PyGlobalUndefined
def copy_results(i1, res):
    global data_atmosphere_fields, data_surface_reflectance, data_surface_reflectance_model
    data_atmosphere_fields[i1, :, :], data_surface_reflectance[i1, :, :], data_surface_reflectance_model[i1, :, :] = res


# noinspection PyGlobalUndefined,PyGlobalUndefined
def processing_single(**opt_args):
    global logger, args
    logger.info("Start single core processing.")
    for i1 in tqdm(range(*args["subset_sample"])):
        copy_results(*ac_for_line(i1=i1, **opt_args))
    print("")


# noinspection PyGlobalUndefined,PyGlobalUndefined
def processing_multi(**opt_args):
    global logger, args
    logger.info("Start multi core processing using %i cores." % args["max_processes"])
    with closing(Pool(processes=args["max_processes"])) as pp:
        job_list = [pp.apply_async(func=ac_for_line, args=(i1,), kwds=opt_args) for i1 in range(*args["subset_sample"])]
        tqdm_joblist(job_list, n_status_prints=100, apply_on_done=copy_results)
    print("")


def processing(**opt_args):
    if not args["multiprocessing"]:
        processing_single(**opt_args)
    else:
        try:
            processing_multi(**opt_args)
        except OSError as err:
            if err.errno == 12:
                logger.info("Out of memory, fallback to single core processing")
                processing_single(**opt_args)
            else:
                raise err


def clean_up_memmaps():
    if args["use_memory"] is False:
        for memmap in memmaps:
            fn = memmap.filename
            logger.info("Closing and deleting: %s" % memmap.filename)
            del memmap
            remove(fn)
        del memmaps[:]


# noinspection PyShadowingNames
def get_pt_names_and_indexes(fos, settings):
    fo_flags = [kk["flag"] for ss, kk in settings["fo_instances"].items()]

    pt_names = []
    for fo_name, fo in fos.items():
        for dim in fo.pt_dims:
            if dim not in pt_names:
                pt_names.append(dim)
    pt_indexes = {}
    for fo_name, fo in fos.items():
        pt_indexes[fo_name] = np.array([pt_names.index(dim) for dim in fo.pt_dims], dtype=int)

    pt_names = np.array(pt_names)

    flag_to_indexes_res = {}
    flag_to_indexes_common = {}
    for fo_name, fo_dfs in settings["fo_instances"].items():
        flag_to_indexes_res[fo_dfs["flag"]] = np.array(
            [ii for ii, name in enumerate(pt_names[pt_indexes[fo_name]]) if name in settings["atm_fields"]],
            dtype=int)
        flag_to_indexes_common[fo_dfs["flag"]] = np.array(
            [settings["atm_fields"].index(name) for ii, name in enumerate(pt_names[pt_indexes[fo_name]]) if
             name in settings["atm_fields"]], dtype=int)

    return (pt_names,
            pt_indexes,
            flag_to_indexes_res,
            flag_to_indexes_common,
            fo_flags)


# noinspection PyShadowingNames
def get_fo_dims(fos):
    fo_dims = {}
    for fo_name, fo in fos.items():
        fo_dims.update(fo.dims)
    return fo_dims


def instrument_subset(instrument, subset):
    return {'rspf': instrument['rspf'][subset, :],
            'sol_irr': None if instrument['sol_irr'] is None else instrument['sol_irr'][subset],
            'wvl_inst': instrument['wvl_inst'][subset],
            'wvl_rsp': instrument['wvl_rsp'], }
