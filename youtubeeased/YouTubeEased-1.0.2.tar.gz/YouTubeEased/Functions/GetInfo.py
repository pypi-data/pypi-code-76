from youtube_dl import YoutubeDL

__all__ = ['GetInfoVideo']


class GetInfoVideo:
    def __init__(self, url):
        self.url = url

    def on_create(self):
        self._ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcetitle': True,
            'forceurl': True,
        }

        with YoutubeDL(self._ydl_opts) as ydl:
            self.data = ydl.extract_info(self.url, False)
            if 'entries' in self.data:
                self.data = self.data['entries']

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

    def get_info_by_elem(self, *elem):
        """Get the data by setting elem steps"""
        to_return = self.data
        try:
            for key in elem:
                to_return = to_return[key]
            return to_return
        except KeyError:
            raise KeyError("Key element was not found")
