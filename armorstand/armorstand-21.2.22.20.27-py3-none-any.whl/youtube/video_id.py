def get_youtube_id(youtube_url: str):
    """Get the YouTube video ID from a URL

    Parameters:
        youtube_url (str): a YouTube video URL

    >>> get_youtube_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    "dQw4w9WgXcQ"
    >>> get_youtube_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ&otherparams=anything')
    "dQw4w9WgXcQ"
    >>> get_youtube_id('youtu.be/dQw4w9WgXcQ')
    "dQw4w9WgXcQ"
    >>> get_youtube_id('dQw4w9WgXcQ')
    "dQw4w9WgXcQ"
    """

    if "youtube.com" in youtube_url:
        # Regular URL, need to check and other queries in URL
        video_id = youtube_url.split("?v=")[1].split("&")[0]

    elif "youtu.be" in youtube_url:
        # Shortened URL
        video_id = youtube_url.split("/")[1]

    elif len(youtube_url) == 11:
        # Each video ID is 11 characters
        video_id = youtube_url

    else:
        raise Exception("Unable to find YouTube video ID")

    return video_id
