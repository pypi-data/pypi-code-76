#!/usr/bin/env python
import logging
import sys
from enum import Enum, IntEnum
from pathlib import Path
from itertools import chain
from dataclasses import dataclass, field
from time import strftime
from hashlib import md5
from os.path import getmtime
import importlib.resources as res

from jinja2 import BaseLoader, TemplateNotFound


PROJECT_NAME = 'pythumbnailer'
logger = logging.getLogger(__name__)


def setup_logging(verbose, shutup=[]):
    _logging = {
        'fmt': '%(levelname).4s %(name)s@%(funcName)s: %(message)s',
    }
    if verbose:
        _logging['level'] = logging.DEBUG
    try:
        import coloredlogs
        coloredlogs.install(**_logging)
    except ModuleNotFoundError:
        _logging['format'] = _logging.pop('fmt')
        logging.basicConfig(**_logging)
    if verbose:
        # Silence spammy logs
        for mod in shutup:
            logging.getLogger(mod).setLevel(logging.WARNING)


def mkdir(path, dir_mod):
    if path.is_dir():
        # If it exists, make sure the permissions are correct
        path.chmod(dir_mod)
    else:
        # If it doesn't exist, create it
        path.mkdir(mode=dir_mod)


@dataclass(frozen=True)
class Resolution:
    width: int
    height: int

    @property
    def tpl(self):
        """
        Return value as tuple
        """
        return (self.width, self.height)


@dataclass(frozen=True)
class TimePoint:
    tpl: tuple  # Time Tuple
    accurate: bool  # Is this worth showing, or it just for internal consumption?

    def strftime(self, fmt='%Y-%m-%d %H:%M:%S'):
        return strftime(fmt, self.tpl)


# FreeDesktop Thumbnail Managing Standard
# https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html#DIRECTORY
class XDG_SIZE(IntEnum):
    normal = 128
    large = 256

    @property
    # Always squares
    def res(self):
        """
        Return a Resolution object
        """
        return Resolution(width=self.value, height=self.value)


@dataclass(frozen=True)
class ImageFormat:
    """
    A supported image format.
    """
    extension: str
    mime: str
    # Settings for `PIL`
    pil_settings: dict = field(default_factory=dict)
    # `-f` for FFMPEG. Defaults to the `extension`
    ffmpeg_codec: str = None
    # PIL format. Defaults to `extension` in upper-case
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    pil_format: str = None

    def __post_init__(self):
        # Setup the default FFMPEG codec
        object.__setattr__(self, 'ffmpeg_codec', self.ffmpeg_codec or self.extension)
        # Setup the default PIL format
        object.__setattr__(self, 'pil_format', self.pil_format or self.extension.upper())


class Format(Enum):
    JPEG = ImageFormat('jpg',
                       ffmpeg_codec='mjpeg',
                       pil_settings={
                           'optimize': True,
                           'progressive': True,  # Progressive thumbnails
                           'quality': 75,  # /100
                       },
                       mime='image/jpeg')
    PNG = ImageFormat('png',
                      pil_settings={
                          'optimize': True,
                      },
                      mime='image/png')

    def __str__(self):
        return self.name


# FreeDesktop Thumbnail Managing Standard
# Standard File Format is PNG
# https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html#CREATION
Format.thumbnails_default: Format = Format.PNG


# TODO: Support XDG Base Directory Standard
TEMPLATES_LGLOBAL = Path('/usr/share')
TEMPLATES_LUSER = Path('~/.local/share').expanduser()
TEMPLATES_LOCATIONS = [
    TEMPLATES_LGLOBAL.joinpath(PROJECT_NAME, 'templates'),
    TEMPLATES_LUSER.joinpath(PROJECT_NAME, 'templates'),
]
if sys.version_info >= (3, 9):
    TEMPLATES_LOCATIONS.append(
        res.files('pythumbnailer').__enter__() / 'templates',  # Current module Folder
    )
else:
    TEMPLATES_LOCATIONS.append(
        Path(__file__).resolve().parent / 'templates',  # Current installation Folder
    )


def template_locations(*override: Path):
    """
    Return the default search paths, including the overriden locations.

    override: Add the given paths to the beginning of the search paths
    """
    return chain(override, TEMPLATES_LOCATIONS)


def template(fname: str, *override: Path):
    """
    Search for the template named `fname` on the search paths.

    This is for "template" file, non-jinja only.
    """
    # For Jinja templates, use `JinjaTemplateLoader`
    for location in template_locations(*override):
        possible = location.joinpath(fname)
        if possible.exists():
            logger.debug(f'Template[{fname}]: "{possible}"')
            return possible
    return None  # Not found


class JinjaTemplateLoader(BaseLoader):
    # https://jinja.palletsprojects.com/en/2.11.x/api/?highlight=choiceloader#jinja2.BaseLoader
    def __init__(self, *override: Path):
        self._overrides = override

    def get_source(self, environment, name):
        path = template(name, *self._overrides)
        if not path.exists():
            raise TemplateNotFound(name)
        mtime = getmtime(path)
        with path.open('r', encoding='utf-8') as obj:
            source = obj.read()
        return source, str(path), lambda: mtime == getmtime(path)


# FreeDesktop Thumbnail Managing Standard
# Shared Thumbnails Only
# https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html#SHARED
XDG_SHARED_FOLDER = '.sh_thumbnails'


@dataclass(frozen=True)
class ThumbnailData:
    path: Path
    original: Path
    title: str  # Image "title", description, whatever you want to call it
    time: TimePoint
    mime: str  # Thumbnail MIME type
    omime: str = None  # Original MIME type
    size: Resolution = None


def _thumbnail_startpath(fname: Path, basedir: Path = None):
    return basedir or fname.parent


def thumbnail_hash(fname: Path, basedir: Path = None):
    """
    Get the XDG hash for the given filename. Implements
    https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html#THUMBSAVE,
    for the shared thumbnails variant.

    fname: The Path to calculate the hash.
    basedir: The root Path to consider when calculating the name.
            When `None`, use the directory of the given `fname`.
            Defaults to `None`
    """
    start_path = _thumbnail_startpath(fname, basedir)
    to_hash = fname.relative_to(start_path)
    return md5(to_hash.as_posix().encode('utf-8')).hexdigest()


def thumbnail_path(fname: Path, size: XDG_SIZE, fmt: Format, basedir: Path = None):
    """
    Get the thumbnail path for the given filename and size, in the given format.

    fname: The Path to calculate the filename
    basedir: The root Path to consider when calculating the name.
            When `None`, use the directory of the given `fname`.
            Defaults to `None`
    size: The XDG_SIZE of the thumbnail
    fmt: The Format of the thumbnail
    """
    start_path = _thumbnail_startpath(fname, basedir)
    hexhash = thumbnail_hash(fname, basedir)
    tname = '%s.%s' % (hexhash, fmt.extension)
    return start_path / XDG_SHARED_FOLDER / size.name / tname
