import requests
import inspect

def main():
    path =  inspect.getfile(requests)[:-20]+"m1key/COMMANDS.md"
    f = open(path,"r")
    print(f.read())