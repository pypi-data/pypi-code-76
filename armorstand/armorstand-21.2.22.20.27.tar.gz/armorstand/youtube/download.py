from youtube_dl import YoutubeDL

from .video_id import get_youtube_id


def download_video(url: str):
    """Download the video in the highest possible format in the same directory

    Parameters:
        url (str): the YouTube video URL or video ID
    """

    opts = {
        "format": "bestvideo+bestaudio",
        "outtmpl": "%(title)s.%(ext)s",
    }

    video_id = get_youtube_id(url)

    with YoutubeDL(opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
