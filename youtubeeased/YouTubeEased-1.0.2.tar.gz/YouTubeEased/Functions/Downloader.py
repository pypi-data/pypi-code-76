import youtube_dl


__all__ = ['DownloadURL']


class DownloadURL:
    url = None

    def __init__(self, url):
        self.url = url

    def on_create_dw(self):
        self.fname = None

    def download_video(self, path_download=None, audio=True):
        """download video using this function"""
        if not path_download:
            path_download = ''
        ytdlopts = {
            'outtmpl': f'{path_download}/%(extractor)s-%(id)s-%(title)s.%(ext)s'
            if self.fname is None else f"{path_download}/{self.fname}"
        }
        if not audio:
            ytdlopts.update({'format': 'bestvideo'})
        with youtube_dl.YoutubeDL(ytdlopts) as ydl:
            meta = ydl.extract_info(url=self.url, download=True)

    def download_audio(self, path_download=None):
        """download audio using this function"""
        if not path_download:
            path_download = ''
        ytdlopts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path_download}/%(extractor)s-%(id)s-%(title)s.%(ext)s'
            if self.fname is None else f"{path_download}/{self.fname}",
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ytdlopts) as ydl:
            ydl.extract_info(url=self.url, download=True)

    def file_name(self, rename):
        self.fname = str(rename)


