# coding: utf-8

import mlib
from mlib import ffmpeg

def test_video_info():
    r = ffmpeg.get_video_height(r"C:\Users\Administrator\Downloads\11111.mp4")
    print(r)

test_video_info()