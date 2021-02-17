import os
from dataclasses import asdict

from ..helpers import ModelWithLicence


def check_sim_file_type(file_path):
    """
    Helper that checks if a provided file is a sim file. This is needed in the
    case of the video bot that only accepts sim files for video extraction
    """
    _, ext = os.path.splitext(file_path)
    if ext != ".sim":
        raise ValueError(f'A sim file(".sim") must be provided and not "{file_path}"')


def load_model_sim(orcaflex_job, job_options):
    """
    Take the job and options and return a model using helpers.ModelWithLicence
    from the provided sim file
    """
    with ModelWithLicence(
        job_options.licence_attempts, 10, job_options.max_wait
    ) as model:
        if orcaflex_job.sim_file:
            model.LoadSimulationMem(orcaflex_job.sim_file.read_file())
            return model
        elif orcaflex_job.sim_file_path:
            model.LoadSimulation(orcaflex_job.sim_file_path["data"]["full_path"])
            return model
        raise AttributeError("The job must have a sim_file or sim_file_path")


def unpack_model_videos(job_dict):
    """
    For the provided job dictionary, unpack the video specifics and return in
    the expected dictionary form
    """
    model_videos = dict()
    for i, video_spec in enumerate(job_dict["model_videos"], start=1):
        video_views = dict()
        if video_spec.model_views is not None:
            for _, mv in enumerate(video_spec.model_views):
                video_views[mv.ViewName] = asdict(mv)
        else:
            video_views["Default View"] = None
        model_videos[f"vid_{i}"] = {
            "start_time": video_spec.start_time,
            "end_time": video_spec.end_time,
            "width": video_spec.width,
            "height": video_spec.height,
            "codec": video_spec.codec,
            "model_views": video_views,
        }
    return model_videos
