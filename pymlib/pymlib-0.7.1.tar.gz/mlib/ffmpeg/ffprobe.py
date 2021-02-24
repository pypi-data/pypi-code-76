# coding: utf-8

import subprocess, logging

mlog = logging.getLogger("mlog")

def get_video_width(file_path):
        """
        计算视频宽
        ffprobe <input> -select_streams v -show_entries stream=width -of default=nk=1:nw=1 -v quiet
        """
        args = ["ffprobe", "-i", file_path, "-select_streams", "v", "-show_entries", "stream=width", "-of", "default=nk=1:nw=1", "-v", "quiet"]
        r = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        if r.returncode != 0:
            mlog.error(r)
            return
        return int(r.stdout)

def get_video_height(file_path):
    """
    计算视频高
    ffprobe <input> -select_streams v -show_entries stream=height -of default=nk=1:nw=1 -v quiet
    """
    args = ["ffprobe", "-i", file_path, "-select_streams", "v", "-show_entries", "stream=height", "-of", "default=nk=1:nw=1", "-v", "quiet"]
    r = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if r.returncode != 0:
        mlog.error(r)
        return
    return int(r.stdout)