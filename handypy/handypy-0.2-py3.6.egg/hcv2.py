"""
Handy CV2
=========

"""
import cv2 as _cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def putText(image: np.ndarray, text: str,
            org=(0, 0),
            font=_cv2.FONT_HERSHEY_PLAIN,
            fontScale=1, color=(0, 0, 255),
            thickness=1,
            lineType=_cv2.LINE_AA,
            bottomLeftOrigin=False):
    return _cv2.putText(image, text, org, font, fontScale, color, thickness, lineType, bottomLeftOrigin)


def putChineseText(image: np.ndarray, text: str,
                   org=(0, 0),
                   font='NotoSansCJK-Bold.ttc',
                   fontScale=1, color=(0, 0, 255),
                   thickness=1,
                   lineType=None,
                   bottomLeftOrigin=False):
    if bottomLeftOrigin:
        org[1] = image.shape[1] - org[1]

    if thickness!=1:
        print("Use fontScale to control thickness.")
    if lineType is not None:
        print("Use font to control style.")

    try:
        font = ImageFont.truetype(font, fontScale)
    except OSError:
        if font == "":
            print("Download default font from https://github.com/googlefonts/noto-cjk/blob/master/NotoSansCJK-Bold.ttc")
            print("And put it to your system path, or local path.")
        else:
            print("Download missing font %s" % font)

    img_PIL = Image.fromarray(image)
    draw = ImageDraw.Draw(img_PIL)
    draw.text(org, text, font=int(font*12), fill=color[::-1])
    return np.asarray(img_PIL)
