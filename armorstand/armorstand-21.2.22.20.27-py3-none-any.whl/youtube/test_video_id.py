from .video_id import get_youtube_id


def test_video_id():
    assert (
        get_youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    )
    assert (
        get_youtube_id(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&otherparams=anything"
        )
        == "dQw4w9WgXcQ"
    )

    assert get_youtube_id("youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    assert get_youtube_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"
