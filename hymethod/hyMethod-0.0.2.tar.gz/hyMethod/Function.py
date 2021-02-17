from time import *
from tkinter import *
from os import *
from random import *
import tkinter.messagebox
import time,os,sys
import webbrowser
from qrcode import *

def wait1():
    import time
    time.sleep(1)

def wait2():
    import time
    time.sleep(2)

def cc(text,timee=0.1):
    import sys,time
    for i in text:
        time.sleep(timee)
        print(i,end='',flush = True)
        sys.stdout.flush()
    print("",end="\n")

def wait(timel):
    import time
    time.sleep(timel)

def hy_dark(a):#暗的输出logo
    for x in range(len(a)):
        if a[x]=="1":#红色
            print("\033[41m ",end="")
        elif a[x]=="0":#黑色
            print("\033[40m ",end="")
        elif a[x]=="2":#绿色
            print("\033[42m ",end="")
        elif a[x]=="3":#黄色
            print("\033[43m ",end="")
        elif a[x]=="4":#深蓝色
            print("\033[44m ",end="")
        elif a[x]=="5":#紫色
            print("\033[45m ",end="")
        elif a[x]=="6":#浅蓝色
            print("\033[46m ",end="")
        elif a[x]=="7":#浅白色
            print("\033[47m ",end="")
        else:
            print(a[x],end="")
        sleep(0.01)
    print("\033[0m")

def hy_light(a):#亮的输出logo
    import time
    for x in range(len(a)):
        if a[x]=="1":
            print("\033[107m ",end="")#白
        elif a[x]=="2":
            print("\033[102m ",end="")#绿
        elif a[x]=="3":
            print("\033[101m ",end="")#红
        elif a[x]=="4":
            print("\033[103m ",end="")#黄
        elif a[x]=="5":
            print("\033[104m ",end="")#蓝
        elif a[x]=="6":
            print("\033[105m ",end="")#紫
        elif a[x]=="7":
            print("\033[106m ",end="")#青蓝
        elif a[x]=="8":
            print("\033[100m ",end="")#灰
        elif a[x]=="0":
            print("\033[0m ",end="")#空格
        else:
            print(a[x],end="")
        sleep(0.01)
    print("\033[0m")

def jzt():
    jindu = 0
    for i in range(50):
        print("\033[96m加载中... "+str(jindu)+"%\033[0m")
        sleep(0.05)
        jindu=jindu+2
        def clear():
            sys.stdout.write("\033[2J\033[00H")
        clear()

def clear():
    sys.stdout.write("\033[2J\033[00H")

def tkprint(aaaaa,bbbbb):
    messagebox.showinfo(aaaaa,bbbbb)

def translate(content):
    url = "http://fanyi.youdao.com/translate?doctype=json&type=AUTO&i="+content
    r = requests.get(url)
    result = r.json()
    return result["translateResult"][0][0]["tgt"]
def card(a):#这个函数改了，不要说我抄袭
    h1 = "─"
    h2 = "-"
    f = "!@#$%^&*()_+-=,.`\[]{};':<>|"
    list = [49,50,51,52,53,54,55,56,57,48,183,65]
    i = 1
    l = 65
    y = 0
    n = 0
    for i in range(57):
        if i == 26:
            l=96
        l = l+1
        list.append(l)
    for i in range(len(a)):
        i1 = i+1
        a1 = a[i:i1]
        a1 = ord(a1)
        if a1 in list :
            y = y+1
        else:
            n = n+1
    if n == 0 and y > 0:
        k1 = "─"
        k2 = "-"
    if n > 0 and y == 0:
        k1 = "─"*2
        k2 = "-"*2
    else:
        k1 = "─"
        k2 = "-"
    for i in range(len(a)):
        h1 = h1+k1
        h2 = h2+k2
    if n > 0 and y > 0:
        h1 = h1+"─"*n
        h2 = h2+"-"*n
    print("┌─"+h1+"┐")
    time.sleep(0.05)
    print("│-"+h2+"│")
    time.sleep(0.05)
    print("│ "+a+" │")
    time.sleep(0.05)
    print("│-"+h2+"│")
    time.sleep(0.05)
    print("└─"+h1+"┘")

def hy_randint(aa,bb):
    num=random.randint(aa,bb)
    return num

def p(txet):
    print(txet)