"""
Module for stitching netCDF-SCM netCDF files together

'Stitching' here means combining results from multiple experiments e.g.
combining historical and scenario experiments. This relies on the 'parent'
conventions within CMIP experiments which define the experiment from which
a given set of output started (in CMIP language, the experiment from which
a given experiment 'branched').
"""
import copy
import datetime as dt
import glob
import logging
import os.path
import re

import click
import numpy as np
import pandas as pd
from scmdata import ScmRun, run_append

from .cli_parallel import _apply_func
from .cli_utils import (
    _convert_units,
    _find_dirs_meeting_func,
    _get_openscmdf_header,
    _get_outfile_dir,
    _get_path_bits,
    _write_ascii_file,
)
from .io import load_scmrun
from .normalisation import get_normaliser

try:
    import netCDF4
except ModuleNotFoundError:  # pragma: no cover # emergency valve
    from .errors import raise_no_iris_warning

    raise_no_iris_warning()


logger_stitching = logging.getLogger(__name__)


def _stitch_netcdf_scm_ncs(  # pylint:disable=too-many-arguments
    src,
    dst,
    stitch_contact,
    regexp,
    prefix,
    out_format,
    drs,
    force,
    number_workers,
    target_units_specs,
    normalise,
):
    regexp_compiled = re.compile(regexp)
    if target_units_specs is not None:
        target_units_specs = pd.read_csv(target_units_specs)

    crunch_list, failures_dir_finding = _find_dirs_meeting_func(
        src, regexp_compiled.match
    )

    failures_wrangling = _apply_func(
        _stitch_magicc_files,
        [{"fnames": f, "dpath": d} for d, f in crunch_list],
        common_kwarglist={
            "dst": dst,
            "force": force,
            "out_format": out_format,
            "target_units_specs": target_units_specs,
            "stitch_contact": stitch_contact,
            "drs": drs,
            "prefix": prefix,
            "normalise": normalise,
        },
        n_workers=number_workers,
        style="processes",
    )

    if failures_dir_finding or failures_wrangling:
        raise click.ClickException(
            "Some files failed to process. See the logs for more details"
        )


def _stitch_magicc_files(  # pylint:disable=too-many-arguments
    fnames,
    dpath,
    dst,
    force,
    out_format,
    target_units_specs,
    stitch_contact,
    drs,
    prefix,
    normalise,
):
    logger_stitching.info("Attempting to process: %s", fnames)
    openscmrun, metadata, header = _get_stitched_openscmdf_metadata_header(
        fnames, dpath, target_units_specs, stitch_contact, drs, normalise
    )

    outfile_dir = _get_outfile_dir(dpath, drs, dst)

    _write_ascii_file(
        openscmrun,
        metadata,
        header,
        outfile_dir,
        fnames,
        force,
        out_format,
        drs,
        prefix=prefix,
    )


def _get_stitched_openscmdf_metadata_header(  # pylint:disable=too-many-arguments
    fnames, dpath, target_units_specs, stitch_contact, drs, normalise
):
    if len(fnames) > 1:
        raise AssertionError(
            "more than one file to wrangle?"
        )  # pragma: no cover # emergency valve

    fullpath = os.path.join(dpath, fnames[0])
    (
        openscmrun,
        picontrol_branching_time,
        picontrol_file,
    ) = get_continuous_timeseries_with_meta(
        fullpath, drs, return_picontrol_info=normalise is not None
    )

    if normalise is not None:
        openscmrun = _normalise_timeseries_against_picontrol(
            openscmrun, picontrol_branching_time, picontrol_file, drs, normalise
        )

    if target_units_specs is not None:
        openscmrun = _convert_units(openscmrun, target_units_specs)

    metadata = openscmrun.metadata
    try:
        header = _get_openscmdf_header(
            stitch_contact, metadata["(child) crunch_netcdf_scm_version"]
        )
    except KeyError:  # pragma: no cover # for future
        if normalise is not None:  # pragma: no cover
            raise AssertionError("Normalisation metadata should be included...")

        if "piControl" not in metadata["parent_experiment_id"]:  # pragma: no cover
            raise AssertionError("Stitching should have occured no?")

        logger_stitching.info(
            "No normalisation is being done and the parent of %s is %s for infile: %s",
            metadata["experiment_id"],
            metadata["parent_experiment_id"],
            os.path.join(dpath, fnames[0]),
        )

        header = _get_openscmdf_header(
            stitch_contact, metadata["crunch_netcdf_scm_version"]
        )

    return openscmrun, metadata, header


def get_continuous_timeseries_with_meta(infile, drs, return_picontrol_info=True):
    """
    Load a continuous timeseries with metadata

    Continuous here means including all parent experiments up to (but not
    including) piControl

    Parameters
    ----------
    infile : str
        netCDF-SCM crunched file to load

    drs : str
        Data reference syntax which applies to this file

    return_picontrol_info : bool
        If supplied, piControl information will be returned in the second
        and third outputs if available (rather than ``None``). A caveat is that
        if the experiment itself is a piControl experiment, ``None`` will be
        returned in the second and third outputs.

    Returns
    -------
    :obj:`scmdata.ScmRun`
        Loaded timseries, including metadata

    :obj:`dt.datetime`
        Branch time from piControl. If ``infile`` points to a piControl or
        piControl-spinup experiment  then this will be ``None``.

    str
        Path from which the piControl data was loaded. If ``infile`` points to a
        piControl or piControl-spinup experiment  then this will be ``None``.
    """
    loaded = _load_scmrun_and_add_source_file(infile, drs)

    parent_replacements = get_parent_replacements(loaded)
    if not parent_replacements:  # pragma: no cover # emergency valve
        return loaded

    pexp_id = parent_replacements["parent_experiment_id"]
    if pexp_id.endswith("piControl"):
        # don't need to look any further
        if not return_picontrol_info:
            return loaded, None, None

        picontrol_file = get_parent_file_path(infile, parent_replacements, drs)
        picontrol_branching_time = get_branch_time(
            loaded, parent=True, parent_path=picontrol_file
        )
        return loaded, picontrol_branching_time, picontrol_file

    if pexp_id.endswith("piControl-spinup") or (pexp_id == "N/A"):
        # hard-code return at piControl-spinup for now, we don't care about spinup
        return loaded, None, None

    parent_file_path = get_parent_file_path(infile, parent_replacements, drs)

    (
        parent,
        picontrol_branching_time,
        picontrol_file,
    ) = get_continuous_timeseries_with_meta(
        parent_file_path, drs, return_picontrol_info
    )

    return (
        _do_stitching(loaded, parent, infile),
        picontrol_branching_time,
        picontrol_file,
    )


def _load_scmrun_and_add_source_file(infile, drs):
    loaded = load_scmrun(infile)
    loaded.metadata["netcdf-scm crunched file"] = infile.replace(
        os.path.join("{}/".format((_get_path_bits(infile, drs)["root_dir"]))), ""
    )

    return loaded


def get_parent_replacements(scmdf):
    """
    Get changes in metadata required to identify a dataset's parent file

    Parameters
    ----------
    scmdf : :obj:`scmdata.ScmRun`
        Dataset of which to identify the parent file

    Returns
    -------
    dict of str : str
        Replacements which must be made to the dataset's metadata in order to
        identify its parent file

    Raises
    ------
    KeyError
        The variant label (e.g. r1i1p1f1) of the parent dataset is missing
    """
    if scmdf.get_unique_meta("mip_era", no_duplicates=True) == "CMIP5":
        parent_keys = [
            "parent_experiment",
            "parent_experiment_id",
            "parent_experiment_rip",
        ]
        replacements = {k: v for k, v in scmdf.metadata.items() if k in parent_keys}
        try:
            replacements["parent_ensemble_member"] = replacements.pop(
                "parent_experiment_rip"
            )
        except KeyError:
            raise KeyError("No `parent_experiment_rip` in metadata")

    else:
        parent_keys = [
            "parent_activity_id",
            "parent_experiment_id",
            "parent_mip_era",
            "parent_source_id",
            "parent_variant_label",
        ]

        replacements = {
            k: v.replace(" ", "") for k, v in scmdf.metadata.items() if k in parent_keys
        }

        # change in language since I wrote netcdf-scm, this is why using
        # ESMValTool instead would be helpful, we would have extra helpers to
        # know when this sort of stuff changes...
        try:
            replacements["parent_member_id"] = replacements.pop("parent_variant_label")
        except KeyError:
            raise KeyError("No `parent_variant_label` in metadata")

    return replacements


def get_parent_file_path(infile, parent_replacements, drs):
    """
    Get parent file path for a given file

    Parameters
    ----------
    infile : str
        File path of which to get the parent

    parent_replacements : dict of str : str
        Replacements to insert in ``infile`` to determine the parent filepath

    drs : str
        Data reference syntax which is applicable to these filepaths

    Returns
    -------
    str
        Path of the parent file

    Raises
    ------
    IOError
        Parent data cannot be found

    AssertionError
        More than one parent datafile is found
    """
    # TODO: write a more user friendly function that just takes infile as an
    # argument and has its paths and failures tested more completely

    parent_file_path_base = _get_parent_path_base(infile, parent_replacements, drs)
    parent_file_path = glob.glob(parent_file_path_base)
    if np.equal(len(parent_file_path), 0):
        raise IOError(
            "No parent data ({}) available for {}, we looked in {}".format(
                parent_replacements["parent_experiment_id"],
                infile,
                parent_file_path_base,
            )
        )

    if len(parent_file_path) > 1:
        raise AssertionError(  # pragma: no cover # emergency valve
            "More than one parent file?"
        )

    return parent_file_path[0]


def _get_parent_path_base(child_path, replacements_in, drs):
    replacements = copy.deepcopy(replacements_in)
    if drs == "MarbleCMIP5":
        replacements["parent_experiment"] = replacements.pop("parent_experiment_id")

    parent_path = copy.copy(child_path)
    for k, v in replacements.items():
        pid = k.replace("parent_", "")

        parent_path = parent_path.replace(_get_path_bits(child_path, drs)[pid], v)

    timestamp_str = _get_path_bits(child_path, drs, include_time_info=True)[
        "timestamp_str"
    ]

    parent_path_base = "{}*.nc".format(parent_path.split(timestamp_str)[0])

    path_bits = _get_path_bits(child_path, drs)
    if "version" in path_bits:
        parent_path_base = parent_path_base.replace(path_bits["version"], "*")

    return parent_path_base


def _do_stitching(loaded, parent, source_path):
    cmip5 = loaded.get_unique_meta("mip_era", no_duplicates=True) == "CMIP5"
    if not cmip5:
        # we have the information to check that things line up as expected so let's do it
        branch_time_in_parent = get_branch_time(loaded, parent=True)
        branch_time = get_branch_time(loaded, parent=False, source_path=source_path)

        if branch_time != branch_time_in_parent:
            raise NotImplementedError(
                "Time axes should be adjusted before stitching timeseries"
            )

    else:
        logger_stitching.debug(
            "CMIP5 data does not have enough information to check if any adjustment to "
            "time axes is required before stitching the timeseries (hence we make no "
            "such check)"
        )

    # join the two, making sure we prioritise data from what we've loaded over the
    # parent data
    out = run_append(
        [loaded, parent.filter(year=loaded["year"].unique().tolist(), keep=False)]
    )

    out = _make_metadata_uniform(
        out, loaded.get_unique_meta("scenario", no_duplicates=True)
    )

    if any(["(child)" in k for k in parent.metadata]):
        parent_metadata = {
            step_up_family_tree(k): v for k, v in parent.metadata.items()
        }
        out.metadata = {
            **{"(child) {}".format(k): v for k, v in loaded.metadata.items()},
            **parent_metadata,
        }

    else:
        out.metadata = {
            **{"(child) {}".format(k): v for k, v in loaded.metadata.items()},
            **{"(parent) {}".format(k): v for k, v in parent.metadata.items()},
        }

    return out


def _make_metadata_uniform(inscmrun, base_scen):
    """Make metadata uniform for ease of plotting etc."""
    base_scmdf = inscmrun.filter(scenario=base_scen)
    cols_to_blend = ["region", "variable", "unit"]
    meta_cols = [c for c in base_scmdf.meta.columns if c not in cols_to_blend]
    meta_order = meta_cols + cols_to_blend

    outscmruns = []
    for scenrun in inscmrun.groupby("scenario"):
        scenrun = scenrun.copy()  # don't mangle source parent_metadata
        for meta_col in meta_cols:
            new_meta = base_scmdf.get_unique_meta(meta_col, no_duplicates=True)
            scenrun[meta_col] = new_meta

        outscmruns.append(
            scenrun.timeseries(meta=meta_order).dropna(how="all", axis="columns")
        )

    joint_df = pd.concat(outscmruns, sort=True, axis=1)
    return ScmRun(joint_df)


def _normalise_timeseries_against_picontrol(
    openscmrun, picontrol_branching_time, picontrol_file, drs, normalise
):
    picontrolscmdf = _load_scmrun_and_add_source_file(picontrol_file, drs)

    normaliser = get_normaliser(normalise)

    return normaliser.normalise_against_picontrol(
        openscmrun, picontrolscmdf, picontrol_branching_time
    )


def get_branch_time(openscmrun, parent=True, source_path=None, parent_path=None):
    """
    Get branch time of an experiment

    Parameters
    ----------
    openscmrun : :obj:`scmdata.ScmRun`
        Data of which to get the branch time

    parent : bool
        Should I get the branch time in the parent experiment's time
        co-ordinates? If ``False``, return the branch time in the child (i.e.
        ``openscmrun``'s) time co-ordinates.

    source_path : str
        Path to the data file from which ``openscmrun`` is derived. This is
        only required if ``parent`` is ``False``. It is needed because
        information about the time calendar and units of the data in
        ``openscmrun`` is only available in the source file.

    parent_path : str
        Path to the data file containing the parent data of ``openscmrun``. This
        is only required if the data is from CMIP5 because CMIP5 data does not
        store information about the parent experiment's time calendar and
        units.

    Returns
    -------
    :obj:`datetime.datetime`
        The branch time, rounded to the nearest year, month and day. netCDF-SCM
        is not designed for very precise calculations, if you need to keep finer
        information, please raise an issue on our issue tracker to discuss.

    Raises
    ------
    ValueError
        ``parent is not True`` and the data is CMIP5 data. It is impossible to
        determine the branch time in the child time co-ordinates from CMIP5 data
        because of a lack of information.

    ValueError
        ``parent_path is None`` and the data is CMIP5 data. You must supply the
        parent path if the data is CMIP5 data because the parent file is the only
        place the parent experiment's time units and calendar information is
        available.
    """
    cmip5 = openscmrun.get_unique_meta("mip_era", no_duplicates=True) == "CMIP5"

    if parent:
        bt_key = "branch_time" if cmip5 else "branch_time_in_parent"
    else:
        bt_key = "branch_time" if cmip5 else "branch_time_in_child"

    if cmip5:
        if not parent:
            raise ValueError(
                "CMIP5 data does not contain information about the branch time "
                "in the child's time axis"
            )

        if parent_path is None:
            raise ValueError("If using cmip5 data, you must provide `parent_path`")

        # have to use file, info not in metadata
        nc = netCDF4.Dataset(parent_path)
        branch_time = netCDF4.num2date(
            openscmrun.metadata[bt_key],
            nc.variables["time"].units,
            nc.variables["time"].calendar,
        )

    elif "BCC" in openscmrun.metadata["source_id"] and not np.equal(
        openscmrun.metadata[bt_key], 0
    ):
        # think the metadata here is wrong as historical has a branch_time_in_parent
        # of 2015 so assuming this means the year of the branch not the actual time
        # in days (like it's meant to)
        warn_str = (
            "Assuming BCC metadata is wrong and branch time units are actually years, "
            "not days"
        )
        logger_stitching.warning(warn_str)
        branch_time = dt.datetime(int(openscmrun.metadata[bt_key]), 1, 1)

    else:
        if not parent:
            if source_path is None:
                raise ValueError(
                    "If not requesting parent data, you must provide `source_path`"
                )

            nc = netCDF4.Dataset(source_path)
            time_units = nc.variables["time"].units
            time_calendar = nc.variables["time"].calendar

        else:
            time_units = openscmrun.metadata["parent_time_units"]
            time_calendar = openscmrun.metadata["calendar"]

        branch_time = netCDF4.num2date(  # pylint:disable=no-member
            openscmrun.metadata[bt_key], time_units, time_calendar,
        )

    branch_time = dt.datetime(branch_time.year, branch_time.month, branch_time.day)

    return branch_time


def step_up_family_tree(in_level):
    """
    Step name up the family tree

    Parameters
    ----------
    in_level : str
        Level from which to step up

    Returns
    -------
    str
        Level one up from ``in_level``

    Examples
    --------
    >>> step_up_family_tree("(child)")
    "(parent)"

    >>> step_up_family_tree("(parent)")
    "(grandparent)"

    >>> step_up_family_tree("(grandparent)")
    "(grandparent)"

    >>> step_up_family_tree("(greatgreatgrandparent)")
    "(greatgreatgreatgrandparent)"
    """
    if "(child)" in in_level:
        return in_level.replace("(child)", "(parent)")

    if "(parent)" in in_level:
        return in_level.replace("(parent)", "(grandparent)")

    return in_level.replace("grandparent)", "greatgrandparent)")
