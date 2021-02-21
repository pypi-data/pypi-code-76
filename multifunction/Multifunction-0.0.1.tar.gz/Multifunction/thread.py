#coding:utf-8
import threading

def start(methods, parameter):
    m = threading.Thread(target=methods, args=parameter)
    m.start()