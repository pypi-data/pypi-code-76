import 图快

# TODO: 添加执行接口（输入木兰源码，返回输出内容）

# 参考： https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

code = """
i = [0,1,2]
for j in i :
    print(j)
"""
def 运行():
    源码 = 代码文本框.获取(1.0, "end-1c")  # 获取当前选中的文本
    with stdoutIO() as s:
        try:
            exec(code)
        except:
            print("Something wrong with the code")
    输出文本框.插入(1.0, s.getvalue())

窗口 = 图快.主窗口类()
窗口.标题('木兰笔谈')
窗口.尺寸('800x600+100+100')

代码文本框 = 图快.文本框类(窗口, 高度=3)
代码文本框.常规布局()

按钮 = 图快.按钮类(窗口, 文本='运行', 宽度=15, 高度=2, 命令=运行)
按钮.常规布局()

输出文本框 = 图快.文本框类(窗口, 高度=3)
输出文本框.常规布局()

窗口.主循环()