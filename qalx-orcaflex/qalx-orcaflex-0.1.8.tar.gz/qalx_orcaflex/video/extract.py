"""
Defines callable to be used in a bot context for video extraction
"""

import os
import shutil
from tempfile import mkdtemp

from qalx_orcaflex.data_models import ModelView, OrcaFlexJob
from qalx_orcaflex.helpers import load_model_data
from qalx_orcaflex.video.core import Video
from qalx_orcaflex.video.helpers import load_model_sim


class ExtractModelVideos:
    """
    Video extraction callable. This is a flexible implementation, so that an
    instance of the class can be used with the `extract_model_videos` method
    as a sub-step within a bot step function, or can also be used directly
    assigned as a processing step function in a bot

    Instance attributes:
        job: The job received as defined in qalx bots
        ofx: An OrcaFlexJob instance representation of job
        model: The orcaflex model to extract a video for
        saved_videos: A dict containing the video file items created
    """

    def __init__(self):
        self.job = None
        self.ofx = None
        self.model = None
        self.saved_videos = dict()

    def _update_attrs(self, job, ofx, model):
        """
        Update the values of the instance attributes when a new job is submitted
        """
        self.job = job
        self.ofx = ofx
        self.model = model
        self.saved_videos = dict()

    def update_job_warnings(self, warnings):
        """Add all the warning texts, save the item"""
        for warn in warnings:
            self.job.warnings["data"]["warning_text"].append(warn)
        self.job.session.item.save(self.job.warnings)

    def extract_video(
        self,
        video_path,
        start_time,
        end_time,
        width,
        height,
        codec,
        mv_raw=None,
        **kwargs,
    ):
        """
        Raw video extraction functionality. Essentially a wrapper around
        `Video.avi_from_ofx`. When a video has been extracted locally with the
        `avi_from_ofx` method, it is then added as an item on qalx the guid of
        which is stored in the `saved_videos` container
        """
        if mv_raw is not None:
            mv = ModelView(**mv_raw)  # unpack into our model
            vp = mv.to_orcfxapi(self.model)
        else:
            vp = None
        Video.avi_from_ofx(
            model=self.model,
            file_path=video_path,
            start_time=start_time,
            end_time=end_time,
            width=width,
            height=height,
            codec=codec,
            view_parameters=vp,
        )
        video = self.job.session.item.add(
            source=video_path,
            file_name=os.path.basename(video_path),
            meta={"_class": "orcaflex.saved_video"},
        )
        self.saved_videos[
            os.path.basename(os.path.splitext(video_path)[0])
        ] = video.guid

    def extract_model_videos(self, job, ofx, model):
        """
        Extract all the model videos defined on the job argument. Creates a
        local temporary directory where all the videos are extracted, which is
        then removed once all videos have been extracted
        """
        self._update_attrs(job, ofx, model)
        temp_dir = mkdtemp()
        if self.ofx.model_videos:
            for vid_ext, vid_spec in self.ofx.model_videos["data"].items():
                for mv_file_name, model_view in vid_spec["model_views"].items():
                    file_path = os.path.join(
                        temp_dir, f"{os.path.splitext(mv_file_name)[0]}_{vid_ext}.avi"
                    )
                    try:
                        self.extract_video(
                            video_path=file_path, mv_raw=model_view, **vid_spec
                        )
                    except Exception as err:
                        self.update_job_warnings(
                            [f"{file_path} failed. Reason\n {str(err)}"]
                        )

        if self.saved_videos:
            saved_videos = self.job.session.item.add(
                data=self.saved_videos, meta={"_class": "orcaflex.saved_videos"}
            )
            self.job.entity["items"]["saved_videos"] = saved_videos
            self.job.save_entity()

        shutil.rmtree(temp_dir, ignore_errors=True)

    def __call__(self, job, *args, **kwargs):
        """
        Allows us to use an instance of the class directly as a bot step
        function that accepts a job argument.
        """
        ofx = OrcaFlexJob(**job.entity["items"])
        if ofx.data_file_path or ofx.data_file:
            model = load_model_data(ofx, job.options)
        else:
            model = load_model_sim(ofx, job.options)
        self.extract_model_videos(job, ofx, model)


video_extractor = ExtractModelVideos()
