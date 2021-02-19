import platform
import os
import stat
import zipfile
from contextlib import closing
import requests


def download(url, filename):
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        progress = ProgressBar(url.split("/")[-1], total=content_size,
                               unit="KB", chunk_size=chunk_size,
                               run_status="正在下载", fin_status="下载完成")
        with open(filename, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))


class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit,
                             self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def which(program):
    """
    Mimics behavior of UNIX which command.
    """
    # Add .exe program extension for windows support
    if os.name == "nt" and not program.endswith(".exe"):
        program += ".exe"

    envdir_list = [os.curdir] + os.environ["PATH"].split(os.pathsep)

    for envdir in envdir_list:
        program_path = os.path.join(envdir, program)
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return program_path
    return False


# ===============================================================================
# 检测 ffmpeg 是否安装，如果没有就下载并安装
# ===============================================================================

user = os.path.expanduser('~')
# print(user)
wood = f"{user}{os.sep}.wood"
# print(wood)
bin = f"{wood}{os.sep}ffmpeg{os.sep}bin"
# print(bin)
os.environ["PATH"] += f"{os.pathsep}{bin}"
# print(os.environ["PATH"])
# print(which("ffmpeg"))

if not which("ffmpeg"):
    print("缺少 ffmpeg，准备下载")
    if not os.path.exists(wood):
        os.mkdir(wood)
        print(f"{wood} 目录创建成功")

    # 下载 window 版本
    if os.name == "nt":
        # 区分系统位数
        bit = platform.architecture()[0]
        if bit == "32bit":
            url = "http://teaching-aes.codemao.cn/test/ffmpeg-win32.zip"
        elif bit == "64bit":
            url = "http://teaching-aes.codemao.cn/test/ffmpeg-win64.zip"
    # 下载 mac 版本
    elif os.name == "posix":
        url = "http://teaching-aes.codemao.cn/test/ffmpeg-mac.zip"

    filename = f"{wood}{os.sep}ffmpeg.zip"
    # 下载 ffmpeg 压缩包
    download(url, filename)
    # 读取压缩包
    archive = zipfile.ZipFile(filename)
    # 解压
    for file in archive.namelist():
        archive.extract(file, wood)
    # os.remove(filename)

    # mac 下需要给 bin 文件设置可执行权限
    if os.name == "posix":
        names = ["ffmpeg", "ffplay", "ffprobe"]
        for name in names:
            filename = f"{bin}{os.sep}{name}"
            os.chmod(filename, stat.S_IXUSR)

    print("ffmpeg 安装成功")




