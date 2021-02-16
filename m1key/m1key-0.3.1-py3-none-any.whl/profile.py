from PIL import Image
import inspect
import requests

DRAWING_CHARS = ['#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ']


def resize_image(image,new_width=40):
    width,height = image.size
    ratio = height/width
    new_height = int(new_width*ratio*0.80)
    resized_image = image.resize((new_width,new_height))
    return(resized_image)

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([DRAWING_CHARS[pixel//27] for pixel in pixels])
    return(characters)
    

def main_image(new_width=40):
    path =  inspect.getfile(requests)[:-20]+"m1key/profile.jpeg"
    image = Image.open(path)
    new_image = pixels_to_ascii((resize_image(image)).convert("L"))
    pixel_count = len(new_image)
    ascii_image = "\n".join(new_image[i:(i+new_width)] for i in range(0,pixel_count,new_width))
    print(ascii_image)
    print()
    print("""Hello, it's Mithilesh Tiwari , aka m1key. Welcome to m1key world.
Run m1key -h to know what you can do...""")

def main():
    path =  inspect.getfile(requests)[:-20]+"m1key/profile.txt"
    f = open(path,"r")
    print(f.read())
    print("""Hello, it's Mithilesh Tiwari , aka m1key. Welcome to m1key world.
I am currently pursuing B.Tech from Motilal Nehru National Institute of Technology 
in Information Technology. I am currently in 6th semester.\nSince I got bore in this covid period, so I decided to made this package. I hope you will enjoy :) 
Run m1key -h or m1key -c to know more what you can do""")