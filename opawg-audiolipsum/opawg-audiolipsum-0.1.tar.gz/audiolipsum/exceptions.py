class AudioLipsumError(Exception):
    """
    Raised when an error occurs within the Audio Lipsum library.
    """


class ExternalLibraryError(AudioLipsumError):
    """
    Raised when an external library cannot be found.
    """
