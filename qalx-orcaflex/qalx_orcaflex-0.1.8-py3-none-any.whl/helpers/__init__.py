"""
.. automodule:: qalx_orcaflex.helpers.smart_statics
    :members:

General Helper Functions
~~~~~~~~~~~~~~~~~~~~~~~~
"""
import json
import time
import collections
from enum import Enum
from logging import getLogger
from os import PathLike
from pathlib import Path
from platform import node
from typing import Iterable, Callable, Mapping, Sequence, Union

import OrcFxAPI
import numpy as np
import yaml
from pyqalx import Item

from qalx_orcaflex.data_models import (
    RangeGraph,
    TimeHistory,
    OrcaFlexJob,
    OrcaFlexJobOptions,
)

logger = getLogger("pyqalx.core")


def append_node(name, dt=False):
    """adds node string for uniqueness, option to include datetime string

    :param name: original name
    :param dt: include datetime
    :type dt: bool
    :return: str
    """
    if dt:
        return f"{name} @ {node()} [{time.time()}]"
    else:
        return f"{name} @ {node()}"


def data_file_paths(
    directory: Union[PathLike, Sequence[PathLike]],
    include_yaml: bool,
    skip_fails: bool,
    recursive: bool,
):
    """return paths to all QalxOrcaFlex data files in a directory

    :param directory: path to search
    :type directory: str, pathlib.Path, list, tuple
    :param include_yaml: search for .yml and .yaml
    :param skip_fails: raise a FileNotFound error if path does not exist (default=True)
    :param recursive: recursively search subfolders
    :return: list of pathlib.Path
    """
    data_file_paths = []
    if include_yaml:
        suffixes = [".dat", ".yml", ".yaml"]
    else:
        suffixes = [".dat"]

    def valid_path(path_like):
        try:
            source_path = Path(path_like)
            if source_path.exists():
                return source_path
            elif skip_fails:
                return False
            else:
                raise FileNotFoundError(f"could not find {path_like}")
        except TypeError as err:
            if skip_fails:
                return False
            else:
                raise err

    def add_data_file_paths(directory_path):
        if recursive:
            glob_strs = ["**/*" + suf for suf in suffixes]
        else:
            glob_strs = ["*" + suf for suf in suffixes]

        for glob_str in glob_strs:
            for p in Path(directory_path).glob(glob_str):
                data_file_paths.append(p)

    def add_directory_or_path(path_like):
        path = valid_path(path_like)
        if path and path.is_dir():
            add_data_file_paths(path)
        elif path and (path.suffix in suffixes):
            data_file_paths.append(path)

    if isinstance(directory, (str, Path)):
        add_directory_or_path(directory)
    elif isinstance(directory, Iterable):
        for s in directory:
            add_directory_or_path(s)
    else:
        raise TypeError("source needs be str, Path or iterable of such objects")

    return data_file_paths


def check_licence():
    """true if a licence can be found
    Useful for polling to wait for a free licence."""
    try:
        OrcFxAPI.Model()
        return True
    except OrcFxAPI.DLLError as err:
        if err.status == OrcFxAPI.stLicensingError:
            return False
        else:
            raise err


def nice_time(s: float) -> str:
    """makes a pretty time string from a number of seconds"""
    if s <= 1e10:
        t = time.gmtime(s)
        mins = time.strftime("%M", t).lstrip("0")
        secs = time.strftime("%S", t).lstrip("0")
        hours = time.strftime("%H", t).lstrip("0")
        if s < 60:
            return "{}s".format(secs)
        elif s < 3600:
            if int(mins) == 1:
                return "{}min, {}s".format(mins, secs)
            else:
                return "{}mins, {}s".format(mins, secs)
        else:
            if int(hours) == 1:
                return "{}hr, {}mins".format(hours, mins)
            else:
                return "{}hrs, {}mins, {}s".format(hours, mins, secs)


def model_simulation_size(model: OrcFxAPI.Model) -> float:
    """estimates simulation size in megabytes from a reset model

    :param model: model to estimate
    :type model: OrcFxAPI.Model
    :return: megabytes size
    """

    buoys = [o for o in model.objects if o.typeName == "6DBuoy"] + [
        o for o in model.objects if o.typeName == "3DBuoy"
    ]
    shapes = [o for o in model.objects if o.typeName == "Shape"]
    vessels = [o for o in model.objects if o.typeName == "Vessel"]
    lines = [o for o in model.objects if o.typeName == "Line"]
    line_nodes = sum([line.CumulativeNumberOfSegments[-1] for line in lines])
    logged_var_count = 0

    for line in lines:
        for i, segments in enumerate(line.NumberOfSegments):
            vars_ = 4
            if line.IncludeTorsion == "Yes":
                vars_ += 4
            if line.ClashCheck[i]:
                vars_ += 3
            logged_var_count += segments * vars_

    contact_lines = set(
        [sl for sl in model["Line Contact Data"].SplinedLine]
        + [pl for pl in model["Line Contact Data"].PenetratingLine]
    )

    logged_var_count += 3 * sum(
        [
            line.CumulativeNumberOfSegments[-1]
            for line in lines
            if line.Name in contact_lines
        ]
    )

    for _ in vessels + buoys:
        logged_var_count += 120

    if any(
        [
            (shape.ShapeType == "Elastic Solid") and (shape.NormalStiffness > 0)
            for shape in shapes
        ]
    ):
        logged_var_count += line_nodes

    t_actual_sample = model.general.ActualLogSampleInterval
    t_simulation = sum(model.general.StageDuration)

    if model.general.LogPrecision == "Single":
        bytes_float = 4
    else:
        bytes_float = 8

    logged_bytes = bytes_float * logged_var_count

    time_steps = t_simulation / t_actual_sample

    bytes_log = time_steps * logged_bytes

    return bytes_log / 1024  # in MB


class Spreading(Enum):
    linear = 1
    exponential = 2
    random = 3
    constant = 4


class ModelWithLicence:
    """context manager to poll for a licence if one is not available

    If a licence is available then

    >>> with ModelWithLicence(max_attempts=10, wait_lower=5) as model:
    ...     model.RunSimulation()

    Will run the simulation immediately. However, suppose that all the licences are being used in that case
    the above code will not move to `model.RunSimulation` until it has tried 10 times. The shortest wait will
    be 5 seconds and the wait will grow exponetially.

    There are other options to control how the wait between attempts will spread.
    """

    __slots__ = ("max_attempts", "wait_lower", "wait_upper", "spreading", "_model")

    def __init__(
        self,
        max_attempts: int,
        wait_lower: int,
        wait_upper: int = None,
        spreading: Spreading = Spreading.exponential,
    ):
        """set up a context manager to only return an OrcFxAPI.Model when there is a licence.

        The polling interval is controlled by and instance of helpers.Spreading and `wait_lower` and `wait_upper`.

        There are four options:

        1. Linear; the first wait will be `wait_lower` seconds and the final attempt will be `wait_upper` and
            there will be equal increments determined by `max_attempts`
        2. Exponential; the first wait will be `wait_lower` seconds and the final attempt will be `wait_upper` and
            there will be an exponential increase determined by `max_attempts`. i.e. there will be very frequent
            attempts at first but these will become far more spaced out
        3. Random; `max_attempts` will be made at random intervals between `wait_lower` and `wait_upper`
        4. Constant; wait `wait_lower` seconds `max_attempts` times

        :param max_attempts: number of attempts should we make to get a licence
        :param wait_lower: the shortest wait time in seconds
        :param wait_upper: the longest wait time in seconds
        :param spreading: an instance of `helpers.Spreading`
        """
        self.max_attempts = max_attempts
        self.wait_lower = wait_lower
        if wait_upper is None:
            self.wait_upper = wait_lower
            self.spreading = Spreading.linear
        else:
            self.wait_upper = wait_upper
            if not isinstance(spreading, Spreading):
                raise TypeError("spreading needs to be a helpers.Spreading")
            else:
                self.spreading = spreading

        self._model = None

    def spread(self):
        """generator which yields the time in seconds to wait"""
        if self.spreading == Spreading.exponential:
            start = np.log(self.wait_lower) / np.log(
                10
            )  # define start and end points for logarithmic growth
            end = np.log(self.wait_upper) / np.log(10)
            for attempt_sleep in np.logspace(start, end, self.max_attempts):
                yield attempt_sleep
        elif self.spreading == Spreading.linear:
            for attempt_sleep in np.linspace(
                self.wait_lower, self.wait_upper, self.max_attempts
            ):
                yield attempt_sleep
        elif self.spreading == Spreading.random:
            for attempt_sleep in self.wait_lower + np.random.random(
                self.max_attempts
            ) * (self.wait_upper - self.wait_lower):
                yield attempt_sleep
        elif self.spreading == Spreading.constant:
            for _ in range(self.max_attempts):
                yield self.wait_lower

    def __enter__(self):

        for wait in self.spread():
            try:
                self._model = OrcFxAPI.Model(
                    threadCount=1
                )  # threadCount very important!
                return self._model
            except OrcFxAPI.DLLError as err:
                if err.status == OrcFxAPI.stLicensingError:
                    logger.error(f"waiting {wait}s for an QalxOrcaFlex Licence")
                    time.sleep(wait)
                else:
                    raise err

        raise ConnectionError(
            f"Did not get a licence after {self.max_attempts} attempts"
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def add_data_files(
    session,
    path,
    include_yaml=False,
    skip_fails=False,
    recursive=False,
    extra_data=None,
    meta=None,
) -> Sequence[Item]:
    """adds datafiles to qalx and returns list of qalx items

    :return:
    """
    data_file_items = []
    if extra_data is not None:
        data = extra_data
    else:
        data = {}
    if meta is None:
        meta = {}
    for dfp in data_file_paths(path, include_yaml, skip_fails, recursive):
        meta["_class"] = "orcaflex.job.data_file"
        meta["data_file_path"] = str(dfp)
        meta["data_file_name"] = dfp.name
        meta["data_file_drive"] = dfp.drive
        meta["data_file_uri"] = dfp.as_uri()
        item = session.item.add(source=str(dfp), data=data, meta=meta)
        data_file_items.append(item)

    return data_file_items


def load_model_data(
    orcaflex_job: OrcaFlexJob, job_options: OrcaFlexJobOptions
) -> OrcFxAPI.Model:
    """take the job and options and return a model using helpers.ModelWithLicence"""
    with ModelWithLicence(
        job_options.licence_attempts, 10, job_options.max_wait
    ) as model:
        if orcaflex_job.data_file_path:
            model.LoadData(orcaflex_job.data_file_path["data"]["full_path"])
            return model
        elif orcaflex_job.data_file:
            model.LoadDataMem(orcaflex_job.data_file.read_file())
            return model
        else:
            raise AttributeError("orcaflex_job must have a data_file or data_file_path")


def result_name(
    n: int,
    ofx_obj: OrcFxAPI.OrcaFlexObject,
    res_type: int,
    result_name: str,
    oe: OrcFxAPI.ObjectExtra,
) -> str:
    """make a unique string for the result, if available will use the FullName given by OrcaFlex"""
    var_details = ofx_obj.varDetails(resultType=res_type, objectExtra=oe)
    this_res = [v for v in var_details if v.VarName.lower() == result_name.lower()]
    if len(this_res) != 1:
        return f"r#{n}: {ofx_obj.name} {str(res_type)} {result_name}"
    else:
        return f"r#{n}: {this_res[0].FullName.replace('.', '')}"


def result_details(
    ofx_obj: OrcFxAPI.OrcaFlexObject,
    res_type: int,
    result_name: str,
    oe: OrcFxAPI.ObjectExtra,
) -> Union[None, Mapping]:
    """tries to get the details of the result variable from OrcaFlex if not avilable then returns None"""
    var_details = ofx_obj.varDetails(resultType=res_type, objectExtra=oe)
    this_res = [v for v in var_details if v.VarName.lower() == result_name.lower()]
    if len(this_res) != 1:
        return None
    else:
        return {
            "var_name": this_res[0].VarName,
            "units": this_res[0].VarUnits,
            "full_name": this_res[0].FullName,
        }


def clean_set_key(dirty_key: str) -> str:
    """get a clean key for items in a set (`$` and `.` are disallowed)

    :param dirty_key:
    :return: str: clean key
    """
    return dirty_key.replace("@", "_at_").replace(".", "_")


def get_tags(
    model: OrcFxAPI.Model,
    tag_filter: Callable = lambda _: True,
    from_json: bool = False,
) -> Mapping:
    """create mapping of object name to tags in entire model

    :param model: model to process
    :param tag_filter: callable to be passed tag name, should return True if
        tag is to be processed
    :param from_json: parse the tag value as json
    :return: dict of ObjectName -> TagNames -> TagValues
    """
    all_tags = collections.defaultdict(dict)
    for o in filter(lambda obj: obj.tags, model.objects):
        # Filter the tags to only be those tags that match the tag_filter (if specified)
        filtered_tags = dict(filter(lambda item: tag_filter(item[0]), o.tags.items()))
        for k, v in filtered_tags.items():
            all_tags[o.name][k] = json.loads(v) if from_json else v
    return all_tags


def required_results_from_yaml(
    filepath: PathLike,
) -> Sequence[Union[RangeGraph, TimeHistory]]:
    """make a dict from a results yaml

    :param filepath:
    :return: list of required results
    """
    with open(filepath, "r") as fs:
        results = yaml.full_load(fs)
    rr = []
    for result in results["Results"]:
        if "RangeGraph" in result:
            rr.append(RangeGraph.from_dict(result["RangeGraph"]))
        elif "TimeHistory" in result:
            rr.append(TimeHistory.from_dict(result["TimeHistory"]))
    return rr
