from NightWindGameLib.Audio import media_tool
from pydub import AudioSegment as a
from pydub.playback import play
import sys


def main():
    bcm = a.from_mp3("remix/四句儿歌编程猫.mp3")
    xk = a.from_mp3("remix/四句儿歌小可.mp3")
    length = len(bcm) - len(xk)

    if length >= 0:
        xk += a.silent(length)
    elif length < 0:
        bcm += a.silent(abs(length))

    s_bcm = list(bcm[5500::3000])
    s_xk = list(xk[5500::3000])
    song = a.empty()

    for i in range(len(s_bcm)):
        if i % 2 == 0:
            song += s_bcm[i].fade_out(300).fade_in(300)
        else:
            song += s_xk[i].fade_out(300).fade_in(300)

    last_bcm = bcm[11000:]
    last_xk = xk[11500:]
    last = last_bcm.overlay(last_xk, position=300)
    start = bcm[0:5500]
    complete = start + song + last

    play(complete)
    sys.exit()


if __name__ == '__main__':
    main()
