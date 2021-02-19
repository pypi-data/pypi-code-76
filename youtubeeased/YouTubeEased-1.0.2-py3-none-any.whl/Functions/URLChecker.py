import youtube_dl

__all__ = ['URLNotSupported', "YoutubeURLChecker"]


class URLNotSupported(Exception):
    """pops up when url is not been supported by youtube_dl"""


class YoutubeURLChecker:
    def __init__(self, url):
        self.url = url

    def is_good_url(self):
        """Checks if url is been supported"""
        extractors = youtube_dl.extractor.gen_extractors()
        for e in extractors:
            if e.suitable(self.url) and e.IE_NAME != 'generic':
                return True
        return False

    def get_url(self) -> str:
        return self.url

    def set_url(self, new_url) -> None:
        if YoutubeURLChecker(new_url).is_good_url():
            self.url = new_url
        else:
            raise URLNotSupported("URL is not supported")
