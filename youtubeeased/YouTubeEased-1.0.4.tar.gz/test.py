from YouTubeEased.utils import Checker, VideoHandle
from YouTubeEased import YouTubeEased


URL = "https://www.youtube.com/watch?v=qb74Eieal24&feature=youtu.be&ab_channel=Snacksss"
# yt = YouTubeEased(URL)
# yt.is_good_url()
# Checker(URL).is_good_url()
# (VideoHandle(URL).is_good_url())

with YouTubeEased(URL) as youtube:
    a = youtube.is_good_url()
    print(a)
