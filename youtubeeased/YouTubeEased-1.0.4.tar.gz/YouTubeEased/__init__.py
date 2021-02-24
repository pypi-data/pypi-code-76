from YouTubeEased.utils import VideoHandle, URLNotSupported, Checker
from youtube_dl import DownloadError


class YouTubeEased(VideoHandle, Checker):
    def __init__(self, url):
        self.url = url
        try:
            super(YouTubeEased, self).__init__(self.url)
        except DownloadError:
            raise URLNotSupported("URL not supported")

    def __enter__(self):
        try:
            super(YouTubeEased, self).__init__(self.url)
            return self
        except DownloadError:
            raise URLNotSupported("URL not supported")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
