"""Generic web download method."""

from pathlib import Path
from urllib.request import urlretrieve

from .logger import logger


log_download, debug_download = logger('Download', info_stdout=True)


def wget(url, fout, skip=False, force=False):
    """Web download.

    Parameters
    ----------
    url: str
        URL to download
    fout: str or Path
        Output file.
    skip: bool, optional
        Skip download if the output file already exists (default: `False`).
        Has the priority over :py:attr:`force`.
    force: bool, optional
        Force download even if the file exists (default: `False`).

    Returns
    -------
    pathlib.Path
        Downloaded file path.

    Raises
    ------
    FileExistsError
        If the file already exists.

    Note
    ----
    The missing sub-directories will be created.

    By default, logging is set at INFO level.
    Use :py:func:`debug_download` function to
    increase or disable the logging output.

    """
    fname = Path(fout)

    if fname.exists():
        if skip:
            return fname
        if not force:
            raise FileExistsError(fname)

    if not fname.exists() or force:
        # Create sub directories (if missing)
        fname.parent.mkdir(parents=True, exist_ok=True)

        # Download the content and save it in `fname`
        log_download.info(url)

        urlretrieve(url, fname)

        log_download.debug('Saved in: %s', fname)

    return fname
