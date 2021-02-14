# -*- coding: utf-8 -*-

"""Main module."""
import os
import typing
from pathlib import Path

import pyperclip
from wand.color import Color
from wand.image import Image

PathLike = typing.Union[str, os.PathLike]


def convert(
    image: PathLike,
    size: int,
    filename: PathLike,
    background: str = "white",
    gravity: str = "center",
    alpha: bool = False,
    colors: int = 256,
    interpolate: str = "nearest",
) -> None:
    with Image(filename=image, background=Color(background)) as i:
        i.interpolate_method = interpolate
        i.alpha_channel = alpha
        i.transform(resize="%dx%d^" % (size, size))
        i.crop(width=size, height=size, gravity=gravity)
        i.quantize(colors, None, 0, False, False)
        i.save(filename=filename)


usage = """<link rel="apple-touch-icon" sizes="57x57" href="%sapple-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="%sapple-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="%sapple-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="%sapple-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="%sapple-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="%sapple-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="%sapple-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="%sapple-icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="%sapple-icon-180x180.png">
<link rel="icon" type="image/png" sizes="192x192"  href="%sandroid-icon-192x192.png">
<link rel="icon" type="image/png" sizes="32x32" href="%sfavicon-32x32.png">
<link rel="icon" type="image/png" sizes="96x96" href="%sfavicon-96x96.png">
<link rel="icon" type="image/png" sizes="16x16" href="%sfavicon-16x16.png">
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="msapplication-TileImage" content="%sms-icon-144x144.png">"""


def generate(_image: PathLike, _output: PathLike, base: str = "/") -> None:
    image = Path(_image)
    output = Path(_output)

    if output.exists() and not output.is_dir():
        raise ValueError("%s does exist and is not a directory" % output)

    # make sure the output dir exists
    output.mkdir(parents=True, exist_ok=True)

    if False:
        with Image(width=32, height=32, background=Color("white")) as ico:
            with Image(filename=image, background=Color("white")) as img:
                for size in [16, 32, 48, 64]:
                    print("Processing favicon.ico (%dx%d)" % (size, size))
                    with img.clone() as i:
                        i.interpolate_method = "nearest"
                        i.alpha_channel = False
                        # i.resize(size, size, filter="point")
                        i.transform(resize="%dx%d^" % (size, size))
                        i.crop(width=size, height=size, gravity="center")
                        i.quantize(256, None, 0, False, False)
                        ico.sequence.append(i)
                ico.save(filename=output / "favicon.ico")

            for size in [57, 60, 72, 76, 114, 120, 144, 152, 180]:
                print("Processing apple icon (%dx%d)" % (size, size))
                convert(image, size, output / ("apple-icon-%dx%d.png" % (size, size)))

            for size in [36, 48, 72, 96, 114, 192]:
                print("Processing android icon (%dx%d)" % (size, size))
                convert(image, size, output / ("android-icon-%dx%d.png" % (size, size)))

            for size in [16, 32, 96]:
                print("Processing favicon (%dx%d)" % (size, size))
                convert(image, size, output / ("favicon-%dx%d.png" % (size, size)))

            for size in [70, 144, 150, 310]:
                print("Processing ms icon (%dx%d)" % (size, size))
                convert(image, size, output / ("ms-icon-%dx%d.png" % (size, size)))

    # print usage
    templated = usage % tuple([base] * 14)
    print("")
    print("To use the favicons, paste this into the <head> of your website.")
    print("We already copied it into your clipboard!")
    print("")
    pyperclip.copy(templated)
    print(templated)
