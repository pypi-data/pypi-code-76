from YouTubeEased.Functions.Downloader import DownloadURL
from YouTubeEased.Functions.GetInfo import GetInfoVideo
from YouTubeEased.Functions.URLChecker import YoutubeURLChecker, URLNotSupported


class YouTubeEased(DownloadURL, GetInfoVideo, YoutubeURLChecker):
    def __init__(self, url):
        super(YouTubeEased, self).__init__(url)
        if self.is_good_url():
            # Creates the other self parameter that do not start
            self.on_create()
            self.on_create_dw()
        else:
            raise URLNotSupported("URL not supported")