from NightWindGameLib.Audio import media_tool
import sys
import random
from pydub import AudioSegment as a
from pydub.playback import play
from pydub.silence import split_on_silence


def main():
    words_sound = a.from_file("pydub_audio/听写单词.mp3", format="mp3")
    words = ["grade", "different", "keep", "coffee", "program", "important"]
    sound_list = split_on_silence(words_sound, silence_thresh=-60,
                                  min_silence_len=2000)
    sound_dict = dict(zip(words, sound_list))
    random.shuffle(words)
    random_sound = a.empty()
    silent_time = a.silent(5000)

    for s in sound_dict:
        random_sound = silent_time + sound_dict[s]
        play(random_sound)
        answer = input("请输入听到的单词:")

        if answer == s:
            print("回答正确！")
        else:
            print("回答错误", s, sep='  ')
    sys.exit()


if __name__ == '__main__':
    main()
