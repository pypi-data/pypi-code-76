#!/usr/bin/env python
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
import argparse
import logging
import mimetypes
import os

from . import utils
from . import thumbnail

from argparse_utils import enum_action, mapping_action
from PIL import Image
import jinja2

XDG_SIZE = utils.XDG_SIZE

logger = logging.getLogger(__name__)


@dataclass
class Output:
    message: str


@dataclass
class MIME:
    mime: str
    split: bool = True

    @property
    def valid(self):
        return self.mime is not None and '/' in self.mime

    def __str__(self):
        return self.mime

    @property
    def type(self):
        if self.valid and self.split:
            return self.mime.split('/')[0]
        else:
            # Should return "None" when invalid
            return self.mime


@dataclass(frozen=True)
class GlobalData:
    """
    Data global to whole task list. Should be passed to all templates.

    - tasks: List of `Task.message` that are to be done.
    """
    title: str
    insecure: bool
    static: str  # URL
    tasks: [str] = field(default_factory=list)


@dataclass(frozen=True)
class TaskInput:
    fname: Path
    mime: MIME


@dataclass
class Task:
    message: str
    mime_types: List[str]
    inputs: List[TaskInput] = field(init=False, default_factory=list)
    outputs: List[object] = field(init=False, default=None)

    @property
    def todo(self):
        return len(self.inputs) > 0

    def doit(self, **kwargs):
        """
        Internal entrypoint for the task.

        DO NOT OVERRIDE ON subclasses, see `do_all`
        """
        self.do_pre(**kwargs)
        self.outputs = self.do_all(**kwargs)
        self.do_post(**kwargs)

    def do_pre(self, **kwargs):
        """
        Setup Task. Runs before `do_all`.

        Can be overriden on sub-classes.
        """
        pass

    def do_post(self, **kwargs):
        """
        Tear Down Task. Runs after `do_all`.

        Can be overriden on sub-classes.
        """
        pass

    def do_all(self, **kwargs):
        """
        Main entrypoint for the task. Defaults to running `do_single` for each
        input, stateless.

        Can be overriden on sub-classes.
        """
        return [self.do_single(inp, **kwargs) for inp in self.inputs]

    def do_single(self, inp: TaskInput, **kwargs):
        """
        Entrypoint for simple stateless tasks. Called by `do_all` for each
        input.
        """
        raise NotImplementedError


class TaskThumbnails(Task):
    def __init__(self):
        super().__init__('Thumbnails', mime_types=[
            'image',
            'video',
        ])
        self.creators = {
            'image': thumbnail.image,
            'video': thumbnail.video,
        }

    def do_pre(self, *, args, **kwargs):
        dir_mod, self.file_mod = (0o705, 0o604) if args.public else (0o700, 0o600)

        toplevel = args.basedir / utils.XDG_SHARED_FOLDER
        logger.debug('Setup directories @ %s', toplevel)
        utils.mkdir(toplevel, dir_mod)
        for subdir in ['normal', 'large', 'fail']:
            subpath = toplevel / subdir
            utils.mkdir(subpath, dir_mod)

    def do_single(self, inp, *, sizes, largest_size, **kwargs):
        logger.debug('- %s', inp.fname)
        creator = self.creators[inp.mime.type]
        result = dict()
        for size in sizes:
            result[size] = self.do_thumbnail(inp.fname, size, creator, mime=inp.mime.type, **kwargs)
        if None in result.values():
            logger.error('Broken File: %s', inp.fname)
        return result[largest_size]  # Show only the biggest size on the HTML

    def do_thumbnail(self, ifname, size, creator, mime, *, args, **kwargs):
        tpath = utils.thumbnail_path(ifname, size, args.format, basedir=args.basedir)
        logger.debug('Thumbnail: %s', tpath)
        existing = tpath.exists()
        result = True
        if existing:
            logger.debug('- Thumbnail exists!')
            os.chmod(tpath, self.file_mod)
        if args.force or not existing:
            logger.debug('- Saving ...')
            try:
                result = creator.thumbnail(ifname, tpath,
                                           size=size,
                                           fmt=args.format, mime=mime,
                                           template=args.template,
                                           verbose=args.verbose,
                                           # MIME Type-specific
                                           overlay=args.thumb_overlay)
                logger.debug('- Saved!')
            except Exception as e:
                logger.debug('- Failed!')
                logger.debug('=> %r', e)
                # TODO: Write to the /fail/ directory
                # See https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html#FAILURES
                result = None  # Explicit
        else:
            logger.debug('- Skipping!')
        if result is not None:
            result = creator.info(ifname, tpath,
                                  size=size,
                                  fmt=args.format, mime=mime,
                                  verbose=args.verbose)

        return result

    def do_post(self, *, jinja, args, gdata, largest_size, **kwargs):
        template = jinja.get_template('photo-album.html')
        logger.debug('HTML Template @ "%s"', template.filename)

        htmlname = args.basedir / 'index.html'
        logger.debug('HTML @ "%s"', htmlname.resolve())

        # Ignore files with errors
        with htmlname.open(mode='w') as htmlfile:
            s = template.stream({
                'gdata': gdata,
                'thumbnails': [obj for obj in self.outputs if obj is not None],
                'maxsize': '%d' % largest_size.value,
            })
            s.dump(htmlfile)


class TaskTracks(Task):
    def __init__(self):
        super().__init__('Tracks', mime_types=[
            'application/gpx+xml'
        ])

    def do_single(self, inp: TaskInput, args, **kwargs):
        # TODO: Parse the XML for more metadata
        # https://www.topografix.com/GPX/1/1/#type_metadataType
        # XPath: /metadata/name
        return {
            'title': inp.fname.stem,
            'url': inp.fname.relative_to(args.basedir),
        }

    def do_post(self, *, jinja, args, gdata, **kwargs):
        template = jinja.get_template('tracks.html')
        logger.debug('HTML Template @ "%s"', template.filename)

        htmlname = args.basedir / 'tracks.html'
        logger.debug('HTML @ "%s"', htmlname.resolve())

        with htmlname.open(mode='w') as htmlfile:
            s = template.stream({
                'gdata': gdata,
                'default_tile': args.gpx_defaulttile,
                'tracks': self.outputs,
            })
            s.dump(htmlfile)


OUTPUT_PATHS = {
    '.sh_thumbnails': Output('Shared Thumbnails'),
    'index.html': Output('Main Index'),
    'tracks.html': Output('GPX Tracks'),
}

MIMES = {
    'inode/directory': MIME('inode/directory', split=False),
}
EXT_MIMES = {
    '.gpx': MIME('application/gpx+xml', split=False),
}

TASKS = [
    TaskTracks(),
    # TODO: Task('Recursive Invocation', mime_types=['inode/directory']),
    TaskThumbnails(),
]

# e: Path
SORT_KEY = {
    'name': lambda e: e.name,
    'mtime': lambda e: e.stat().st_mtime,
}


def Directory(location):
    location = Path(location)
    if location.is_dir():
        return location
    else:
        raise argparse.ArgumentTypeError(f'Invalid folder: {location}')


def __main__():
    parser = argparse.ArgumentParser(
        description='Publish static HTML to describe a folder',
        allow_abbrev=False
    )
    parser.add_argument('--basedir',
                        type=Directory, default=Path('.'),
                        help='Base directory to process. Defaults to `%(default)s`')
    parser.add_argument('--sort', action=mapping_action(SORT_KEY),
                        default='name',
                        help='Sort files by metadata. Defaults to `%(default)s`')
    parser.add_argument('--title', default=None,
                        help='Publishing Title. Default to the `--basedir` name')
    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='Overwrite existing thumbnails')
    parser.add_argument('-p', '--public',
                        action='store_true',
                        help='Adjust the file permissions for public read-only access. '
                             'Defaults to the specification, exclusive owner access')
    parser_size = parser.add_mutually_exclusive_group()
    parser_size.add_argument('-s', '--size', action=enum_action(XDG_SIZE),
                             help='Create the given size.')
    parser_size.add_argument('-S', '--sizes-all',
                             action='store_true',
                             help='Create all available sizes')
    parser.add_argument('-m', '--format', type=lambda f: f.value,
                        action=enum_action(utils.Format),
                        default=utils.Format.thumbnails_default.value,
                        help='The image format for thumbnails. Defaults to %(default)s')
    parser.add_argument('--template', type=Path,
                        action='append', default=[],
                        help='Extra template location to use. Overrides other locations')
    parser.add_argument('--static-location', default='',
                        help='The URL (absolute or relative) where the files in `static` are provided. Defaults to being relative to the HTML location')
    parser.add_argument('--no-thumb-play-overlay', dest='thumb_overlay',
                        action='store_const', default=True, const=None,
                        help='Thumbnails: Hide the "play" overlay image. Defaults to an internal one, based on size')
    parser.add_argument('--gpx-defaulttile', default='OpenStreetMap',
                        help='Tracks: The default tile data key (see `static/gpx/multiple.js`). Defaults to %(default)s')
    parser.add_argument('--insecure', action='store_true',
                        help='Do not use any security-related features on the generated files. Useful for tests on `localhost`')
    parser.add_argument('-v', '--verbose',
                        help='Show debug messages',
                        action='store_true')
    args = parser.parse_args()

    utils.setup_logging(args.verbose, shutup=[
        'PIL',
    ])

    Image.init()  # Initialize PIL
    mimetypes.init()  # Initialize MIME types

    # Mapper MIME -> Task
    task_mapper = dict()
    for t in TASKS:
        for mtype in t.mime_types:
            # On conflict, first task wins
            # TODO: Support same file to multiple tasks? Not needed so far
            task_mapper.setdefault(mtype, t)

    # File Selection
    logger.debug('Base Directory: "%s"', args.basedir)
    for element in sorted(args.basedir.iterdir(), key=args.sort):
        if output := OUTPUT_PATHS.get(element.name):
            logger.debug('= "%s": %s', element, output.message)
            continue
        if element.is_dir():
            # Use this as MIME for a directory
            # See: https://specifications.freedesktop.org/shared-mime-info-spec/shared-mime-info-spec-latest.html#idm140625828597376
            mimetype = MIMES['inode/directory']
        else:
            # Discover MIME type based on file name
            raw_mimetype = mimetypes.guess_type(element)
            mimetype = raw_mimetype[0]
            if mimetype is None:
                # TODO: Sniff the file contents? Use `file --mime-type`?
                # No automatic detection, fallback to EXT_MIMES
                mimetype = EXT_MIMES.get(''.join(element.suffixes))
            else:
                # Check the MIMES for custom MIME objects
                mimetype = MIMES.get(mimetype, MIME(mimetype))
        logger.debug('- "%s": %s', element, mimetype)
        # `mimetype` can be None
        if mimetype and mimetype.type in task_mapper:
            telement = TaskInput(element, mimetype)
            # TODO: Turn into generator
            task_mapper[mimetype.type].inputs.append(telement)

    # Size Selection
    if args.sizes_all:
        sizes = [s for s in XDG_SIZE]
    else:
        sizes = args.size or [XDG_SIZE.large]  # Default to building only the "large" thumbnails
    largest_size = sorted(sizes, key=lambda s: s.value, reverse=True)[0]
    logger.debug('Largest Size: %s', largest_size)

    # Global Values
    gdata = GlobalData(
        title=args.title or args.basedir.resolve().name,
        insecure=args.insecure,
        static=args.static_location,
        tasks=[t.message for t in TASKS if t.todo],
    )

    # Jinja2
    jinja = jinja2.Environment(
        loader=utils.JinjaTemplateLoader(*args.template),
        autoescape=jinja2.select_autoescape(('html', 'xml')),
    )

    logger.debug('Tasks')
    for task in TASKS:
        if task.todo:
            logger.debug('- %s| %d items', task.message, len(task.inputs))
            # for tin in task.inputs:
            #     logger.debug('  > %s| %s', tin.mime.type, tin.fname)
            task.doit(**locals())  # This is a very ugly hack...
            # for tout in task.outputs:
            #     logger.debug('  < %r', tout)


if __name__ == '__main__':
    import sys
    sys.exit(__main__())
