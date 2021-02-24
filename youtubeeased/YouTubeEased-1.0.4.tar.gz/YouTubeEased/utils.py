try:
    import youtube_dl
    from youtube_dl import YoutubeDL
except ImportError:
    raise ImportError("youtube_dl must be downloaded!")


__all__ = ['URLNotSupported', "VideoHandle", "Checker"]


class URLNotSupported(Exception):
    """pops up when url is not been supported by youtube_dl"""


class Checker:
    def __init__(self, url):
        self.url = url

    def is_good_url(self) -> bool:
        """Checks if url is been supported"""
        extractors = youtube_dl.extractor.gen_extractors()
        for e in extractors:
            if e.suitable(self.url) and e.IE_NAME != 'generic':
                return True
        return False


class VideoHandle(Checker):
    def __init__(self, url):
        super(VideoHandle, self).__init__(url)
        self.__fname = ''
        self.url = url
        self.__ydl_opts = {
            'format': 'best',
            'quiet': True,
            'skip_download': True,
            'forcetitle': True,
            'forceurl': True,
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s'
        }

        with YoutubeDL(self.__ydl_opts) as ydl:
            self.data = ydl.extract_info(self.url, False)
            if 'entries' in self.data:
                self.data = self.data['entries']

    def get_url(self) -> str:
        return self.url

    def set_url(self, new_url) -> None:
        if self.is_good_url():
            self.url = new_url
        else:
            raise URLNotSupported("URL is not supported")

    def get_full_info(self) -> dict:
        """Get the full data"""
        return self.data

    def get_minimized_info(self) -> dict:
        """Get the data more specifically to the video"""
        to_return = {}
        wanted_info = ['title', 'description', 'upload_date',
                       'uploader', 'uploader_url', 'channel_url', 'duration', 'view_count',
                       'average_rating', 'age_limit', 'webpage_url', 'like_count',
                       'dislike_count', 'filesize', 'fps', 'height', 'width', 'quality', 'url', 'is_live']

        for info in wanted_info:
            try:
                to_return.update({info: self.data[info]})
            except KeyError:
                pass
        return to_return

    def get_info_by_elem(self, *steps) -> dict:
        """Get the data by setting elem steps"""
        to_return = self.data
        try:
            for key in steps:
                to_return = to_return[key]
            return to_return
        except KeyError:
            raise KeyError("Key element was not found")

    def download_video(self, path_download=None, audio=True):
        """download video using this function"""
        ydl_opts = self.__ydl_opts

        if not path_download:
            path_download = ''
        if path_download is not None:
            ydl_opts.update({'outtmpl': path_download})
        if not audio:
            ydl_opts.update({'format': 'bestvideo'})
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.url)

    def download_audio(self, path_download=None):
        """download audio using this function"""
        if not path_download:
            path_download = ''
        ytdlopts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path_download}/%(extractor)s-%(id)s-%(title)s.%(ext)s'
            if self.__fname is None else f"{path_download}/{self.__fname}",
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ytdlopts) as ydl:
            ydl.extract_info(url=self.url, download=True)

    def rename(self, rename):
        self.__fname = str(rename)

    def set_new_ydl_opts(self, opts):
        self.__ydl_opts = opts

    def get_ydl_opts(self):
        return self.__ydl_opts
