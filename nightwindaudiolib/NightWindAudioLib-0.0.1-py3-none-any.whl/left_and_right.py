from NightWindAudioLib import media_tool
from pydub import AudioSegment as a
from pydub.playback import play
import os

bcm = a.from_mp3("channel" + os.sep + "编程猫的梦想.mp3")
channels = bcm.split_to_mono()
left, right = channels[0], channels[1]
l, r = a.empty(), a.empty()

for i in range(len(bcm), 5000):
    if i % 10000 == 0:
        l += left[i:i + 5000].fade_in(900).fade_out(900)
        r += right[i:i + 5000].apply_gain(-120.0)
    else:
        l += left[i:i + 5000].apply_gain(-120.0)
        r += right[i:i + 5000].fade_in(900).fade_out(900)

play(l)
