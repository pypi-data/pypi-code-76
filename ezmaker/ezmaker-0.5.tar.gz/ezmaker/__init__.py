import pyautogui

import discord
from discord.ext import commands



import time
import random
import webbrowser
import tkinter as tk



def easywin():
    print("cs")


def dislbot():

#pyautogui.displayMousePosition()
    pyautogui.click(x=209, y=1062)
    time.sleep(3)
    pyautogui.click(x=114, y=15)
    time.sleep(1)
    pyautogui.press("y")
    pyautogui.press("o")
    pyautogui.press("t")
    pyautogui.press("u")
    pyautogui.press("b")
    time.sleep(1)
    pyautogui.click(x=219, y=120)
    time.sleep(3)
    pyautogui.click(x=220, y=251)
    time.sleep(3)
    pyautogui.click(x=675, y=97)
    pyautogui.press("c")
    pyautogui.press("s")
    pyautogui.press("g")
    pyautogui.press("o")
    pyautogui.press("Enter")
    time.sleep(3)
    pyautogui.click(x=603, y=866)
    time.sleep(3)
    pyautogui.click(x=1081, y=931)
    while True:
        pyautogui.click(x=1481, y=608)
        time.sleep(3)
        
        pyautogui.click(x=1081, y=946)
        time.sleep(0.5)
        pyautogui.scroll(-150)
        time.sleep(3)
        pass

    #Dislike Bot v0.2

def meno():
    


    lucka = input("MENO: ")

    print("")
    print (f"Ahoj!{lucka}")




#easy ui
def easyui3butn(size, label, t1, t2, t3, cmd):
  

                       

    root = tk.Tk()
    lol= tk.Label(root, text=label)
    lol.pack()


    yt_link = tk.Button(root, text=t1 , padx=10, pady=10, command = cmd  )
    yt_link.pack(padx=20,pady=20 )
    yt_link = tk.Button(root, text=t2 , padx=10, pady=10, )
    yt_link.pack(padx=20,pady=20 )
    yt_link = tk.Button(root, text=t3 , padx=10, pady=10)
    yt_link.pack()

    #text
    

    #canvase


    root.geometry(size)
    root.resizable(False,False)



    #mainloop
    root.mainloop()







