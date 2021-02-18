from time import*
from sys import*
from datetime import*
def printf(a):
    for b in a:
        sleep(0.1)
        print(b, end = '', flush=True)
def clear():
    print("\033[2J")
    print("\033[99999999A")
def logo(color):
    for x in range(len(color)):
        if color[x]=="0":
            print("\033[40m ",end="")
        elif color[x]=="1":
            print("\033[41m ",end="")
        elif color[x]=="2":
            print("\033[42m ",end="")
        elif color[x]=="3":
            print("\033[43m ",end="")
        elif color[x]=="4":
            print("\033[44m ",end="")
        elif color[x]=="5":
            print("\033[45m ",end="")
        elif color[x]=="6":
            print("\033[46m ",end="")
        elif color[x]=="7":
            print("\033[47m ",end="")
        else:
            print(color[x],end="")
    print("\033[0m")
def hello():
    h=datetime.now().hour
    if h==6 or h==7 or h==8:
        print("早上好！")
    elif h==9 or h==10:
        print("上午好！")
    elif h==11 or h==12:
        print("中午好！")
    elif h==13 or h==14 or h==15 or h==16:
        print("下午好！")
    elif h==17 or h==18:
        print("傍晚好！")
    else:
        print("晚上好！")
def help():
    print("printf is used to output word by word.")
    print("clean is used to clear terminals.")
    print("logo is used to do logo.")
    print("hello is used to say hello.")