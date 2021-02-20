from logging import getLogger
from mimetypes import guess_type
from mutagen import id3
from mutagen.mp3 import MP3
from tempfile import mkstemp
from .exceptions import ExternalLibraryError
from .models import Sound
import os
import subprocess


def lame(source, dest):
    """
    Looks for and then runs the LAME MP3 encoder, given a source and
    destination filename.

    Args:
        source (str): Name of the file to convert from.
        dest (str): Name of the file to convert to.

    Raises:
        ExternalLibraryError: If the LAME library can't be located.
    """

    logger = getLogger('opawg.audiolipsum')
    result = subprocess.run(
        'which lame',
        shell=True,
        capture_output=True,
        text=True
    )

    lame_filename = result.stdout and result.stdout.strip()
    if not lame_filename:
        raise ExternalLibraryError(
            'LAME MP3 library not installed or could not be found.'
        )

    logger.debug('LAME library found at %s' % lame_filename)
    logger.debug('Converting %s to %s' % (source, dest))

    subprocess.call(
        '$(which lame) %s %s' % (source, dest),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    logger.debug('Converted %s to %s' % (source, dest))


def generate_wav(low_freq, high_freq, duration=60):
    """
    Generates a WAV file with a number of random tones of a given
    `tone_duration`, within a frequency range of `low_freq` and `high_freq`.

    Args:
        low_freq (int): The lowest frequency to generate a tone at.
        high_freq (int): The highest frequency to generate a tone at.
        duration (int): The desired duration of the audio file in seconds.

    Returns:
        str: The name of the generated WAV file.
    """

    sound = Sound(
        *range(low_freq, high_freq + 1),
        total_duration=duration,
        randomize_frequencies=True
    )

    handle, filename = mkstemp('.wav')
    os.close(handle)

    sound.save(filename)
    return filename


def convert_mp3(source, dest):
    """
    Converts a given source audio file into an MP3, placed at the
    specified destination.

    Args:
        source (str): Name of the file to convert from.
        dest (str): Name of the file to convert to.
    """

    lame(source, dest)


def tag_mp3(filename, title, artwork=None):
    """
    Adds ID3 tags to a file.

    Args:
        filename (str): The name of the MP3 file that needs tagging.
        title (str): The text to be used as the ID3 title.
        artwork (str): The naem of the image file to be attached as artwork.
            Defaults to None.
    """

    audio = MP3(filename)
    duration = audio.info.length
    tags = id3.ID3()

    tags['TLEN'] = id3.TLEN(
        encoding=3,
        text=str(int(duration * 1000))
    )

    if title:
        tags['TIT2'] = id3.TIT2(
            encoding=3,
            text=[title]
        )

    if artwork:
        mimetype, encoding = guess_type(artwork)
        if mimetype:
            with open(artwork, 'rb') as f:
                tags['APIC'] = id3.APIC(
                    encoding=0,
                    mime=mimetype,
                    type=9,
                    data=f.read()
                )

    tags.update_to_v23()
    tags.save(
        filename,
        v1=1,
        v2_version=3,
        padding=lambda info: 0
    )
