import pytube
from pytube import YouTube
import urllib.request
import re


class _youtube:
    def __init__(self):
        pass
    @staticmethod
    def get_results(vid):
        vid = vid.replace(" ", '+')
        vid = vid.strip()
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query={}".format(vid))
        video_ext = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        latest = video_ext[0]
        first = video_ext[-1]
        return [video_ext, latest, first]
        


class vids:
    def __init__(self, videos, first, latest):
        self.videos = videos
        self.first = first
        self.latest = latest
    def get_videos_all(self):
        return self.videos
    def get_video_first(self):
        return Downloader("https://www.youtube.com/watch?v="+self.first)
    def get_video_latest(self):
        return Downloader("https://www.youtube.com/watch?v="+self.latest)
class YouTube_Search:

    def __init__(self, video_title):
        self.video = video_title
        self.videos, self.latest, self.first = _youtube.get_results(video_title)
    @property
    def links(self):
        return vids(self.videos, self.first, self.latest)



class Downloader(YouTube):
    def __init__(self, link):
        super().__init__(link)
        self.link_ff = link
    def download_first(self, location=""):
        if location == "":
            self.streams.get_highest_resolution().download()
        else:
            self.streams.get_highest_resolution().download(location)
    def download_last(self, location=''):
        if location == "":
            self.streams.get_lowest_resolution().download()
        else:
            self.streams.get_lowest_resolution().download(location)
