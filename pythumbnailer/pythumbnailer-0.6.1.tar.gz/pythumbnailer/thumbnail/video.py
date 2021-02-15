#!/usr/bin/env python
from datetime import timedelta
from itertools import chain
from pathlib import Path
from time import gmtime
import json
import logging
import subprocess

from .. import utils

XDG_SIZE = utils.XDG_SIZE
Format = utils.Format

logger = logging.getLogger(__name__)


def _probe(ifile: Path, verbose: bool):
    loglevel = ['-v', 'quiet']
    if verbose:
        loglevel = []
    probe_command = [
        'ffprobe',
        *loglevel,
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        ifile,
    ]
    json_text = subprocess.check_output(probe_command, text=True)
    return json.loads(json_text)


def video_title(probe, ipath: Path):
    # TODO: Get this from some video tag ???
    return ipath.stem


def video_size(probe):
    # Usually there's only a single video stream, but there might be more...
    w = max([s['width'] for s in probe['streams'] if s['codec_type'] == 'video'], default=None)
    h = max([s['height'] for s in probe['streams'] if s['codec_type'] == 'video'], default=None)
    if None in (w, h):
        return None
    else:
        return utils.Resolution(width=w, height=h)


def video_time(probe, ipath: Path):
    # TODO: Get this from some video tag ???
    return utils.TimePoint(
        tpl=gmtime(ipath.stat().st_ctime),
        accurate=False,
    )


def thumbnail(ifile: Path, ofile: Path, *, size: XDG_SIZE, fmt: Format, mime: str, template=[], verbose=False, overlay=None, **options):
    loglevel = ['-v', 'quiet']
    if verbose:
        loglevel = []
    probe = _probe(ifile, verbose)
    raw_duration = probe['format']['duration']
    duration_seconds = round(float(raw_duration))
    duration_string = str(timedelta(seconds=duration_seconds))
    logger.debug('Duration: "%s" => "%s"', raw_duration, duration_string)

    inputs = [ifile]
    filters = [
        'thumbnail',
        # Scale towards the resolution, keeping the aspect ratio
        'scale=%s' % ':'.join([
            "'min(%d, iw)':'min(%d, ih)'" % size.res.tpl,
            'force_original_aspect_ratio=decrease',
        ]),
        # Pad the rest of the size with transparent pixels
        'pad=%s' % ':'.join([
            '%d:%d' % size.res.tpl,
            'x=(ow-iw)/2',
            'y=(oh-ih)/2',
            "color=0x00000000",  # Transparent
        ]),
        'drawtext=%s' % ':'.join([
            # Center horizontally, on the bottom
            'x=(w-text_w)/2',
            'y=(h-line_h)-1',
            # Font Settings
            'fontsize=%d' % (size // 7),  # Should take about 1/4 of the height
            'borderw=1', 'bordercolor=black',
            'fontcolor=white',
            # Escape the text, twice
            'expansion=none',
            'text=%s' % duration_string.replace(':', r'\\:'),
        ]),
    ]
    if overlay is True:
        # Default to a size-specific play circle
        overlay = utils.template('play-circle-regular.%d.png' % int(size), *template)

    if overlay is not None:
        if not overlay.exists():
            raise Exception('Invalid overlay file: %s' % overlay)
        # Overlay the file, without processing
        inputs.append(overlay)
        filters.append('overlay=%s' % ':'.join([
            # Center overlay on the main frame
            'x=(main_w-overlay_w)/2',
            'y=(main_h-overlay_h)/2',
        ]))

    thumbnail_command = [
        'ffmpeg',
        '-y',  # Overwrite existing file
        *loglevel,
        *chain.from_iterable([['-i', f] for f in inputs]),
        '-filter_complex', ','.join(filters),
        '-frames:v', '1',  # Single frame
        # Output Format and Codec
        '-f', 'image2',
        '-codec', fmt.ffmpeg_codec,
        ofile,
    ]
    subprocess.run(thumbnail_command)
    return utils.ThumbnailData(
        path=ofile,
        original=ifile,
        title=video_title(probe, ifile),
        size=video_size(probe),
        time=video_time(probe, ifile),
        mime=fmt.mime,
        omime=mime,
    )


def info(ifile: Path, ofile: Path, *, size: XDG_SIZE, fmt: Format, mime: str, template=[], verbose=False, overlay=None, **options):
    probe = _probe(ifile, verbose)
    return utils.ThumbnailData(
        path=ofile,
        original=ifile,
        title=video_title(probe, ifile),
        size=video_size(probe),
        time=video_time(probe, ifile),
        mime=fmt.mime,
        omime=mime,
    )


if __name__ == '__main__':
    import argparse
    import shutil

    parser = argparse.ArgumentParser(description='Create thumbnail for video files')

    parser.add_argument('file', type=Path,
                        help='The input file name to thumbnailize')
    parser.add_argument('output', type=Path,
                        help='The thumbnail file name')
    parser.add_argument('-s', '--size', type=utils.Enum_type(XDG_SIZE),
                        choices=utils.Enum_choices(XDG_SIZE),
                        default=XDG_SIZE.large,
                        help='Create the given size. Defaults to %(default)s')
    parser.add_argument('-m', '--format', type=utils.Enum_type(Format, only_value=True),
                        choices=utils.Enum_choices(Format),
                        default=Format.thumbnails_default,
                        help='The image format for thumbnails. Defaults to %(default)s')
    parser.add_argument('--template', type=Path,
                        action='append', default=[],
                        help='Extra template location to use. Overrides other locations')
    parser.add_argument('--play-overlay', type=Path,
                        default=True,
                        metavar='OVERLAY_FILE',
                        help='Override the "play" image to overlay on the thumbnail')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Show debug messages')
    args = parser.parse_args()

    utils.setup_logging(args.verbose)

    # Hard Requirements
    for cmd in ['ffmpeg', 'ffprobe']:
        if shutil.which(cmd) is None:
            parser.error(f'Missing executable: {cmd}')

    thumbnail(args.file, args.output,
              size=args.size,
              fmt=args.format,
              template=args.template,
              verbose=args.verbose,
              overlay=args.play_overlay,
              )
