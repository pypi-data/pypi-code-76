import os
import keyboard
import PIL.ImageGrab
import time
import pyperclip
import pytesseract
from playsound import playsound
import win32gui
import win32api
import pyautogui
from win32api import GetSystemMetrics
import site
print("this project is about converting image from your screen to text\nto choose the area press ctrl, then for english press ctrl again, shift for hebrew and alt for arabic, an rectangle will be shown and the area in the rectangle will be converted to text and copied to your clipboard (press ctrl + v after choosing the area)\ndisclaimer: the actual code that converts the image to text is not made by me, its by google, I just made a way to make the usage of their code better")
if not os.path.exists("Tesseract-OCR"):
    print("please wait three minutes, we are downloading the files, it will take some time(:")
    from mega import Mega

    mega = Mega()

    m = mega.login()
    try:
        m.download_url('https://mega.nz/file/J6ZnjQYB#VmlsnPQFCU0lroPUw8moR_CSVXfDE9aWNQPdM-iCP88')
    except:
        pass

    import zipfile

    with zipfile.ZipFile("Tesseract-OCR.zip", 'r') as zip_ref:
        zip_ref.extractall()
    os.remove("Tesseract-OCR.zip")
    print("finished downloading the files")
directory = fr"{site.getsitepackages()[1]}\\snirocr\\"
playsound(directory + "startup.wav", block = False)
first_key = keyboard.read_key()
while first_key != "ctrl":
    first_key = keyboard.read_key()
    print("waiting for the keys")
playsound(directory + "first_click.wav", block=False)
print(first_key, "pressed (first key)")
firstx, firsty = pyautogui.position()
time.sleep(0.3)
second_key = keyboard.read_key()
while second_key != "ctrl" and second_key != "alt" and second_key != "shift":
    second_key = keyboard.read_key()
    print("waiting for the keys")
print(second_key, "pressed (second key)")
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"
dc = win32gui.GetDC(0)
red = win32api.RGB(255, 0, 0)
x, y = pyautogui.position()
if x < firstx:
    tempx, tempy = x, y
    x, y = firstx, firsty
    firstx, firsty  = tempx, tempy
try:
    im = PIL.ImageGrab.grab(bbox=(firstx, firsty, x, y))
except:
    im = PIL.ImageGrab.grab(bbox=(x, y, firstx, firsty))
my_image = pyautogui.screenshot()
playsound(directory + "second_click.wav", block=False)
for num1 in range(35):
    for num in range(firsty, y):
        win32gui.SetPixel(dc, firstx - 1, num, red)
        win32gui.SetPixel(dc, firstx - 2, num, red)
        win32gui.SetPixel(dc, x + 1, num, red)
        win32gui.SetPixel(dc, x + 2, num, red)
    for num in range(firstx - 2, x + 2):
        win32gui.SetPixel(dc, num, firsty + 1, red)
        win32gui.SetPixel(dc, num, firsty, red)
        win32gui.SetPixel(dc, num, y, red)
        win32gui.SetPixel(dc, num, y - 1, red)
lang = ""
if second_key == "ctrl":
    lang = "eng"
    print("language: eng")
elif second_key == "shift":
    lang = "heb"
    print("language: hebrew")
else:
    lang = "ara"
    print("language: arabic")
try:
    clipboard_text = pytesseract.image_to_string(im, lang=lang).strip()
    print("the clipboard:", clipboard_text)
    if len(clipboard_text) < 5:
        raise Exception
except Exception as e:
    playsound(directory + "negativebeep.wav", block=False)
    time.sleep(1)
    hwnd = win32gui.WindowFromPoint((0, 0))
    monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
    win32gui.InvalidateRect(hwnd, monitor, True)
    print("cleaned")
    if len(str(e)) == 0:
        print("cant get the text from the image")
    else:
        print("the error:", e)
    quit()
pyperclip.copy(clipboard_text)
playsound(directory + "success.wav", block=False)
hwnd = win32gui.WindowFromPoint((0,0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
win32gui.InvalidateRect(hwnd, monitor, True)
time.sleep(1.5)
quit()

