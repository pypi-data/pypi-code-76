#!/usr/bin/env python
from pathlib import Path
import logging
import time

from .. import utils

from PIL import Image

XDG_SIZE = utils.XDG_SIZE
Format = utils.Format

logger = logging.getLogger(__name__)


EXIF_ORIENTATION = 0x0112  # PIL.ExifTags.TAGS with Orientation
EXIF_DATETIME = 0x0132  # PIL.ExifTags.TAGS with DateTime
ORIENTATION_OP = {
    1: [],  # Default
    2: [Image.FLIP_LEFT_RIGHT],
    3: [Image.ROTATE_180],
    4: [Image.FLIP_TOP_BOTTOM],
    5: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
    6: [Image.ROTATE_270],
    7: [Image.FLIP_TOP_BOTTOM, Image.ROTATE_270],
    8: [Image.ROTATE_90],
}


def image_size(image: Image):
    return utils.Resolution(width=image.width, height=image.height)


def image_time(image: Image, ipath: Path):
    # Information taken from:
    # - EXIF tags
    # - File Creation Time
    o_time_exif = None
    # Only if EXIF information is exposed
    if getattr(image, '_getexif'):
        raw_exif = image._getexif()
        if raw_exif is not None:
            dt = raw_exif.get(EXIF_DATETIME, None)
            if dt:
                # Get date from EXIF
                # https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif/datetimeoriginal.html
                try:
                    o_time_exif = time.strptime(dt, '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    # Invalid EXIF format, skip
                    o_time_exif = None
    return utils.TimePoint(
        tpl=o_time_exif or time.gmtime(ipath.stat().st_ctime),
        accurate=o_time_exif is not None
    )


def image_title(image: Image, ipath: Path):
    # File Name, without extension
    # TODO: Get something title/description from EXIF?
    # - https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif/usercomment.html
    #   - ImageDescription (ASCII only)
    #   - UserComment: Supports UTF-8 (write only this)
    return ipath.stem


def thumbnail(ifile: Path, ofile: Path, *, size: XDG_SIZE, fmt: Format, mime: str, template=[], verbose=False, **options):
    image = Image.open(ifile)
    o_size = image_size(image)
    o_time = image_time(image, ifile)
    o_title = image_title(image, ifile)
    ops = []
    # Only if EXIF information is exposed
    if getattr(image, '_getexif'):
        raw_exif = image._getexif()
        if raw_exif is not None:
            # Orientation
            orientation = raw_exif.get(EXIF_ORIENTATION, None)
            if orientation in ORIENTATION_OP:
                ops.extend(ORIENTATION_OP[orientation])
            logger.debug('Orientation: %r', orientation)
    # Modify the image in-place (in RAM, doesn't change the ifile)
    # TODO: Same thing as the video, pad the image to the exact size with transparent pixels
    image.thumbnail(size.res.tpl)
    logger.debug('Transpositions: %r', ops)
    for op in ops:
        image = image.transpose(op)
    with open(ofile, mode='wb') as ofobj:
        image.save(ofobj, fmt.pil_format, **fmt.pil_settings)
    return utils.ThumbnailData(
        path=ofile,
        original=ifile,
        title=o_title,
        size=o_size,
        time=o_time,
        mime=fmt.mime,
        omime=mime,
    )


def info(ifile: Path, ofile: Path, *, size: XDG_SIZE, fmt: Format, mime: str, template=[], verbose=False, **options):
    image = Image.open(ifile)
    return utils.ThumbnailData(
        path=ofile,
        original=ifile,
        title=image_title(image, ifile),
        size=image_size(image),
        time=image_time(image, ifile),
        mime=fmt.mime,
        omime=mime,
    )


if __name__ == '__main__':
    import argparse

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
    parser.add_argument('--template', type=Path,  # Un-used, worth to keep around
                        action='append', default=[],
                        help='Extra template location to use. Overrides other locations')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Show debug messages')
    args = parser.parse_args()

    utils.setup_logging(args.verbose)

    thumbnail(args.file, args.output,
              size=args.size,
              fmt=args.format,
              template=args.template,
              verbose=args.verbose,
              )
