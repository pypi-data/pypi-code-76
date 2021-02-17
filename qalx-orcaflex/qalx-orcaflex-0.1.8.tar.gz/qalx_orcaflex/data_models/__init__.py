"""
Models
~~~~~~

This is set of `dataclass` classes that help define elements of the system.

These data_models are used to be able to easily construct data structures that are
required for the OrcaFlex simulation processing system to work.

Some of these data_models can be used at the definition stage where you are required to
set some options or settings, provide source data or pre-specify some thing that you
need to have processed once the simulation is finished.

Other data_models are used by the system to populate data structures during or post
processing of the simulation.

"""
import ctypes as ct
from dataclasses import dataclass, field, asdict, fields
from enum import Enum
from typing import List, Mapping, Any, Tuple, Sequence

import OrcFxAPI
from pyqalx.core.entities import Item

from .notifications import Notifications
from ..video import DEFAULT_WIDTH, DEFAULT_HEIGHT

OE_LINE_PT = {
    "End A": OrcFxAPI.ptEndA,
    "End B": OrcFxAPI.ptEndB,
    "Touchdown": OrcFxAPI.ptTouchdown,
    "NodeNum": OrcFxAPI.ptNodeNum,
    "ArcLength": OrcFxAPI.ptArcLength,
}

OE_RADIAL = {
    "Inner": OrcFxAPI.rpInner,
    "Mid": OrcFxAPI.rpMid,
    "Outer": OrcFxAPI.rpOuter,
}


def rehydrate_dataclass(klass, d):
    """
    https://stackoverflow.com/a/54769644/11984516
    Rehydrates a dictionary into the given dataclass.  Handles rehydrating nested dataclasses.
    :param klass: The dataclasses class that will be rehydrated
    :param d: The dict to use for the source data
    """
    try:
        fieldtypes = {f.name: f.type for f in fields(klass)}
        return klass(**{f: rehydrate_dataclass(fieldtypes[f], d[f]) for f in d})
    except TypeError:
        # TypeError: Not a dataclass field, probably an attribute on the class
        return d


@dataclass
class OrcaFlexJobOptions:
    """Options for an OrcaFlex job

    :param time_to_wait [int]: jobs will pause for this number of second before
        starting (default = 0)
    :param record_progress [bool]: send updates on simulation progress (default = True)
    :param killable [bool]: can a kill signal be sent to the job? (default = False)
    :param save_simulation [bool]: save the simulation in qalx (default = True)
    :param licence_attempts [int]: number of time to try getting a licence before
        failing (default = 3600)
    :param max_search_attempts [int]: number or attempts at static search (default = 10)
    :param max_wait [int]: the longest to wait before trying to
        (default = 60)
    :param update_interval [int]: the number of seconds to wait between updating on
        model progress (default=5)
    """

    time_to_wait: int = 0
    record_progress: bool = True
    killable: bool = False
    save_simulation: bool = True
    licence_attempts: int = 3600
    max_search_attempts: int = 10
    max_wait: int = 60
    update_interval: int = 5


class JobState(Enum):
    NEW = "New"  # When a job has been created
    QUEUED = "Queued"  # When the job has been added to the queue
    PRE_PROCESSING = "Pre-processing"  # The job has been loaded by a bot
    PROCESSING = "Processing"  # The job is about to be run bot
    LOADING_MODEL_DATA = "Loading model data"  # The model data is about to be loaded
    MODEL_DATA_LOADED = "Model data loaded"  # The model data has loaded
    RUNNING_STATICS = "Running statics"  # Trying to find a static solution
    STATICS_FAILED = "Statics failed"  # Couldn't find a static solution
    RUNNING_DYNAMICS = "Running dynamics"  # Running simulation dynamics
    SAVING_SIMULATION = "Saving simulation"  # Saving the simulation data to qalx
    SIMULATION_SAVED = "Simulation saved"  # Simulation data saved
    EXTRACTING_RESULTS = "Extracting results"  # Extracting results
    RESULTS_EXTRACTED = "Results extracted"  # All results extracted
    EXTRACTING_MODEL_VIEWS = "Extracting model views"  # Extracting model views
    MODEL_VIEWS_EXTRACTED = "Model views extracted"  # All model views extracted
    EXTRACTING_MODEL_VIDEOS = "Extracting model videos"  # Extracting videos
    MODEL_VIDEOS_EXTRACTED = "Model videos extracted"  # Videos extracted
    SIMULATION_UNSTABLE = "Simulation unstable"  # Simulation was unstable
    ERROR = "Error"  # There was an error
    USER_CANCELLED = "User cancelled"  # A user cancelled the job


@dataclass
class OrcaFlexJobState:
    """the current state of an OrcaFlex job

    :param state [str]: Current state of the job (default="New")
    :param info [str]: info about the state (default=None)
    :param error [str]: error text is the state is rror (default=None)
    """

    state: str = field(default=JobState.NEW.value)
    info: str = None
    error: str = None


@dataclass
class BatchOptions:
    """options for a batch

    :param batch_queue[str]: name of the batch queue
    :param sim_queue[str]: name of the simulation queue
    :param wait_between_completion_checks[int]: how long to wait before checking for
        completion (default=30)
    :param summarise_results[bool]: should we create a results summary automatically
        (default=True)
    :param build_threads[int]: threads to use to build the batch(default=10)
    :param send_sim_to [list]: queues to send sims to when ``SimBot`` is finished
    :param send_batch_to [list]: queues to send batches to when ``BatchBot`` is finished
    :param notifications [~data_models.notifications.Notifications]: An instance of Notifications which will detail
    which notifications should be automatically sent out by the system.  (default=None)
    :param timeout: How long should this batch be processed for before timing out in seconds
    """

    batch_queue: str
    sim_queue: str
    wait_between_completion_checks: int = 30
    summarise_results: bool = True
    build_threads: int = 10
    send_sim_to: Sequence = field(default_factory=lambda: [])
    send_batch_to: Sequence = field(default_factory=lambda: [])
    notifications: Notifications = None
    timeout: int = None

    def to_valid_dict(self):
        if self.notifications:
            self.notifications.validate()
        return asdict(self)


class ValidationError(Exception):
    """That ain't valid yo'"""

    pass


@dataclass
class Period:
    """representation of Period for OrcaFlex results

    Set the attributes to tell OrcFxAPI what period to extract the results for:

    from_time & to_time -> OrcFxAPI.SpecifiedPeriod(self.from_time, self.to_time)
    named_period = "Whole Simulation" -> OrcFxAPI.Period(OrcFxAPI.pnWholeSimulation)
    named_period = "Latest Wave" -> OrcFxAPI.Period(OrcFxAPI.pnLatestWave)
    named_period = "Static State" -> OrcFxAPI.Period(OrcFxAPI.pnStaticState)
    stage_number -> OrcFxAPI.Period(self.stage_number)

    if nothing is set then -> OrcFxAPI.Period(OrcFxAPI.pnWholeSimulation)

    """

    from_time: float = None
    to_time: float = None
    stage_number: int = None
    named_period: str = None

    def to_orcfxapi(self):
        """return an OrcFxAPI.Period or similar
        """
        if self.from_time is not None:
            return OrcFxAPI.SpecifiedPeriod(self.from_time, self.to_time)
        elif self.named_period == "Whole Simulation":
            return OrcFxAPI.Period(OrcFxAPI.pnSpecifiedPeriod)
        elif self.named_period == "Latest Wave":
            return OrcFxAPI.Period(OrcFxAPI.pnLatestWave)
        elif self.named_period == "Static State":
            return OrcFxAPI.Period(OrcFxAPI.pnStaticState)
        elif self.stage_number is not None:
            return OrcFxAPI.Period(self.stage_number)
        else:
            return OrcFxAPI.Period(OrcFxAPI.pnWholeSimulation)

    def validate(self):
        both_times = (self.from_time is not None) and (self.to_time is not None)
        if both_times and (self.stage_number is not None):
            raise ValidationError("Stage number and time range given. Use only one.")
        if both_times and (self.named_period is not None):
            raise ValidationError("Named period and time range given. Use only one.")
        if self.named_period not in [
            None,
            "Whole Simulation",
            "Latest Wave",
            "Static State",
        ]:
            raise ValidationError(
                "Named period must be one of: Whole Simulation, "
                "Latest Wave or Static State."
            )
        return True

    def __str__(self):
        if (self.from_time is not None) and (self.to_time is not None):
            return "between {}s to {}s".format(self.from_time, self.to_time)
        elif self.stage_number is not None:
            return "stage {}".format(self.stage_number)
        elif self.named_period:
            return self.named_period
        else:
            return ""


@dataclass
class Support:
    """ObjectExtra specification for a Support"""

    supported_line_name: str = None
    support_index: int = 0


@dataclass
class Turbine:
    """ObjectExtra specification for a Turbine"""

    blade_arc_length: float = None
    blade_index: int = 0


@dataclass
class ResultMeta:
    """some metadata for results

    :param name [str]: Use if you want a custom name for the result (default=None)
    :param stat [str]: needs to be "min" or "max" for which is
        the limiting condition (default=None)
    :param limit [dict]: limit of result (default={})
    :param var_details[dict]: details of the result variable from OrcFxAPI (default={})
    """

    name: str = None
    stat: str = None
    limit: dict = field(default_factory=lambda: {})
    var_details: dict = field(default_factory=lambda: {})

    def hashable(self):
        return (
            self.name,
            self.stat,
            self.limit.get("max"),
            self.limit.get("min"),
            self.var_details.get("full_name"),
            self.var_details.get("units"),
        )


@dataclass
class ArcLengthRange:
    """representation of ArcLengthRange for OrcaFlex results

    from_arc & to_arc -> OrcFxAPI.arSpecifiedArclengths(self.from_arc, self.to_arc)
    from_section &  to_section ->
    OrcFxAPI.arSpecifiedSections(self.from_section, self.to_section)
    if nothing is set -> OrcFxAPI.arEntireLine()
    """

    from_arc: float = None
    to_arc: float = None
    from_section: int = None
    to_section: int = None

    def to_orcfxapi(self):
        """return an OrcFxAPI arc length range type object"""
        if self.from_arc is not None:
            return OrcFxAPI.arSpecifiedArclengths(self.from_arc, self.to_arc)
        elif self.from_section is not None:
            return OrcFxAPI.arSpecifiedSections(self.from_section, self.to_section)
        else:
            return OrcFxAPI.arEntireLine()

    def validate(self):
        both_arcs = (self.from_arc is not None) and (self.to_arc is not None)
        both_sections = (self.from_section is not None) and (
            self.to_section is not None
        )
        if [self.from_arc, self.to_arc, self.from_section, self.to_section] == [
            None,
            None,
            None,
            None,
        ]:
            return True
        elif not (both_arcs or both_sections):
            raise ValidationError("Specify either arcs or sections.")
        return True

    def __str__(self):
        _str_repr = ""
        if (self.from_section is not None) and (self.to_section is not None):

            _str_repr += "between sections {} and {} ".format(
                self.from_section, self.to_section
            )
        elif (self.from_arc is not None) and (self.to_arc is not None):
            _str_repr += "between lengths {} and {} ".format(self.from_arc, self.to_arc)
        return _str_repr


@dataclass
class ObjectExtra:
    """representation of ObejctExtra for an OrcaFlex result

    converts to orcfxapi based on the type of object that the result is called for

    For a Line:

          line_named_point='End A' -> OrcFxAPI.ptEndA
          line_named_point='End B' -> OrcFxAPI.ptEndB
          line_named_point='Touchdown' -> OrcFxAPI.ptTouchdown
          line_named_point='NodeNum' -> OrcFxAPI.ptNodeNum
          line_named_point='ArcLength' -> OrcFxAPI.ptArcLength
          line_named_point= None -> OrcFxAPI.ptArcLength

        defaults:
            line_named_point = None
            line_radial_position = "Inner"
            line_clearance_line_name = None
            line_theta = 0.0
            external_result_text = None

    For other object types:

        object_type = Environment -> OrcFxAPI.oeEnvironment(self.position)
        object_type = Vessel -> OrcFxAPI.oeVessel(self.position)
        object_type = NdBouy -> OrcFxAPI.oeBuoy(self.position)
        object_type = WingType -> OrcFxAPI.oeWing(self.wing_name)
        object_type = Winch -> OrcFxAPI.oeWinch(self.winch_connection)

    For Supports and Turbines, use the `Support` and `Turbine` data_models provided
        object_type = SupportType -> OrcFxAPI.oeSupport(self.support.support_index,
            self.support.supported_line_name)
        object_type = Turbine -> OrcFxAPI.oeTurbine(self.turbine.blade_index,
            self.turbine.blade_arc_length)

    """

    line_node: int = 0
    line_arc: float = 0.0
    line_named_point: str = None
    line_radial_position: str = "Inner"
    line_clearance_line_name: str = None
    line_theta: float = 0.0
    external_result_text: str = None
    wing_name: str = None
    winch_connection: float = 0.0
    support: Support = Support()
    turbine: Turbine = Turbine()
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    def to_orcfxapi(self, object_type):
        """based on the object_type return an ObjectExtra parameter"""
        if object_type == OrcFxAPI.otEnvironment:
            return OrcFxAPI.oeEnvironment(self.position)
        elif object_type == OrcFxAPI.otVessel:
            return OrcFxAPI.oeVessel(self.position)
        elif object_type in [OrcFxAPI.ot3DBuoy, OrcFxAPI.ot6DBuoy]:
            return OrcFxAPI.oeBuoy(self.position)
        elif object_type == OrcFxAPI.otWingType:
            return OrcFxAPI.oeWing(self.wing_name)
        elif object_type == OrcFxAPI.otWinch:
            return OrcFxAPI.oeWinch(self.winch_connection)
        elif object_type == OrcFxAPI.otSupportType:
            return OrcFxAPI.oeSupport(
                self.support.support_index, self.support.supported_line_name
            )
        elif object_type == OrcFxAPI.otTurbine:
            return OrcFxAPI.oeTurbine(
                self.turbine.blade_index, self.turbine.blade_arc_length
            )
        elif object_type == OrcFxAPI.otLine:
            if self.line_named_point is not None:
                line_point = OE_LINE_PT[self.line_named_point]
            elif self.line_node:
                line_point = OE_LINE_PT["NodeNum"]
            else:
                line_point = OE_LINE_PT["ArcLength"]
            return OrcFxAPI.oeLine(
                line_point,
                self.line_node,
                self.line_arc,
                OE_RADIAL[self.line_radial_position],
                self.line_theta,
                self.line_clearance_line_name,
                self.external_result_text,
            )
        else:
            return None

    def validate(self):
        if (self.line_node != 0) and (self.line_arc != 0.0):
            raise ValidationError("You have specified both non-zero arc and node.")
        if self.line_named_point and ((self.line_node != 0) or (self.line_arc != 0.0)):
            raise ValidationError(
                f"You have specified both a named point ({self.line_named_point})"
                f"and either an arc or node."
            )
        if self.line_named_point not in [None, "End A", "End B", "Touchdown"]:
            raise ValidationError(
                "line_named_point must be one of End A, End B or Touchdown"
            )
        if self.line_radial_position not in [None, "Inner", "Outer", "Mid"]:
            raise ValidationError(
                "line_radial_position must be one of Inner, Outer or Mid"
            )
        if len(self.position) != 3:
            raise ValidationError("position must be in the format [x, y, z]")
        return True


@dataclass
class ExtractedRangeGraph:
    """An extracted range graph"""

    arc: List[float] = None
    y_min: List[float] = None
    y_mean: List[float] = None
    y_max: List[float] = None
    y_limits: List[float] = None
    y_static: List[float] = None

    def __bool__(self):
        if [
            self.arc,
            self.y_min,
            self.y_mean,
            self.y_max,
            self.y_limits,
            self.y_static,
        ] == [None, None, None, None, None, None]:
            return False
        else:
            return True


@dataclass
class RangeGraph:
    """representation of a Range Graph OrcaFlex result


    To be specified before the simulation:
        :param object [str]: the name of the OrcaFlex object
        :param variable [str]: the name of the result variable
        :param period [Period]: period to extra the result
            (default=Period(named_period="Whole Simulation"))
        :param arc_length_range [ArcLengthRange]: arc length range to
            extract (default=ArcLengthRange())
        :param object_extra [ObjectExtra]:  (default=ObjectExtra())
        :param storm_duration_hours [float]:  (default=3.0)
        :param meta [ResultMeta]:  (default=ResultMeta())

    Available after the simulation has been post-processed:
        :param extracted [ExtractedRangeGraph]: the extracted
            (default=ExtractedRangeGraph())
    """

    object: str
    variable: str
    period: Period = Period(named_period="Whole Simulation")
    arc_length_range: ArcLengthRange = ArcLengthRange()
    extracted: ExtractedRangeGraph = ExtractedRangeGraph()
    object_extra: ObjectExtra = ObjectExtra()
    storm_duration_hours: float = 3.0
    meta: ResultMeta = ResultMeta()

    _type: str = "rg"

    def to_valid_dict(self):
        if (
            self.period.validate()
            and self.arc_length_range.validate()
            and self.object_extra.validate()
        ):
            return asdict(self)

    @classmethod
    def from_dict(cls, a_dict):
        """builds a RangeGraph from a dict"""
        return cls(
            _type="rg",
            object=a_dict["object"],
            variable=a_dict["variable"],
            period=Period(**a_dict.get("period", Period().__dict__)),
            arc_length_range=ArcLengthRange(
                **a_dict.get("arc_length_range", ArcLengthRange().__dict__)
            ),
            object_extra=ObjectExtra(
                **a_dict.get("object_extra", ObjectExtra().__dict__)
            ),
            extracted=ExtractedRangeGraph(
                **a_dict.get("extracted", ExtractedRangeGraph().__dict__)
            ),
            storm_duration_hours=a_dict.get("storm_duration_hours", 3.0),
            meta=ResultMeta(**a_dict.get("meta", ResultMeta().__dict__)),
        )

    def hashable_meta(self):
        return self.meta.hashable()


@dataclass
class ExtractedTimeHistory:
    """an extracted Time History"""

    time: List[float] = None
    y_values: List[float] = None
    y_limits: List[float] = None
    static_value: float = None

    def __bool__(self):
        if [self.time, self.y_limits, self.y_values, self.static_value] == [
            None,
            None,
            None,
            None,
        ]:
            return False
        else:
            return True


@dataclass
class TimeHistory:
    """representation of a Range Graph OrcaFlex result

    To be specified before the simulation:
        :param object [str]:
        :param variable [str]:
        :param period [Period]:
        :param object_extra [ObjectExtra]:  (default=ObjectExtra())
        :param meta [ResultMeta]:  (default=ResultMeta())

    Available after the simulation has been post-processed:
        :param extracted: ExtractedTimeHistory = ExtractedTimeHistory()
     """

    object: str
    variable: str
    period: Period
    extracted: ExtractedTimeHistory = ExtractedTimeHistory()
    object_extra: ObjectExtra = ObjectExtra()
    meta: ResultMeta = ResultMeta()

    _type: str = "th"

    @classmethod
    def from_dict(cls, a_dict):
        """builds a TimeHistory from a dict"""
        return cls(
            _type="th",
            object=a_dict["object"],
            variable=a_dict["variable"],
            period=Period(**a_dict.get("period", Period().__dict__)),
            object_extra=ObjectExtra(
                **a_dict.get("object_extra", ObjectExtra().__dict__)
            ),
            extracted=ExtractedTimeHistory(
                **a_dict.get("extracted", ExtractedTimeHistory().__dict__)
            ),
            meta=ResultMeta(**a_dict.get("meta", ResultMeta().__dict__)),
        )

    def to_valid_dict(self):
        if self.period.validate() and self.object_extra.validate():
            return asdict(self)

    def hashable_meta(self):
        return self.meta.hashable()


@dataclass
class ModelInfo:
    """information to extract from a model to aid with results presentation

    To be specified before the simulation:
        :param object_name [str]: name of the object
        :param data_name [str]: data item name
        :param item_index [int]: data item index (default=0)
        :param alias [str]: an alternate name for this variable

    Available after the simulation has been post-processed:
        :param value [Any]: the value of the specified info
    """

    object_name: str = None
    data_name: str = None
    item_index: int = 0
    alias: str = None
    value: Any = None

    @property
    def key(self):
        if self.alias is not None:
            return self.alias
        else:
            return f"{self.data_name} for {self.object_name} [{self.item_index}]"


@dataclass
class RawInfo:
    """raw information about the model not tied to any object data.

    E.g. a client reference or internal document reference

    :param key: info key
    :param value: info value
    """

    key: str = None
    value: Any = None


@dataclass
class LoadCaseInfo:
    """all additional information about a laod case

    :param raw_info: list of :ref:RawInfo
    :param model_info: list of ref:ModelInfo
    """

    raw_info: List[RawInfo] = field(default_factory=lambda: [])
    model_info: List[ModelInfo] = field(default_factory=lambda: [])

    @classmethod
    def from_dict(cls, a_dict):
        if a_dict is not None:
            return cls(
                raw_info=[RawInfo(**info) for info in a_dict.get("raw_info", [])],
                model_info=[ModelInfo(**info) for info in a_dict.get("model_info", [])],
            )
        else:
            return cls()

    def __iter__(self):
        for info in self.raw_info + self.model_info:
            yield info


@dataclass
class RangeGraphSummary:
    """summary of range graph results across a batch

    :param result_meta [dict]: some metadata about the result. SOme of this can be
        pre-specified and some is extracted post-sim
    :param max_value [float]: the maximum value of this result across all sims
    :param arc_max_value [float]: the arc of the max value
    :param max_case_info [Mapping]: the load case info for the maximum case
    :param max_result_guid [str]: the guid of the qalx item for the max result
    :param min_value [float]: the minimum value of this result across all sims
    :param arc_min_value [float]: the arc of the min value
    :param min_case_info [Mapping]: the load case info for the minimum case
    :param min_result_guid [str]: the guid of the qalx item for the min result
    :param static_max_value [float]: the static maximum value of this result across
        all sims
    :param arc_static_max_value [float]: the arc of the static max value
    :param static_max_case_info [Mapping]: the load case info for the static
        maximum case
    :param static_max_result_guid [str]: the guid of the qalx item for the
        static max result
    :param static_min_value [float]: the static minimum value of this
        result across all sims
    :param arc_static_min_value [float]: the arc of the static min value
    :param static_min_case_info [Mapping]: the load case info for the static
        minimum case
    :param static_min_result_guid [str]: the guid of the qalx item for the
        static min result
    :param vs_info [Mapping]: mappings to be able to plot results against loadcase info
    """

    result_meta: dict = None
    max_value: float = None
    arc_max_value: float = None
    max_case_info: Mapping = None
    max_result_guid: str = None
    min_value: float = None
    arc_min_value: float = None
    min_case_info: Mapping = None
    min_result_guid: str = None
    static_max_value: float = None
    arc_static_max_value: float = None
    static_max_result_guid: str = None
    static_max_case_info: Mapping = None
    static_min_value: float = None
    arc_static_min_value: float = None
    static_min_case_info: Mapping = None
    static_min_result_guid: str = None
    vs_info: Mapping = None


@dataclass
class TimeHistorySummary:
    """summary of time history results across a batch

    :param result_meta [dict]: some metadata about the result. SOme of this can be
        pre-specified and some is extracted post-sim
    :param max_value [float]: the maximum value of this result across all sims
    :param time_max_value [float]: the time of the maximum value
    :param max_case_info [Mapping]: the load case info for the maximum case
    :param max_result_guid: [str] the guid of the qalx item for the max result
    :param min_value [float]: the minimum value of this result across all sims
    :param time_min_value [float]: the time of the minimum value
    :param min_case_info [Mapping]: the load case info for the minimum case
    :param min_result_guid: [str] the guid of the qalx item for the min result
    :param vs_info [Mapping]: mappings to be able to plot results against loadcase info
    """

    result_meta: dict = None
    max_value: float = None
    time_max_value: float = None
    max_case_info: Mapping = None
    max_result_guid: str = None
    min_value: float = None
    time_min_value: float = None
    min_case_info: Mapping = None
    min_result_guid: str = None
    vs_info: Mapping = None


@dataclass
class ModelView:
    """a representation of OrcFxAPI.ViewParameters

    Despite the use of PascalCase for attributes triggering slight dev OCD this has been
    done for good reason. The only
    attribute that we've added is `ViewName` so that you can easily identify it later
    e.g. "Plan", "from Starboard", "Fish view", etc.

    The other attributes here are passed directly to OrcFxAPI.ViewParameters. Read
    more about that here if you need to:

    https://www.orcina.com/webhelp/OrcFxAPI/Content/html/Pythonreference,ViewParameters.htm

    This class has some helper methods that should allow you to copy and paste from
    the "edit view parameters" window in the OrcaFlex GUI.

    Basic process for simply defining model view then can be this:


    1. Get the view you want in the OrcaFlex GUI 2. Open edit view parameters if it's
    not open already (CTRL+W) 3. CTRL+A to select all cells 4. Give a name for the
    view and paste as a string using one of the following methods depending on what
    type of view you want:

         wire_frame_from_form_str: for wireframe views
         shaded_solid_from_form_str: for solid shaded views
         shaded_mesh_from_form_str: for shaded mesh views

    Defaults:

        GraphicsMode: "WireFrame"
        FileFormat: "PNG"
        BackgroundColour:  (0, 0, 0)
        ShadedFillMode: "Mesh"

    """

    ViewName: str
    ViewSize: float = None
    Size: None = None
    ViewAzimuth: float = None
    ViewElevation: float = None
    ViewCentre: List[float] = None
    Height: int = None
    Width: int = None
    DrawViewAxes: bool = None
    DrawScaleBar: bool = None
    DrawGlobalAxes: bool = None
    DrawEnvironmentAxes: bool = None
    DrawLocalAxes: bool = None
    DrawOutOfBalanceForces: bool = None
    DrawNodeAxes: bool = None
    GraphicsMode: str = "WireFrame"
    FileFormat: str = "PNG"
    BackgroundColour: Tuple[int, int, int] = (0, 0, 0)
    ViewGamma: float = None
    RelativeToObjectHandle: str = None
    DisturbanceVesselHandle: str = None
    DisturbancePosition: List[float] = None
    ShadedFillMode: str = "Mesh"
    DrawNameLabels: bool = None
    DrawConnections: bool = None
    LabelScale: int = None
    DrawOrigins: bool = None

    @property
    def view_filename(self):
        return f"{self.ViewName}.{self.FileFormat.lower()}"

    def _build_params(self, form_str):
        params = form_str.split("\t")
        self.RelativeToObjectHandle = params[0]
        self.ViewSize = float(params[1])
        self.ViewCentre = [float(pos) for pos in params[2:5]]
        self.ViewAzimuth = float(params[5])
        self.ViewElevation = float(params[6])
        self.ViewGamma = float(params[7])
        self.Width = int(params[8])
        self.Height = int(params[9])

    @classmethod
    def wire_frame_from_form_str(cls, view_name, form_str):
        """make a ModelView from a view name and the string from copying the "edit view
         parameters" form in OrcaFlex GUI

        :return: ModelView
        """
        mv = cls(view_name)
        mv._build_params(form_str)
        return mv

    @classmethod
    def shaded_solid_from_form_str(cls, view_name, form_str):
        """make a ModelView from a view name and the string from copying the "edit view
         parameters" form in OrcaFlex GUI

        :return: ModelView
        """
        mv = cls(view_name)
        mv._build_params(form_str)
        mv.GraphicsMode = "Shaded"
        mv.ShadedFillMode = "Solid"
        return mv

    @classmethod
    def shaded_mesh_from_form_str(cls, view_name, form_str):
        """make a ModelView from a view name and the string from copying the "edit view
        parameters" form in OrcaFlex GUI

        :return: ModelView
        """
        mv = cls(view_name)
        mv._build_params(form_str)
        mv.GraphicsMode = "Shaded"
        mv.ShadedFillMode = "Mesh"
        return mv

    def to_orcfxapi(self, model):
        """build an OrcFxAPI.ViewParameters from this ModelView instance"""

        def parse_graphics_mode(ofx_params):
            mode = getattr(self, "GraphicsMode", "WireFrame")
            ofx_params.GraphicsMode = getattr(OrcFxAPI, f"gm{mode}")

        def parse_shaded_mode(ofx_params):
            mode = getattr(self, "ShadedFillMode", "Solid")
            ofx_params.ShadedFillMode = getattr(OrcFxAPI, f"fm{mode}")

        def parse_file_format(ofx_params):
            format_ = getattr(self, "FileFormat", "PNG")
            ofx_params.FileFormat = getattr(OrcFxAPI, f"bff{format_}")

        def parse_bg_colour(ofx_params):
            # via Heff and https://stackoverflow.com/a/7224257
            def RGB(r, g, b):
                r = r & 0xFF
                g = g & 0xFF
                b = b & 0xFF
                return (b << 16) | (g << 8) | r

            r, g, b, = getattr(self, "BackgroundColour", (0, 0, 0))
            ofx_params.BackgroundColour = RGB(r, g, b)

        PARSERS = {
            "GraphicsMode": parse_graphics_mode,
            "FileFormat": parse_file_format,
            "ShadedFillMode": parse_shaded_mode,
            "BackgroundColour": parse_bg_colour,
        }

        vp = model.defaultViewParameters
        for fld, type_ in filter(
            lambda f: getattr(self, f[0]) is not None, vp._fields_
        ):
            if fld in PARSERS:
                PARSERS[fld](vp)
            elif isinstance(type_, ct.Array.__class__):
                getattr(vp, fld)[:] = getattr(self, fld)
            elif type_ == ct.c_void_p:
                if getattr(self, fld) == "Global":
                    setattr(vp, fld, 0)
                else:
                    setattr(vp, fld, model[getattr(self, fld)].handle)
            elif fld != "Size":
                setattr(vp, fld, getattr(self, fld))
        return vp


@dataclass
class VideoSpecification:
    """
    Video parameters for extracting a video from an orcaflex model

    :param start_time [float]: The start time in the model to start recording
    :param end_time [float]: The end time in the model to stop the recording
    :param width [float]: The width of the video in pixels
    :param height [float]: The height of the video in pixels
    :param codec [str]: The codec of the video. Accepted values: "MRLE", "XVID"
    :param model_views [List]: list of ref:ModelView
    """

    start_time: float
    end_time: float
    width: float = DEFAULT_WIDTH
    height: float = DEFAULT_HEIGHT
    codec: str = None
    model_views: List[ModelView] = None


@dataclass
class JobProgress:
    """progress of the job

    :param progress [str]: a summary of the current progress
    :param start_time [float]: time the job started
    :param end_time [float]: time the job ended
    :param current_time [float]: current time in the job
    :param time_to_go [float]: how long estimated to completion in seconds
    :param percent [float]: progress as a percentage
    :param pretty_time [str]: a nice string of time to go e.g. "3 hours, 4 mins"
    """

    progress: str
    start_time: float = None
    end_time: float = None
    current_time: float = None
    time_to_go: float = None
    percent: float = None
    pretty_time: str = None


@dataclass
class OrcaFlexJob:
    """contains references to the items that make up a job


    :param kill_signal [Item]: item with details about any kill_signal being sent to the
        job
    :param job_options [OrcaFlexJobOptions]: job options
    :param data_file [Item]: information about the source of the binary data
        for simulation
    :param data_file_path [Item]: path of data file (if not using a data file item)
    :param results [Item]: details of results required for the simulation
    :param additional_files [Item]: NOT IMPLEMENTED
    :param model_views [List[ModelView]]: images to be saved of the completed simulation
    :param saved_views [List]: saved image files
    :param model_videos [List]: NOT S
    :param saved_videos [List]: NOT IMPLEMENTED
    :param progress [Item]: job progress information
    :param warnings [Item]: warnings from qalx or OrcaFlex
    :param load_case_info [Item]: load case information
    """

    kill_signal: Item = None  # TODO: Implement and document kill signals
    job_options: OrcaFlexJobOptions = OrcaFlexJobOptions()
    data_file: Item = None
    data_file_path: Item = None
    sim_file: Item = None
    sim_file_path: Item = None
    results: Item = None
    additional_files: Item = None  # TODO: Implement and document additional files
    model_views: List[ModelView] = None
    saved_views: List[Item] = None
    model_videos: List[VideoSpecification] = None
    saved_videos: List[Item] = None
    progress: Item = None
    warnings: Item = None
    load_case_info: Item = None

    def as_set_dict(self):
        return {k: v for k, v in self.__dict__.items() if isinstance(v, Item)}
