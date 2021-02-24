from time import *
from turtle import *
pen = Turtle()
pen.hideturtle()
pen.penup()
sc = Screen()
sc.setup(500,500)
def prtd(something,speet):
      number = 0
      for i in range(len(something)):
            print(something[number],end = "")
            sleep(speet)
            number += 1
      print()
      sleep(0.3)
'''turprint(some,size,x,y),括号里some的位置填想打印的文本，size的位置填文本大小,place的位置填"center"、"left"、"right"等'''
def turprint(some,size,place):
    write(some,align=place,font=("微软雅黑", size,"normal"))
def libnumber():
      prtd("当前版本号：0.1.0")