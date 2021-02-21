from NightWindAudioLib import media_tool
from pydub import AudioSegment as a
from pydub.playback import play
import os


sound = a.from_mp3("channel" + os.sep + "模式之歌.mp3")
sound_channel = sound.split_to_mono()
sound_single = sound.set_channels(1)
sound_double = sound_single.set_channels(2)
print(sound.channels)
play(sound_single)
