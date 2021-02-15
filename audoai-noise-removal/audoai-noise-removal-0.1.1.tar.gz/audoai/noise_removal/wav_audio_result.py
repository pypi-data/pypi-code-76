import shutil

import requests


class WavAudioResult:
    """An audio result from the API in the form of a WAV file"""
    def __init__(self, url: str):
        self.url = url

    def save(self, filename: str):
        """Save the wav file to the provided filename"""
        if not filename.lower().endswith('.wav'):
            raise ValueError('Filename should end with .wav')
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def __repr__(self):
        return 'WavAudioResult(url={!r})'.format(self.url)
