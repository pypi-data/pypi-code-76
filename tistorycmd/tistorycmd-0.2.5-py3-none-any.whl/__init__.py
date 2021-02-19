from pyfiglet import Figlet
from .auth import *
from .server import *
from .blog import *

# 타이틀 출력
fig = Figlet(font='slant')
print(fig.renderText('tistory cmd'))