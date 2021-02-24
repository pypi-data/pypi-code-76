"""
Utility functions for command-line relevant operations
"""
import datetime as dt
import logging
import os
import os.path
import re
from time import gmtime, strftime

import numpy as np
import openscm_units
import pymagicc
import tqdm
from pymagicc.io import MAGICCData
from scmdata import ScmRun, run_append

from . import __version__
from .io import get_scmcube_helper, load_scmrun
from .iris_cube_wrappers import ScmCube

LOGGER = logging.getLogger("netcdf_scm")

_ureg = openscm_units.unit_registry
"""
Unit registry for miscellaneous unit checking
"""

_MAGICC_VARIABLE_MAP = {"tas": ("Surface Temperature", "SURFACE_TEMP")}
"""Mapping from CMOR variable names to MAGICC variables"""

DEFAULT_LOG_FORMAT = "{process} {asctime} {levelname}:{name}:{message}"


def _setup_log_file(out_filename=None, level=logging.DEBUG):
    if not out_filename:
        return

    h = logging.FileHandler(out_filename, "a")
    h.setLevel(level)
    h.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT, style="{"))

    netcdf_scm_logger = logging.getLogger("netcdf_scm")
    netcdf_scm_logger.handlers.append(h)


def _log_options(params):
    """
    Log the version of netcdf-scm used and other helpful debugging properties

    Parameters
    ----------
    params : list
        A list of key values to write at the start of the log
    """
    LOGGER.info("netcdf-scm: %s", __version__)
    for k, v in params:
        LOGGER.info("%s: %s", k, v)


def _get_timestamp():
    return strftime("%Y%m%d %H%M%S", gmtime())


def _make_path_if_not_exists(path_to_check):
    if not os.path.exists(path_to_check):
        LOGGER.info("Making output directory: %s", path_to_check)
        os.makedirs(path_to_check)


def _load_scm_cube(drs, dirpath, filenames):
    scmcube = get_scmcube_helper(drs)
    if len(filenames) == 1:
        scmcube.load_data_from_path(os.path.join(dirpath, filenames[0]))
    else:
        scmcube.load_data_in_directory(dirpath)

    return scmcube


def _set_crunch_contact_in_results(res, crunch_contact):
    for _, c in res.items():
        if "crunch_contact" in c.cube.attributes:
            LOGGER.warning(
                "Overwriting `crunch_contact` attribute"
            )  # pragma: no cover # emergency valve
        c.cube.attributes["crunch_contact"] = crunch_contact

    return res


def _get_outfile_dir(dpath, drs, dst):
    scmcube = get_scmcube_helper(drs)
    outfile_dir = dpath.replace(scmcube.process_path(dpath)["root_dir"], dst)
    _make_path_if_not_exists(outfile_dir)

    return outfile_dir


def _convert_units(openscmrun, target_units_specs):
    for variable in openscmrun["variable"].unique():
        if variable in target_units_specs["variable"].tolist():
            target_unit = target_units_specs[
                target_units_specs["variable"] == variable
            ]["unit"].values[0]
            current_unit = openscmrun.filter(variable=variable)["unit"].values[0]

            LOGGER.info(
                "Converting units of %s from %s to %s",
                variable,
                current_unit,
                target_unit,
            )

            target_length = _ureg(target_unit).dimensionality["[length]"]
            current_length = _ureg(current_unit).dimensionality["[length]"]
            if np.equal(target_length - current_length, 2):
                openscmrun = _take_area_sum(openscmrun, current_unit)

            openscmrun = openscmrun.convert_unit(target_unit, variable=variable)

    return openscmrun


def _find_dirs_meeting_func(src, check_func):
    matching_dirs = []
    failures = False
    LOGGER.info("Finding directories with files")
    tqdm_kwargs = {
        "desc": "Walking through directories and applying `check_func`",
        "leave": True,
    }
    for dirpath, _, filenames in tqdm.tqdm(os.walk(src), **tqdm_kwargs):
        LOGGER.debug("Entering %s", dirpath)
        if filenames:
            try:
                if check_func(dirpath):
                    matching_dirs.append((dirpath, filenames))
            except Exception as e:  # pylint:disable=broad-except
                LOGGER.error(
                    "Directory checking failed on %s with error %s", dirpath, e
                )
                failures = True

    LOGGER.info("Found %s directories with files", len(matching_dirs))
    return matching_dirs, failures


def _match_regexp_list(list_to_check, regexp):
    regexp_compiled = re.compile(regexp)

    return [v for v in list_to_check if regexp_compiled.match(v)]


def _skip_file(out_file, force):
    if not force and os.path.isfile(out_file):
        LOGGER.info("Skipped (already exists, not overwriting) %s", out_file)
        return True

    if os.path.isfile(out_file):
        os.remove(out_file)

    return False


def _get_path_bits(inpath, drs, include_time_info=False):
    helper = get_scmcube_helper(drs)

    out = helper.process_path(os.path.dirname(inpath))

    if include_time_info:
        out.update(helper._get_timestamp_bits_from_filename(os.path.basename(inpath)))

    return out


def _write_ascii_file(  # pylint:disable=too-many-arguments
    openscmrun,
    metadata,
    header,
    outfile_dir,
    fnames,
    force,
    out_format,
    drs,
    prefix=None,
):
    if out_format in ("mag-files",):
        _write_mag_file(
            openscmrun, metadata, header, outfile_dir, fnames, force, prefix, drs,
        )
    elif out_format in (
        "mag-files-average-year-start-year",
        "mag-files-average-year-mid-year",
        "mag-files-average-year-end-year",
        "mag-files-point-start-year",
        "mag-files-point-mid-year",
        "mag-files-point-end-year",
    ):
        _write_mag_file_with_operation(
            openscmrun,
            metadata,
            header,
            outfile_dir,
            fnames,
            force,
            out_format,
            prefix,
            drs,
        )
    elif out_format in ("magicc-input-files",):
        _write_magicc_input_file(
            openscmrun, metadata, header, outfile_dir, fnames, force, prefix,
        )
    elif out_format in (
        "magicc-input-files-average-year-start-year",
        "magicc-input-files-average-year-mid-year",
        "magicc-input-files-average-year-end-year",
        "magicc-input-files-point-start-year",
        "magicc-input-files-point-mid-year",
        "magicc-input-files-point-end-year",
    ):
        _write_magicc_input_file_with_operation(
            openscmrun,
            metadata,
            header,
            outfile_dir,
            fnames,
            force,
            out_format,
            prefix,
        )
    else:
        raise AssertionError("how did we get here?")  # pragma: no cover


def _write_mag_file(  # pylint:disable=too-many-arguments,too-many-locals
    openscmrun, metadata, header, outfile_dir, fnames, force, prefix, drs
):
    ts = openscmrun.timeseries()

    src_time_points = ts.columns

    time_id = "{:04d}{:02d}-{:04d}{:02d}".format(
        src_time_points[0].year,
        src_time_points[0].month,
        src_time_points[-1].year,
        src_time_points[-1].month,
    )
    old_time_id = _get_path_bits(
        os.path.join(outfile_dir, fnames[0]), drs, include_time_info=True
    )["timestamp_str"]

    out_file_base = fnames[0].replace(old_time_id, time_id)
    if prefix is not None:
        out_file_base = "{}_{}".format(prefix, out_file_base)

    out_file = os.path.join(outfile_dir, out_file_base)
    out_file = "{}.MAG".format(os.path.splitext(out_file)[0])

    if _skip_file(out_file, force):
        return

    writer = MAGICCData(openscmrun)
    writer["todo"] = "SET"
    _check_timesteps_are_monthly(writer)

    writer.metadata = metadata
    writer.metadata["timeseriestype"] = "MONTHLY"
    writer.metadata["header"] = header

    LOGGER.info("Writing file to %s", out_file)
    writer.write(out_file, magicc_version=7)


def _check_timesteps_are_monthly(scmdf):
    time_steps = scmdf["time"][1:].values - scmdf["time"][:-1].values
    step_upper = np.timedelta64(32, "D")  # pylint:disable=too-many-function-args
    step_lower = np.timedelta64(28, "D")  # pylint:disable=too-many-function-args
    if any((time_steps > step_upper) | (time_steps < step_lower)):
        raise ValueError(
            "Please raise an issue at "
            "gitlab.com/netcdf-scm/netcdf-scm/issues "
            "to discuss how to handle non-monthly data"
        )


def _write_mag_file_with_operation(  # pylint:disable=too-many-arguments
    openscmrun, metadata, header, outfile_dir, fnames, force, out_format, prefix, drs,
):  # pylint:disable=too-many-locals
    if len(fnames) > 1:
        raise AssertionError(
            "more than one file to wrangle?"
        )  # pragma: no cover # emergency valve

    ts = openscmrun.timeseries()

    src_time_points = ts.columns
    original_years = ts.columns.map(lambda x: x.year).unique()

    time_id = "{:04d}-{:04d}".format(src_time_points[0].year, src_time_points[-1].year)
    old_time_id = _get_path_bits(
        os.path.join(outfile_dir, fnames[0]), drs, include_time_info=True
    )["timestamp_str"]

    out_file_base = fnames[0].replace(old_time_id, time_id)
    if prefix is not None:
        out_file_base = "{}_{}".format(prefix, out_file_base)

    out_file = os.path.join(outfile_dir, out_file_base)
    out_file = "{}.MAG".format(os.path.splitext(out_file)[0])

    if _skip_file(out_file, force):
        return

    writer = MAGICCData(_do_timeseriestype_operation(openscmrun, out_format)).filter(
        year=original_years
    )

    writer["todo"] = "SET"
    writer.metadata = metadata
    writer.metadata["timeseriestype"] = (
        out_format.replace("mag-files-", "").replace("-", "_").upper()
    )

    writer.metadata["header"] = header

    LOGGER.info("Writing file to %s", out_file)
    writer.write(out_file, magicc_version=7)


def _do_timeseriestype_operation(openscmrun, out_format):
    if out_format.endswith("average-year-start-year"):
        out = openscmrun.time_mean("AS")

    elif out_format.endswith("average-year-mid-year"):
        out = openscmrun.time_mean("AC")

    elif out_format.endswith("average-year-end-year"):
        out = openscmrun.time_mean("A")

    elif out_format.endswith("point-start-year"):
        out = openscmrun.resample("AS")

    elif out_format.endswith("point-mid-year"):
        out_time_points = [
            dt.datetime(y, 7, 1)
            for y in range(
                openscmrun["time"].min().year, openscmrun["time"].max().year + 1
            )
        ]
        out = openscmrun.interpolate(target_times=out_time_points)

    elif out_format.endswith("point-end-year"):
        out = openscmrun.resample("A")

    else:  # pragma: no cover # emergency valve
        raise NotImplementedError("Do not recognise out_format: {}".format(out_format))

    if out.timeseries().shape[1] == 1:
        error_msg = "We cannot yet write `{}` if the output data will have only one timestep".format(
            out_format
        )
        raise ValueError(error_msg)

    return out


def _write_magicc_input_file(  # pylint:disable=too-many-arguments
    openscmrun, metadata, header, outfile_dir, fnames, force, prefix
):
    if len(fnames) > 1:
        raise AssertionError(
            "more than one file to wrangle?"
        )  # pragma: no cover # emergency valve

    _write_magicc_input_files(
        openscmrun, outfile_dir, force, metadata, header, "MONTHLY", prefix,
    )


def _write_magicc_input_file_with_operation(  # pylint:disable=too-many-arguments
    openscmrun, metadata, header, outfile_dir, fnames, force, out_format, prefix,
):
    if len(fnames) > 1:
        raise AssertionError(
            "more than one file to wrangle?"
        )  # pragma: no cover # emergency valve

    ts = openscmrun.timeseries()

    original_years = ts.columns.map(lambda x: x.year).unique()

    openscmrun = _do_timeseriestype_operation(openscmrun, out_format).filter(
        year=original_years
    )

    _write_magicc_input_files(
        openscmrun,
        outfile_dir,
        force,
        metadata,
        header,
        out_format.replace("magicc-input-files-", "").replace("-", "_").upper(),
        prefix,
    )


def _write_magicc_input_files(  # pylint:disable=too-many-arguments,too-many-locals
    openscmrun, outfile_dir, force, metadata, header, timeseriestype, prefix,
):
    try:
        var_to_write = openscmrun["variable"].unique()[0]
        variable_abbreviations = {
            "filename": var_to_write,
            "magicc_name": _MAGICC_VARIABLE_MAP[var_to_write][0],
            "magicc_internal_name": _MAGICC_VARIABLE_MAP[var_to_write][1],
        }
    except KeyError:
        raise KeyError(
            "I don't know which MAGICC variable to use for input `{}`".format(
                var_to_write
            )
        )

    region_filters = {
        "FOURBOX": [
            "World|Northern Hemisphere|Land",
            "World|Southern Hemisphere|Land",
            "World|Northern Hemisphere|Ocean",
            "World|Southern Hemisphere|Ocean",
        ],
        "GLOBAL": ["World"],
    }
    for region_key, regions_to_keep in region_filters.items():
        out_file_base = (
            ("{}_{}_{}_{}_{}_{}.IN")
            .format(
                variable_abbreviations["filename"],
                openscmrun["scenario"].unique()[0],
                openscmrun["climate_model"].unique()[0],
                openscmrun["member_id"].unique()[0],
                region_key,
                variable_abbreviations["magicc_internal_name"],
            )
            .upper()
        )
        if prefix is not None:
            out_file_base = "{}_{}".format(prefix, out_file_base)

        out_file = os.path.join(outfile_dir, out_file_base,)

        if _skip_file(out_file, force):
            return

        writer = MAGICCData(openscmrun).filter(region=regions_to_keep)
        writer["todo"] = "SET"
        writer["variable"] = variable_abbreviations["magicc_name"]
        writer.metadata = metadata
        writer.metadata["header"] = header
        writer.metadata["timeseriestype"] = timeseriestype

        LOGGER.info("Writing file to %s", out_file)
        writer.write(out_file, magicc_version=7)


def _get_openscmdf_metadata_header(
    fnames, dpath, target_units_specs, wrangle_contact, out_format
):
    if len(fnames) > 1:
        raise AssertionError(
            "more than one file to wrangle?"
        )  # pragma: no cover # emergency valve

    openscmrun = run_append([load_scmrun(os.path.join(dpath, f)) for f in fnames])
    if openscmrun.timeseries().shape[1] == 1:
        error_msg = "We cannot yet write `{}` if the output data has only one timestep".format(
            out_format
        )
        raise ValueError(error_msg)

    if target_units_specs is not None:
        openscmrun = _convert_units(openscmrun, target_units_specs)

    metadata = openscmrun.metadata
    header = _get_openscmdf_header(
        wrangle_contact, metadata["crunch_netcdf_scm_version"]
    )

    return openscmrun, metadata, header


def _get_openscmdf_header(contact, netcdf_scm_version):
    header = (
        "Date: {}\n"
        "Contact: {}\n"
        "Source data crunched with: netCDF-SCM v{}\n"
        "File written with: pymagicc v{} (more info at "
        "github.com/openclimatedata/pymagicc)\n".format(
            dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            contact,
            netcdf_scm_version,
            pymagicc.__version__,
        )
    )

    return header


def _take_area_sum(openscmrun, current_unit):
    converted_ts = []

    for region, df in openscmrun.timeseries().groupby("region"):
        rkey = ScmCube._convert_region_to_area_key(  # pylint:disable=protected-access
            region
        )
        for k, v in openscmrun.metadata.items():
            if "{} (".format(rkey) in k:
                unit = k.split("(")[-1].split(")")[0]
                conv_factor = v * _ureg(unit)

                converted_region = df * v
                converted_region = converted_region.reset_index()
                converted_region["unit"] = str(
                    (1 * _ureg(current_unit) * conv_factor).units
                )
                converted_ts.append(ScmRun(converted_region))
                break

    converted_ts = run_append(converted_ts)
    converted_ts.metadata = openscmrun.metadata
    return converted_ts
