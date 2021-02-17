"""
Sim Bot Functions
~~~~~~~~~~~~~~~~~

This module contains the step functions that are called by SimBot.

`preprocess_orcaflex` simply parses the job options sets up state and warnings items

Almost all the work is done in `process_orcaflex`, the basic steps are:

1. Load the model data - this will only return once it has been able to get a licence or
    has tried multiple times to get one as defined in model.OrcaFlexJobOptions
2. Define progress handlers if required
3. Calculate the estimated size of the simulation and based on available RAM disable
    in-memory logging if required.
4. Attempt statics, use the `static_search`_ method if defined in model tags. If statics
    fails the step function returns
5. Attempt dynamics. If dynamics fails the step function returns.
6. Save the simulation file to qalx if required.
7. Extract results if required
8. Extract load case information if required
9. Extract model views if required
10. If simulation stoped due to instability then report this in the warnings and update the state
11. Put the OrcFxAPI.Model instance into the the step result data so a custom post-processing function can play with it


"""
import platform
import queue
import threading
import time
import traceback
from io import BytesIO
from random import randint
from time import sleep
from typing import Mapping, Sequence, Union, Tuple

from qalx_orcaflex.core import QalxSmartStaticsError

try:  # we build the docs on linux and this won't work...
    import OrcFxAPI
except (ImportError, ValueError):
    pass
import psutil
from OrcFxAPI import DLLError
from dataclasses import asdict
from pyqalx.bot import QalxJob
from pyqalx.core.errors import QalxError

from qalx_orcaflex.data_models import (
    OrcaFlexJob,
    OrcaFlexJobOptions,
    OrcaFlexJobState,
    TimeHistory,
    RangeGraph,
    ModelInfo,
    ModelView,
    JobState,
)
from qalx_orcaflex.helpers import (
    nice_time,
    model_simulation_size,
    load_model_data,
    result_name,
    result_details,
    get_tags,
)
from qalx_orcaflex.helpers.smart_statics import solved_model
from qalx_orcaflex.video.extract import video_extractor


def initialise_orcaflex_bot(qalx):
    try:
        import OrcFxAPI

        OrcFxAPI.Model()
    except ImportError:
        raise QalxError("Could not import OrcFxAPI, is it installed?")
    return True


def on_wait_orcaflex(job):
    pass


def begin_orcaflex(job):
    pass


def preprocess_orcaflex(job: QalxJob):
    job.entity["meta"]["state"] = OrcaFlexJobState(
        state=JobState.PRE_PROCESSING.value
    ).__dict__
    job.entity["meta"]["bot_host"] = {
        "node": platform.node(),
        "platform": platform.platform(),
    }
    job.save_entity()
    options = job.entity.get_item_data("job_options")
    if options:
        job.options = OrcaFlexJobOptions(**options)
    else:
        job.options = OrcaFlexJobOptions()
    job.warnings = job.add_item_data(
        "warnings", data={"warning_text": []}, meta={"_class": "orcaflex.warnings"}
    )


def update_job_progress(ofx, update_queue, job):
    """update the progress and save the item"""
    time_of_last_update = time.time()
    if ofx.progress:
        should_exit = False
        while not should_exit:
            progress = update_queue.get()
            update_queue.task_done()
            if progress is None:
                should_exit = True
            else:
                time_since_last_update = time.time() - time_of_last_update
                if time_since_last_update > job.options.update_interval:
                    ofx.progress["data"] = progress
                    job.session.item.save(ofx.progress)
                    time_of_last_update = time.time()


# DEV_NOTE: this function was written a long time ago using a functional approach, as it has grown it probably should
# have been converted to a more object-oriented approach. One day maybe we will get there.
def process_orcaflex(job: QalxJob) -> None:
    def update_job_state(state_dict: Mapping) -> None:
        """update the state and save the set"""
        job.entity["meta"]["state"] = OrcaFlexJobState(**state_dict).__dict__
        job.save_entity()

    update_job_state({"state": JobState.PROCESSING.value})
    ofx = OrcaFlexJob(
        **job.entity["items"]
    )  # unpack the raw Set into our pre-defined model
    update_queue = queue.Queue()

    threading.Thread(target=update_job_progress, args=(ofx, update_queue, job)).start()

    def update_job_warnings(warnings: Sequence[str]) -> None:
        """add all the warning texts, save the item"""
        for warn in warnings:
            job.warnings["data"]["warning_text"].append(warn)
        job.session.item.save(job.warnings)

    # if you have a network dongle and lots of jobs starting at once it can cause the licence server to freak out
    # one way around this is to define random waits for each job so they stagger the start slightly.
    # Best solution: use software licencing from Orcina
    if job.options.time_to_wait:
        sleep(job.options.time_to_wait)

    def report_dynamics(
        model: OrcFxAPI.Model, current_time: float, start: float, stop: float
    ) -> Union[None, bool]:
        """progress handler for dynamics"""

        def dynamic_percent() -> float:
            """calculate the percentage completion based on start,
            stop and current time"""
            secs_in = abs((start - current_time))
            total_secs = stop - start
            if total_secs:
                return secs_in / total_secs
            else:
                return 0.0

        pc = dynamic_percent()
        pretty_time = nice_time(
            model.simulationTimeToGo
        )  # make a nice time from seconds
        if pretty_time is None:
            pretty_time = f"{pc:2.1%}"
        dp = dict(
            progress=f"dynamics: {pretty_time}",
            start_time=start,
            end_time=stop,
            current_time=current_time,
            time_to_go=model.simulationTimeToGo,
            percent=pc,
            pretty_time=pretty_time,
        )
        update_queue.put(dp)
        if (
            job.options.killable
        ):  # allows killing jobs/bots although this is not tested or
            # documented and might not work
            kill_signal = ofx.kill_signal
            if kill_signal["data"].get("KILL BOT"):
                job.publish_status("Bot kill signal sent", kill_signal["data"])
                update_job_state({"state": JobState.USER_CANCELLED.value})
                job.terminate()
                return False
            if kill_signal["data"].get("KILL JOB"):
                job.publish_status("Job kill signal sent", kill_signal["data"])
                update_job_state({"state": JobState.USER_CANCELLED.value})
                return False

    def report_statics(model: OrcFxAPI.Model, progress: str) -> None:
        """handler for statics progess"""
        sp = dict(
            progress=f"statics: {progress}",
            time_to_go=model.simulationTimeToGo,
            pretty_time=nice_time(model.simulationTimeToGo),
        )
        update_queue.put(sp)

    def report_percent(model: OrcFxAPI.Model, percent: float):
        pp = dict(
            percent=percent / 100,
            time_to_go=model.simulationTimeToGo,
            pretty_time=nice_time(model.simulationTimeToGo),
        )
        update_queue.put(pp)

    def report_error(error: str):
        update_job_state({"state": JobState.ERROR.value, "error": error})

    def try_statics(model: OrcFxAPI.Model) -> bool:
        update_job_state({"state": JobState.RUNNING_STATICS.value})
        statics = {}  # we save info about how well statics went

        def save_statics_data():
            job.add_item_data("statics", statics, meta={"_class": "orcaflex.statics"})

        try:
            start = time.time()  # we time how long statics takes
            try:
                solved_model(
                    model, job.options.max_search_attempts
                )  # solves with search if required
            except QalxSmartStaticsError:
                fn = f"{job.entity['meta']['case_name']}_FAILED_SS.dat"
                ff = job.session.item.add(
                    source=BytesIO(model.SaveDataMem()),
                    file_name=fn,
                    meta={"_class": "orcaflex.failed_statics"},
                )
                job.entity["items"]["failed_statics"] = ff
                update_job_state({"state": JobState.STATICS_FAILED.value})
                return False
            end = time.time()
            statics["time_to_solve"] = end - start
            statics["solves"] = True
            save_statics_data()
            update_job_warnings(model.warnings)  # add the warnings if there were any
            return True  # this worked
        except DLLError as err:  # there was an error in OrcFxAPI
            report_error(str(err))
            statics["solves"] = False
            save_statics_data()
            return False
        except Exception as err:  # there was a qalx_orcaflex error
            tb = traceback.format_exc()
            report_error(str(err) + tb)
            statics["solves"] = False
            save_statics_data()
            return False

    def try_dynamics(model: OrcFxAPI.Model) -> bool:
        update_job_state({"state": JobState.RUNNING_DYNAMICS.value})
        success = False  # we might need to have a few goes at getting a licence
        while not success:
            try:
                model.RunSimulation()
                update_job_warnings(model.warnings)
                return True  # worked
            except OrcFxAPI.DLLError as err:
                if (
                    err.status == OrcFxAPI.stLicensingError
                ):  # if we got a licence error then wait and try again
                    time.sleep(
                        randint(20, 600)
                    )  # TODO: make this smarter, ten minis to wait could be overkill
                    job.log.debug("waiting for licence... " + str(err))
                else:  # some other kind of error best report it
                    tb = traceback.format_exc()
                    report_error(str(err) + "\n\n" + tb)
                    return False  # didn't work

    def try_save_sim(model: OrcFxAPI.Model) -> Tuple[bool, Union[None, str]]:
        """try to save the simulation data to qalx"""
        update_job_state({"state": JobState.SAVING_SIMULATION.value})
        try:
            model_bytes = model.SaveSimulationMem()
            sim_name = f"{job.entity['meta']['case_name']}.sim"
            job.entity["items"]["simulation_file"] = job.session.item.add(
                source=BytesIO(model_bytes),
                file_name=sim_name,
                meta={"_class": "orcaflex.simulation_file"},
            )
            job.save_entity()
            update_job_state({"state": JobState.SIMULATION_SAVED.value})
            return True, None  # worked with no errors
        except Exception as err:
            msg = """Failed to save a simulation:\n\n""" + str(err)
            report_error(msg)
            return False, msg  # there was a problem

    def extract_results(model: OrcFxAPI.Model):
        """take the pre-specified results required and populates the extracted results information
        """
        # DEV NOTE: This does not use any of the recent OrcFxAPI ability to extract
        # multiple results which would offer
        # quite a bit of performace improvement in a lot of cases
        # TODO: use multiple result specification - requires grouping  the results
        #  first by object, period and
        #  object extra
        update_job_state({"state": JobState.EXTRACTING_RESULTS.value})
        job.log.debug(ofx.results)
        for res_n, (_, result_guid) in enumerate(
            ofx.results["data"].items()
        ):  # for all the results specified
            try:
                result = job.session.item.get(guid=result_guid)  # get the result item
                if result["data"]["_type"] == "th":  # if it's a time history
                    rr = TimeHistory.from_dict(result["data"])  # unpack into our model
                    ofx_obj = model[rr.object]  # get the OrcaFlexObject
                    obj_ex = rr.object_extra.to_orcfxapi(
                        ofx_obj.type
                    )  # get the ObjectExtra
                    period = rr.period.to_orcfxapi()  # get the Period
                    th = ofx_obj.TimeHistory(
                        rr.variable, period=period, objectExtra=obj_ex
                    )  # extract TimeHistory
                    rr.extracted.time = list(
                        model.general.TimeHistory("Time", period=period)
                    )  # get time for x-axis
                    rr.extracted.y_values = list(th)  # y axis
                    rr.extracted.static_value = ofx_obj.StaticResult(
                        rr.variable, objectExtra=obj_ex
                    )  # static value
                    if (
                        rr.meta.name is None
                    ):  # if we don't have a name for this result then make one
                        rr.meta.name = result_name(
                            res_n,
                            ofx_obj,
                            OrcFxAPI.rtTimeHistory,
                            result_name=rr.variable,
                            oe=obj_ex,
                        )
                    else:  # or ensure it is unique
                        rr.meta.name = f"r#{res_n}: {rr.meta.name}"
                    rr.meta.var_details = result_details(
                        ofx_obj,
                        OrcFxAPI.rtTimeHistory,
                        result_name=rr.variable,
                        oe=obj_ex,
                    )  # get all the gory details of the result
                else:  # it's a range graph
                    rr = RangeGraph.from_dict(result["data"])  # unpack into our model
                    ofx_obj = model[rr.object]  # get the OrcaFlexLineObject
                    arc_length_range = (
                        rr.arc_length_range.to_orcfxapi()
                    )  # get the ArcLengthRange
                    obj_ex = rr.object_extra.to_orcfxapi(ofx_obj.type)  # get the Period
                    period = rr.period.to_orcfxapi()  # get the ObjectExtra
                    rg = ofx_obj.RangeGraph(
                        rr.variable,
                        period,
                        obj_ex,
                        arc_length_range,
                        rr.storm_duration_hours,
                    )  # extract RangeGraph
                    rr.extracted.arc = list(rg.X)  # x-axis
                    rr.extracted.y_static = list(
                        ofx_obj.RangeGraph(
                            rr.variable,
                            OrcFxAPI.Period(OrcFxAPI.pnStaticState),
                            obj_ex,
                            arc_length_range,
                        ).Mean
                    )  # get the static values
                    rr.extracted.y_max = list(rg.Max)
                    rr.extracted.y_mean = list(rg.Mean)
                    rr.extracted.y_min = list(rg.Min)
                    if (
                        rr.meta.name is None
                    ):  # if we don't have a name for this result then make one
                        rr.meta.name = result_name(
                            res_n,
                            ofx_obj,
                            OrcFxAPI.rtRangeGraph,
                            result_name=rr.variable,
                            oe=obj_ex,
                        )
                    else:  # or ensure it is unique
                        rr.meta.name = f"r#{res_n}: {rr.meta.name}"
                    rr.meta.var_details = result_details(
                        ofx_obj,
                        OrcFxAPI.rtRangeGraph,
                        result_name=rr.variable,
                        oe=obj_ex,
                    )
                result["data"] = rr.to_valid_dict()  # put our data into the result Item
                job.session.item.save(result)  # save the item back to qalx
            except Exception as err:  # something went wrong
                msg = f"Failed to extract result with guid {result_guid}:\n\n{err}"
                job.log.error(msg + "\n\n" + traceback.format_exc())
                update_job_warnings([msg])
        update_job_state({"state": JobState.RESULTS_EXTRACTED.value})

    def extract_load_case_info(model: OrcFxAPI.Model) -> None:
        """extracts load case information"""
        for mi in ofx.load_case_info["data"]["model_info"]:
            mi["value"] = model[mi["object_name"]].GetData(
                mi["data_name"], mi["item_index"]
            )  # get the value for the given tag data

        # get all tags on general that start with "lci__"
        def _lci(key):
            print(key)
            return key.startswith("lci__")

        for k, v in get_tags(model, tag_filter=_lci)["General"].items():
            ofx.load_case_info["data"]["model_info"].append(
                asdict(ModelInfo("general", "tag", alias=k.split("__")[-1], value=v))
            )
        job.session.item.save(ofx.load_case_info)

    def extract_model_views(model: OrcFxAPI.Model) -> None:

        saved_views = {}

        def extract_view(mv_raw: Mapping):
            mv = ModelView(**mv_raw)  # unpack into our model
            vp = mv.to_orcfxapi(model)  # make ViewParameters
            save_bytes = model.SaveModelViewMem(
                viewParameters=vp
            )  # bytes of saved view
            mvi = job.session.item.add(
                source=BytesIO(save_bytes),
                file_name=mv.view_filename,
                meta={"_class": "orcaflex.saved_view"},
            )  # save to qalx
            saved_views[
                mv.ViewName
            ] = mvi.guid  # make a mapping of saved view name to guid of the save data

        if ofx.model_views:  # we have some pre-defined views in the OrcaFlexJob
            update_job_state({"state": JobState.EXTRACTING_MODEL_VIEWS.value})
            for mv_name, mv_raw in ofx.model_views["data"].items():
                try:
                    extract_view(mv_raw)
                except Exception as err:
                    update_job_warnings([f"{mv_name} failed. Reason\n {str(err)}"])

        mv_tags = get_tags(model, lambda t: t.startswith("mv__"), True)
        if mv_tags:
            flag_state = False
            for _, tags in mv_tags.items():
                # get all the views defined in the model file
                for tag, data in tags.items():
                    if flag_state is False:
                        update_job_state(
                            {"state": JobState.EXTRACTING_MODEL_VIEWS.value}
                        )
                        flag_state = True
                    data["ViewName"] = tag.split("__")[-1]
                    try:
                        extract_view(data)
                    except Exception as err:
                        update_job_warnings([f"{tag} failed. Reason\n {str(err)}"])

        if (
            saved_views
        ):  # if we saved some views then we add the item to the Job and save it
            svi = job.session.item.add(
                data=saved_views, meta={"_class": "orcaflex.saved_views"}
            )
            job.entity["items"]["saved_views"] = svi
            update_job_state({"state": JobState.MODEL_VIEWS_EXTRACTED.value})

    # THE FUNCTION BEGINS HERE AND CALLS ABOVE FUNCTIONS AS IT GOES (Not great.)
    update_job_state({"state": JobState.LOADING_MODEL_DATA.value})
    model = load_model_data(ofx, job.options)  # load the model

    if job.options.record_progress:  # set the handlers
        model.dynamicsProgressHandler = report_dynamics
        model.staticsProgressHandler = report_statics

    # TODO: #2750-include-model-deltas-in-job

    ram_per_core = (
        (psutil.virtual_memory().available / 1024) * 0.90 / psutil.cpu_count()
    )  # in MB

    if model_simulation_size(model) > ram_per_core:  # set the right logging
        model.DisableInMemoryLogging()

    if not try_statics(model):  # try statics and if it fails exit
        job.entity["meta"]["processing_complete"] = True
        return
    if not try_dynamics(model):  # try dynamics and if it fails exit
        job.entity["meta"]["processing_complete"] = True
        return

    if job.options.save_simulation:  # try to save the sim
        worked, warning = try_save_sim(model)
        if not worked:
            update_job_warnings([warning])

    if ofx.results:
        extract_results(model)

    if ofx.load_case_info:
        extract_load_case_info(model)

    if ofx.model_views or get_tags(model, lambda t: t.startswith("mv__"), True):
        extract_model_views(model)

    if ofx.model_videos:
        update_job_state({"state": JobState.EXTRACTING_MODEL_VIDEOS.value})
        video_extractor.extract_model_videos(job=job, ofx=ofx, model=model)
        update_job_state({"state": JobState.MODEL_VIDEOS_EXTRACTED.value})

    if (
        str(model.state) == "SimulationStoppedUnstable"
    ):  # if the simulation was unstable then let us know
        msg = "Simulation was unstable at {:2.3f}s".format(
            model.simulationTimeStatus.CurrentTime
        )
        update_job_warnings([msg])
        update_job_state({"state": JobState.SIMULATION_UNSTABLE.value})

    # this allows `postprocessing_function` to access model data
    job.context["model"] = model
    job.entity["meta"]["processing_complete"] = True  # we done.
    # Signal the end of update worker thread and release the memory
    update_queue.put(None)
    update_queue.join()


def post_process_orcaflex(job: QalxJob):
    send_to = job.entity["meta"].get("send_to", [])
    if send_to:
        for queue_name in send_to:
            queue = job.session.queue.get_or_create(queue_name)
            job.entity.__class__.add_to_queue(payload=job.entity, queue=queue)
            job.log.debug(f"{job.entity.guid} sent to {queue_name}")
    # Clear up the model and delete references to the model and context dict
    # from the job. This is to try and keep the memory usage of the worker as
    # low as possible for the next job
    job.context["model"].Clear()
    del job.context["model"].progressHandlerCallback
    del job.context["model"]
    del job.context
