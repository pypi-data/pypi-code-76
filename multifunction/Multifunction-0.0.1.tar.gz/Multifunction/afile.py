#coding:utf-8
import os

def file_exists(path):
    if not os.path.exists(path):
        return True
    else:
        return False


def file_remove(path):
    os.remove(path)


def create_folder(path):
    os.mkdir(path)