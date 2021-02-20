from hashlib import md5
from lorem.text import TextLorem
from multiprocessing import Pool
from tempfile import mkstemp
from .helpers import generate_wav, convert_mp3, tag_mp3
import os
import qrcode


__version__ = '0.1'


class MP3Batch(object):
    def __init__(self, low_freq, high_freq, duration):
        """
        Creates a new batch of MP3 generation jobs.

        Args:
            low_freq (int): The lowest frequency to generate a tone at.
                Defaults to 16.
            high_freq (int): The highest frequency to generate a tone at.
                Defaults to 7902.
            duration (int): The desired duration of the audio file in seconds.
                Defaults to 60.
        """

        self.low_freq = low_freq
        self.high_freq = high_freq
        self.duration = duration

    def generate(self, number):
        """
        Generates an MP3 file with tones from a range of low and high
        frequencies.

        Args:
            number (int): A number used in the multiprocessing iterator.

        Returns:
            str: The name of the generated MP3 file.
        """

        lorem = TextLorem()
        title = lorem.sentence()
        handle, qr_filename = mkstemp('.png')
        os.close(handle)

        try:
            qr = qrcode.make(md5(title.encode('utf-8')).hexdigest())
            qr.save(qr_filename)
            wav_filename = generate_wav(
                self.low_freq,
                self.high_freq,
                self.duration
            )

            try:
                handle, mp3_filename = mkstemp('.mp3')
                os.close(handle)

                convert_mp3(wav_filename, mp3_filename)
                tag_mp3(mp3_filename, title, qr_filename)
                return mp3_filename
            finally:
                os.remove(wav_filename)
        finally:
            os.remove(qr_filename)


def generate_mp3s(
    count,
    low_freq=16,
    high_freq=7902,
    duration=60,
    multiprocessing=True
):
    """
    Generates a specific number of MP3 files with tones from a range
    of low and high frequencies.

    Args:
        count (int): The number of files to generate.
        low_freq (int): The lowest frequency to generate a tone at.
            Defaults to 16.
        high_freq (int): The highest frequency to generate a tone at.
            Defaults to 7902.
        duration (int): The desired duration of the audio file in seconds.
            Defaults to 60.
        multiprocessing (bool): Run operations in parallel.
            Defauls to True.

    Returns:
        generator: An iterable list of file objects containing the
            MP3s generated.

    The `multiprocessing` argument was added as an option because coverage.py
    can't cope with paralell operations, despite what the docs say.
    """

    mapper = multiprocessing and Pool().map or map
    batch = MP3Batch(low_freq, high_freq, duration)

    for mp3_filename in mapper(batch.generate, range(count)):
        try:
            yield open(mp3_filename, 'rb')
        finally:
            os.remove(mp3_filename)
