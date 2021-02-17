"""
Example usage

qalx bot-start --processes 1 --queue-name "qalx-ofx-video" qalx_orcaflex.bots:video_bot  # noqa
"""

from pyqalx import Bot

from ..bots.sim import preprocess_orcaflex
from ..video.extract import video_extractor


class VideoBot(Bot):
    """
    Video bot

    This bot takes an orcaflex job in the same way as the SimBot, but only
    requires a sim file and a video parameters specification. It is only used
    to extract video from existing simulation files
    """

    DEFAULT_NAME = "VideoBot"

    def __init__(self, bot_name):
        super(VideoBot, self).__init__(bot_name)

        self.preprocess_function = preprocess_orcaflex
        self.process_function = video_extractor
