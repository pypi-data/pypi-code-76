from logging import getLogger
import math
import random
import struct
import wave


CHANNELS = 1
SAMPLE_WIDTH = 2
SAMPLE_RATE = 44100
FRAME_COUNT = 0
TONE_DURATION = .05
COMPRESSION_TYPE = 'NONE'
COMPRESSION_NAME = 'not compressed'


class Sound(object):
    """
    Represents a sound, made up of a tones at a range of frequencies.
    """

    def __init__(
        self,
        *frequencies,
        total_duration=60,
        randomize_frequencies=False
    ):
        """
        Creates a new Sound object.

        Args:
            *frequencies (int): A number of frequencies to generate tones at.
            total_duration (int): The duration of the sound, in seconds.
                Defaults to 60.
            randomize_frequencies (bool): If true, shuffle the list of
                supplied frequencies.
        """

        self.frequencies = list(frequencies)
        self.total_duration = total_duration

        if randomize_frequencies:
            random.shuffle(self.frequencies)

    def emit(self, frequency, samples):
        """
        Emits a tone at a frequency, for a given number of samples.

        Args:
            frequency (int): The frequency to emit a tone at.
            samples (int): The number of samples to emit the tone for.

        Returns:
            bytes: A packed string of bytes representing the tone.
        """

        tone = math.sin(
            math.pi * frequency * samples / SAMPLE_RATE
        ) * 32000

        return struct.pack('h', int(tone))

    def generate_tones(self):
        """
        Generates a list of tones.

        Returns:
            generator: A list of emitted frequencies, as bytes.
        """

        max_samples = self.total_duration * SAMPLE_RATE
        yielded = 0

        for frequency in self.frequencies:
            for samples in range(0, int(SAMPLE_RATE * TONE_DURATION)):
                tone = self.emit(frequency, samples)
                yield tone
                yielded += 1

                if yielded == max_samples:
                    return

    def save(self, filename):
        """
        Saves the sound to a given file.

        Args:
            filename (str): The name of the destination file to write to.
        """

        logger = getLogger('opawg.audiolipsum')
        logger.debug('Generating %s' % filename)

        with wave.open(filename, 'w') as noise_output:
            noise_output.setparams(
                (
                    CHANNELS,
                    SAMPLE_WIDTH,
                    SAMPLE_RATE,
                    FRAME_COUNT,
                    COMPRESSION_TYPE,
                    COMPRESSION_NAME
                )
            )

            tones = self.generate_tones()
            stream = b''.join(tones)
            noise_output.writeframes(stream)
            noise_output.close()

        logger.debug('Finished %s' % filename)
