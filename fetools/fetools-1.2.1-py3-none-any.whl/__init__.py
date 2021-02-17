import os

__all__ = ["pause", "cls", "rgb_to_int", "int_to_rgb"]


#########################
# Misc. helpers
#########################

def pause():
    """ Does 'Press any key to continue' """
    if os.name == "nt":
        print()
        os.system("pause")
    else:
        input("\nPress Enter to continue . . . ")

def cls():
    """ Clear the terminal/command prompt """
    os.system("cls" if os.name=="nt" else "clear")


#########################
# Color converters
#########################

def rgb_to_int(r, g, b):
    """ Convert color from RGB to 24-bit integer """
    return b*65536 + g*256 + r

def int_to_rgb(num):
    """ Convert color from 24-bit integer to RGB """
    color = bin(num)[2:].zfill(24)
    b = int(color[:8], 2)
    g = int(color[8:16], 2)
    r = int(color[16:], 2)
    return r, g, b
