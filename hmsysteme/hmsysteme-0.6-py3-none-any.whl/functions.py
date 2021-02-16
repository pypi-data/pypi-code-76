import multiprocessing
import pygame
#from queue import Queue
queue=multiprocessing.Queue(maxsize=1)
import pickle
import time
import os
from pathlib import Path

path=os.path.realpath(__file__)
path=path.replace('functions.py','')

def get_path():
    return path
    
def screenshot_refresh():
    try:
        file = open((os.path.join(path, "hmscreen")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmscreen", False)
            return True
        else:
            return False
    except:
        return False
    
def take_screenshot(screen):
    try:
        os.remove(os.path.join(path,"screencapture.png"))
    except:
        True
    pygame.image.save(screen, os.path.join(path,"screencapture.png"))
    file = open((os.path.join(path, "hmscreen")), 'wb')
    pickle.dump(True, file)
    file.close()
    
    

def game_isactive():
    try:
        file = open((os.path.join(path, "hmsys")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != True:
            clear_pickle("hmsys",True)
            return False
        else:
            return True
    except:
        return True
    
def clear_pickle(filename, val):
    file = open((os.path.join(path, filename)), 'wb')
    pickle.dump(val, file)
    file.close()
    

def close_pygame():
    file = open((os.path.join(path, "hmsys")), 'wb')
    pickle.dump(False, file)
    file.close()

def put_pos(pos):
    file = open((os.path.join(path, "hmpos")), 'wb')
    pickle.dump(pos, file)
    file.close()
    
def get_size():
    return (1366,768)

def get_pos():
    try:
        file = open((os.path.join(path, "hmpos")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmpos", False)
            return q
        else:
            return False
    except:
        return False
        
def put_hit():
    file = open((os.path.join(path, "hmhit")), 'wb')
    pickle.dump(True, file)
    file.close()


def hit_detected():
    try:
        file = open((os.path.join(path, "hmhit")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmhit", False)
            return q
        else:
            return False
    except:
        return False
        
def put_playernames(playernames):
    file = open((os.path.join(path, "hmplayers")), 'wb')
    pickle.dump(playernames, file)
    file.close()   
    
def get_playernames():
    try:
        file = open((os.path.join(path, "hmplayers")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            w=[]
            for i in range(0,len(q)):
                if q[i][1]==True:
                    w.append(q[i][0])               
            return w
        else:
            return False
    except:
        return False
    
def clear_all():    
    clear_pickle("hmhit", False)
    clear_pickle("hmsys", True)
    clear_pickle("hmpos", False) 
    clear_pickle("hmplayers", False)
    clear_pickle("hmscreen", False)


