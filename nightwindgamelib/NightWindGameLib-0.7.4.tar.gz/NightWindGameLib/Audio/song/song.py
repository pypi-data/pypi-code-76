from NightWindGameLib.Audio import media_tool
from pydub import AudioSegment as a
from pydub.playback import play
import os
import random


def get_song(path):
    files = os.listdir(path)
    sound_ext = [".mp3", ".wav", ".flac", ".ape"]
    music = {}

    for file in files:
        file_name, ext = os.path.splitext(file)
        if ext in sound_ext:
            new = ext[1:]
            sound = a.from_file(file, format=new)[3000:8000]
            music[file_name] = sound

    songs = list(music.keys())
    random.shuffle(songs)

    for s in songs:
        play(music[s].reverse())
        answer = input("请输入听到的歌曲名称：")

        if answer == s:
            print("回答正确！")
        else:
            print("回答错误！正确的歌曲名为：%s" % s)


if __name__ == '__main__':
    get_song(".")
