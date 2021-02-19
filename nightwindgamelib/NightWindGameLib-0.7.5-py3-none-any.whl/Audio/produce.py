from NightWindGameLib.Audio import media_tool
from pydub import AudioSegment as a
# from pydub.playback import play
import os

sounds = {}
sound = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si", "Do2"]
for i in range(1, len(sound) + 1):
    sounds[str(i)] = a.from_wav("produce" + os.sep + sound[i - 1] + ".wav")

music = a.empty()
song = "1234555066865550445433432432111"

for s in song:
    if s == "0":
        music += a.silent(335)
        continue
    music += sounds[s][100:435]

vocal = a.from_mp3("produce" + os.sep + "人声.mp3")
music = music.overlay(vocal, gain_during_overlay=-5)
# play(music)
music.export("produce" + os.sep + "demo.wav", format="wav")
