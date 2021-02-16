
"""
PythonModule for Windows
---------------------------------------------------
This module can only run on Windows10+!
Please do not call or run on Linux and MacOS systems
"""
import getpass
import glob
import os
import platform
import shutil
import subprocess
import sys
import time
import zipfile

import pydub
from pydub.playback import play


__doc__ = "PyDll on win32 If you have some questions for this Program,Please send email to 3150237154@qq.com "
__version__ = "1.1.0-debug"
Now_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
Data = {"System" : platform.platform(),
        "UserName": getpass.getuser(),
        "NowTime": Now_Time,
        "File": sys.argv[0],
        "Args": sys.argv[1:]}
Filelist = []
d_filelist = []
sys.stderr.write(f"PyDll {__version__}\n")
__all__ = ["ari", "fib", "chase_distance", "chase_time", "meet_distance",
           "meet_time", "mkfod", "mkzip", "unzip", "copy", "dirs", "rename",
           "get_module_dir", "deletefile"]


class SameError(OSError):
    """当两个文件或文件夹相同时引发该错误"""


class InputError(Exception):
    """当输入的值为空时引发该错误"""


class SystemVersionError(Exception):
    """当操作系统不正确时引发该错误"""


class NotFoundError(OSError):
    """当未找到指定的文件或文件夹时引发该错误"""


def deletefile(name):
    """删除指定后缀名的文件"""
    for root, d, files in os.walk(os.getcwd()):
        for p in glob.glob1(root, f"*.{name}"):
            d_filelist.append(os.path.join(root, p))
    while True:
        for i in d_filelist:
            try:
                os.remove(i)
                del d_filelist[d_filelist.index(i)]
            except PermissionError:
                del d_filelist[d_filelist.index(i)]
                continue
        if len(d_filelist) == 0:
            break
    return True

def musicfile(filename):
    name = os.path.basename(filename)
    print(filename)
    if os.path.isfile(filename):
        sys.stderr.write(f"播放音乐: {name}\n")
        if (fd := filename[-4:]) == ".wav":
            play(pydub.AudioSegment.from_wav(filename))
        elif fd == ".mp3":
            play(pydub.AudioSegment.from_mp3(filename))
        elif fd == ".ogg":
            play(pydub.AudioSegment.from_ogg(filename))
        else:
            sys.stderr.write(f"暂时还不支持该类型音乐 {fd}")
    else:
        sys.stderr.write(f"不存在该文件{name}")



def ari(maxnum: int, diff: int = 1) -> list:
    """返回到 maxnum 的等差数列"""
    numlist = []
    a = 0
    while (a < maxnum):
        a += diff
        numlist.append(a)
    return numlist


def fib(maxnum: int) -> list:  #
    """返回到 maxnum 的斐波那契数列"""
    result = []
    a, b = 0, 1
    while b < maxnum:
        result.append(b)
        a, b = b, a+b
    return result


def chase_distance(speed_1: int, speed_2: int, meet_time: int) -> int:
    """追及问题求追及路程"""
    speedx = abs(speed_1-speed_2)
    distance = speedx*meet_time
    return distance


def chase_time(speed_1: int, speed_2: int, distance: int) -> int:
    """追及问题求追及时间"""
    speedx = abs(speed_1-speed_2)
    meet_time = distance/speedx
    return meet_time


def meet_distance(speed_1: int, speed_2: int, meet_time: int) -> int:
    """相遇问题求相遇路程"""
    speedh = speed_1+speed_2
    distance = speedh*meet_time
    return distance


def meet_time(speed_1: int, speed_2: int, distance: int) -> int:
    """相遇问题求相遇时间"""
    speedh = speed_1+speed_2
    meet_time = distance/speedh
    return meet_time


def mkfod(filename: str, inputstring: str = None, mkmode: bool = False, wmode: bool = False) -> int:
    """创建一个文件或文件夹"""
    if os.path.isfile(filename) or os.path.isdir(filename):
        raise SameError("相同的文件或文件夹")
    elif mkmode == True:
        print(f"正在新建文件夹: {filename}")
        os.mkdir(filename)
    elif mkmode == False:
        print(f"正在新建文件: {filename}")
        if wmode == True:
            with open(filename, "a+") as _:
                _.write(inputstring)
        else:
            with open(filename, "w") as _:
                _.close()
    return True

def _Getzip(input_path: str, result: list) -> None:
    """
    对目录进行深度优先遍历
    \ninput_path:
    \nresult:
    """
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '\\' + file):
            _Getzip(input_path + '\\' + file, result)
        else:
            result.append(input_path + "\\" + file)


def mkzip(input_path: str, output_name: str, output_path: str = ".\\") -> str:
    """
    压缩文件
    \ninput_path: 压缩的文件夹路径
    \noutput_path: 解压（输出）的路径
    \noutput_name: 压缩包名称
    """
    f = zipfile.ZipFile(output_path + '/' + output_name,
                        'w', zipfile.ZIP_DEFLATED)
    filelists = []
    _Getzip(input_path, filelists)
    for file in filelists:
        f.write(file)
    # 调用了close方法才会保证完成压缩
    f.close()
    return output_path + r"/" + output_name


def unzip(zipname: str, unzipdir: str, mode=True) -> str:
    """
    解压格式为'.zip'的文件
    \nzipname: 压缩文件名
    \nunzipdir: 解压到的文件夹
    \nmode: 选择是否解压单个文件
    """
    uz = zipfile.ZipFile(zipname)
    if mode:
        print(f"解压所有文件至: {unzipdir}")
        uz.extractall(unzipdir)
    else:
        print("当前文件夹内的文件:")
        for n in uz.namelist():
            print(n)
        insidefile = str(input("选择一个文件>> "))
        if insidefile != "":
            print(f"解压 {zipname} 至 {unzipdir}")
            uz.extract(insidefile)
        else:
            raise InputError("insidefile 的值不能为空！")
    uz.close()
    subprocess.Popen(f"explorer {unzipdir}")
    return unzipdir


def copy(filename: str, filenewdir: str, move=False):
    '''
    复制和拷贝文件及文件夹
    \nfilename: 要执行操作的文件或文件夹
    \nfiledir:  文件或文件夹执行操作后的文件或文件夹
    \nmove:     当为True时拷贝filename至filenewdir,为False时复制filename至filedir
    '''
    if move == False:
        # 复制文件
        if os.path.isdir(filename):
            # 判断是否为目录
            try:
                print(f"将 {filename} 复制到 {filenewdir} ...")
                shutil.copytree(filename, filenewdir)
                print("完成.")
            except OSError as _:
                sys.stderr.write(f"警告：{_}")
        elif os.path.isfile(filename):
            # 判断是否为文件
            print(f"将 {filename} 复制到 {filenewdir} ...")
            shutil.copy(filename, filenewdir)
            print("完成.")
        elif os.path.isfile(filename) == False or os.path.isdir(filename) == False or os.path.isdir(filenewdir) == False:
            # 如果不存在就退出程序
            raise NotFoundError(f"文件或文件夹{filename}不存在！")
    else:
        # 拷贝文件
        if os.path.isfile(filename) or os.path.isdir(filename) and os.path.isdir(filenewdir):
            # 判断要复制的文件或者文件夹和复制后的路径是否存在
            print(f"将 {filename} 移动到 {filenewdir} ...")
            shutil.move(filename, filenewdir)
            print("完成.")
        elif os.path.isfile(filename) == False or os.path.isdir(filename) == False or os.path.isdir(filenewdir) == False:
            # 如果不存在就退出程序
            raise NotFoundError(f"文件或文件夹{filename}不存在！")
    return True

def dirs(path) -> list:
    """
    遍历函数,打印path下的所有文件及文件夹
    """
    file_num = 0
    all_dirs = []
    dir_list = []
    for root, dirs, files in os.walk(path):
        all_dirs.append(dirs)
        for i in files:
            file_path = root + '/' + i
            a = os.path.getsize(file_path)
            b = round(a, 3)
            text = (f'{file_path} [{b} KB]')
            file_num += 1
            dir_list.append([file_num, b, "KB", text])
    return dir_list


def rename(path, name, startNumber, fileType):
    """
    批量重命名文件
    \npath: 文件夹路径
    \nname: 重命名后的主名字
    \nstartNumber: 附加在主名字后的编号
    \nfileType: 重命名后的文件后缀名
    """
    count = 0
    fileList = os.listdir(path)
    for files in fileList:
        old_name = os.path.join(path, files)
        if os.path.isdir(old_name):
            continue
        new_name = os.path.join(
            path, name + str(count + int(startNumber)) + fileType)
        os.rename(old_name, new_name)
        count += 1
    return count


def get_module_dir(name):
    """查询模块位置"""
    path = getattr(sys.modules[name], '__file__', None)
    print(path)
    if not path:
        raise AttributeError('module %s has not attribute __file__' % name)
    return os.path.dirname(os.path.abspath(path))


def _mktempfile(num, dir):
    for temp in range(num):
        mkfod(f"{dir}{temp}.temp", wmode=False)
