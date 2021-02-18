from NightWindGameLib.Audio import media_tool
from pydub import AudioSegment as a
from pydub.playback import play


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

play(song)
