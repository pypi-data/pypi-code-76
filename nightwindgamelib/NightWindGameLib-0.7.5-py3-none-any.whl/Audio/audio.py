from pydub import AudioSegment as a
from NightWindGameLib.Audio import media_tool
import sys


def main():
    source = input("请输入要转换的文件名(输入q退出)：")
    result = ''

    while source != 'q' and result != 'q':
        source = input("请输入要转换的文件名(输入q退出)：")
        result = input("请输入转换后的文件名(输入q退出)：")
        sound = a.from_file(source, format=result.split(".")[-1])
        sound.export(result, format=result.split(".")[-1])

    sys.exit()


if __name__ == "__main__":
    main()
